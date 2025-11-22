# Copyright (c) 2024 Juan Luis Gabriel
# This software is released under the MIT License.
# https://opensource.org/licenses/MIT

"""Aircraft Tracker

This program is an open source real-time aircraft tracker that visualizes Aerofly FS4 - (C) Copyright IPACS -
flight simulator data on an interactive map. It can be used to track flights, analyze routes,
and enhance the overall simulation experience. Key features include:

- Receives UDP data from Aerofly FS4 (C) flight simulator
- Displays the aircraft's position on a customizable map interface
- Shows real-time flight information including latitude, longitude, altitude, ground speed, heading, pitch, and roll
- Allows users to switch between different map styles
- Updates the aircraft's position and orientation in real-time
- Provides a user-friendly GUI for easy interaction
- Flight path recording with visual trail
- Flight statistics panel with key metrics
- Auto-center toggle for map exploration
- Unit conversion between Imperial and Metric systems

Version 27: Added unit conversion system to switch between Imperial (ft, kts, nm) and Metric (m, km/h, km) units.

"""

import socket
import threading
import re
import tkinter as tk
from tkintermapview import TkinterMapView
from tkinter import font as tkfont
from PIL import Image, ImageTk
from typing import Optional, Dict, Any, Tuple, List
from dataclasses import dataclass
from datetime import datetime
import time
import math

# Constants
UDP_PORT = 49002
WINDOW_SIZE = "1200x700"
MAP_SIZE = (900, 700)
CONTROL_FRAME_WIDTH = 300
INFO_DISPLAY_SIZE = (30, 7)
STATS_DISPLAY_SIZE = (30, 8)
UPDATE_INTERVAL = 100  # milliseconds
RECEIVE_TIMEOUT = 5.0  # seconds
PATH_COLOR = "#00BFFF"  # Deep Sky Blue for flight path
PATH_MIN_DISTANCE = 0.0005  # Minimum distance to add new point (degrees, ~50m)

@dataclass
class GPSData:
    """Dataclass to store GPS data received from the flight simulator."""
    longitude: float
    latitude: float
    altitude: float
    track: float
    ground_speed: float

@dataclass
class AttitudeData:
    """Dataclass to store attitude data received from the flight simulator."""
    true_heading: float
    pitch: float
    roll: float

class UDPReceiver:
    """
    Class responsible for receiving and parsing UDP data from the flight simulator.
    """
    def __init__(self, port: int = UDP_PORT):
        self.port = port
        self.socket: Optional[socket.socket] = None
        self.latest_gps_data: Optional[GPSData] = None
        self.latest_attitude_data: Optional[AttitudeData] = None
        self.running: bool = False
        self.receive_thread: Optional[threading.Thread] = None
        self.last_receive_time: float = 0

    def start_receiving(self) -> None:
        """Initialize and start the UDP receiving thread."""
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.socket.settimeout(0.5)  # Set a timeout for the socket
        self.socket.bind(('', self.port))
        self.running = True
        self.receive_thread = threading.Thread(target=self._receive_data)
        self.receive_thread.start()

    def _receive_data(self) -> None:
        """Continuously receive and parse UDP data while the thread is running."""
        while self.running:
            try:
                data, _ = self.socket.recvfrom(1024)
                self.last_receive_time = time.time()
                message = data.decode('utf-8')
                if message.startswith('XGPS'):
                    self.latest_gps_data = self._parse_gps_data(message)
                elif message.startswith('XATT'):
                    self.latest_attitude_data = self._parse_attitude_data(message)
            except socket.timeout:
                # This is expected, just continue the loop
                pass
            except Exception as e:
                print(f"Error receiving data: {e}")

    @staticmethod
    def _parse_gps_data(message: str) -> Optional[GPSData]:
        """Parse GPS data from the received message."""
        pattern = r'XGPSAerofly FS 4,([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+),([-\d.]+)'
        match = re.match(pattern, message)
        if match:
            return GPSData(*map(float, match.groups()))
        return None

    @staticmethod
    def _parse_attitude_data(message: str) -> Optional[AttitudeData]:
        """Parse attitude data from the received message."""
        pattern = r'XATTAerofly FS 4,([-\d.]+),([-\d.]+),([-\d.]+)'
        match = re.match(pattern, message)
        if match:
            return AttitudeData(*map(float, match.groups()))
        return None

    def get_latest_data(self) -> Dict[str, Any]:
        """Return the latest received GPS and attitude data."""
        return {
            'gps': self.latest_gps_data,
            'attitude': self.latest_attitude_data,
            'connected': (time.time() - self.last_receive_time) < RECEIVE_TIMEOUT
        }

    def stop(self) -> None:
        """Stop the UDP receiving thread and close the socket."""
        self.running = False
        if self.receive_thread:
            self.receive_thread.join()
        if self.socket:
            self.socket.close()

class AircraftTrackerApp:
    """
    Main application class for the Aircraft Tracker.
    Handles the GUI and updates the aircraft position on the map.
    """
    def __init__(self, master: tk.Tk):
        self.master = master
        self.master.title("Aircraft Tracker - Aerofly FS4")
        self.master.geometry(WINDOW_SIZE)

        # Flight path recording
        self.flight_path_points: List[Tuple[float, float]] = []
        self.path_line = None

        # Flight statistics
        self.flight_start_time: Optional[datetime] = None
        self.flight_start_position: Optional[Tuple[float, float]] = None
        self.total_distance: float = 0.0  # in nautical miles
        self.max_altitude: float = 0.0  # in feet
        self.max_speed: float = 0.0  # in knots
        self.speed_samples: List[float] = []
        self.last_position: Optional[Tuple[float, float]] = None

        # Auto-center control
        self.auto_center_enabled = tk.BooleanVar(value=True)

        # Unit system control (False = Imperial, True = Metric)
        self.use_metric_units = tk.BooleanVar(value=False)

        self.setup_ui()
        self.udp_receiver = UDPReceiver()
        self.udp_receiver.start_receiving()
        self.setup_aircraft_marker()
        self.update_aircraft_position()

    def setup_ui(self):
        """Set up the main user interface components."""
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(fill="both", expand=True)

        # Create and configure the map widget
        self.map_widget = TkinterMapView(self.main_frame, width=MAP_SIZE[0], height=MAP_SIZE[1], corner_radius=0)
        self.map_widget.pack(side="left", fill="both", expand=True)

        # Create the control frame for additional UI elements
        self.control_frame = tk.Frame(self.main_frame, width=CONTROL_FRAME_WIDTH)
        self.control_frame.pack(side="right", fill="y")

        # Connection status at the top
        self.connection_status = tk.Label(self.control_frame, text="Disconnected", fg="red", font=("Arial", 10, "bold"))
        self.connection_status.pack(pady=5)

        self.setup_map_controls()
        self.setup_map_selection()
        self.setup_info_display()
        self.setup_stats_display()

        # Add a close button
        self.close_button = tk.Button(self.control_frame, text="Close", command=self.close_application, bg="#ff6b6b", fg="white")
        self.close_button.pack(side="bottom", pady=10)

        # Set up the window close protocol
        self.master.protocol("WM_DELETE_WINDOW", self.close_application)

    def setup_map_controls(self):
        """Set up map control buttons (auto-center, clear path, etc)."""
        controls_frame = tk.LabelFrame(self.control_frame, text="Map Controls", padx=5, pady=5)
        controls_frame.pack(pady=10, padx=5, fill="x")

        # Auto-center checkbox
        auto_center_check = tk.Checkbutton(
            controls_frame,
            text="Auto-Center",
            variable=self.auto_center_enabled,
            font=("Arial", 9)
        )
        auto_center_check.pack(anchor="w", pady=2)

        # Re-center button
        recenter_btn = tk.Button(
            controls_frame,
            text="⊚ Re-Center",
            command=self.recenter_map,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 9)
        )
        recenter_btn.pack(fill="x", pady=2)

        # Clear path button
        clear_path_btn = tk.Button(
            controls_frame,
            text="🗑 Clear Path",
            command=self.clear_flight_path,
            bg="#FF9800",
            fg="white",
            font=("Arial", 9)
        )
        clear_path_btn.pack(fill="x", pady=2)

        # Reset stats button
        reset_stats_btn = tk.Button(
            controls_frame,
            text="↻ Reset Stats",
            command=self.reset_statistics,
            bg="#2196F3",
            fg="white",
            font=("Arial", 9)
        )
        reset_stats_btn.pack(fill="x", pady=2)

        # Unit conversion toggle button
        self.unit_toggle_btn = tk.Button(
            controls_frame,
            text="⇄ Switch to Metric",
            command=self.toggle_units,
            bg="#9C27B0",
            fg="white",
            font=("Arial", 9)
        )
        self.unit_toggle_btn.pack(fill="x", pady=2)

    def setup_map_selection(self):
        """Set up the map selection listbox."""
        map_frame = tk.LabelFrame(self.control_frame, text="Map Style", padx=5, pady=5)
        map_frame.pack(pady=5, padx=5, fill="both", expand=True)

        self.map_listbox = tk.Listbox(map_frame, width=32, height=8, font=("Arial", 8))
        self.map_listbox.pack(fill="both", expand=True)

        for option, _ in self.get_map_options():
            self.map_listbox.insert(tk.END, option)

        self.map_listbox.bind('<<ListboxSelect>>', lambda e: self.change_map())

    def setup_info_display(self):
        """Set up the information display area."""
        info_frame = tk.LabelFrame(self.control_frame, text="Aircraft Data", padx=5, pady=5)
        info_frame.pack(pady=5, padx=5, fill="x")

        info_font = tkfont.Font(family="Consolas", size=8)
        self.info_display = tk.Text(info_frame, width=INFO_DISPLAY_SIZE[0], height=INFO_DISPLAY_SIZE[1],
                                    wrap=tk.NONE, font=info_font, bg="#f0f0f0")
        self.info_display.pack(fill="x")

    def setup_stats_display(self):
        """Set up the flight statistics display area."""
        stats_frame = tk.LabelFrame(self.control_frame, text="Flight Statistics", padx=5, pady=5)
        stats_frame.pack(pady=5, padx=5, fill="x")

        stats_font = tkfont.Font(family="Consolas", size=8)
        self.stats_display = tk.Text(stats_frame, width=STATS_DISPLAY_SIZE[0], height=STATS_DISPLAY_SIZE[1],
                                     wrap=tk.NONE, font=stats_font, bg="#e8f5e9")
        self.stats_display.pack(fill="x")

    def setup_aircraft_marker(self):
        """Set up the aircraft marker image and related variables."""
        self.aircraft_image = Image.open("aircraft_icon.png").resize((32, 32))
        self.rotated_image = ImageTk.PhotoImage(self.aircraft_image)
        self.aircraft_marker = None
        self.initial_position_set = False

    def update_aircraft_position(self):
        """
        Update the aircraft's position on the map and the information display.
        This method is called periodically to refresh the display.
        """
        data = self.udp_receiver.get_latest_data()
        if data['connected']:
            self.connection_status.config(text="● Connected", fg="green")
            if data['gps'] and data['attitude']:
                self.update_map_and_marker(data)
                self.update_info_display(data)
                self.update_flight_path(data['gps'])
                self.update_statistics(data['gps'])
        else:
            self.connection_status.config(text="● Disconnected", fg="red")
            self.clear_info_display()

        self.master.after(UPDATE_INTERVAL, self.update_aircraft_position)

    def clear_info_display(self):
        """Clear the information display when disconnected."""
        self.info_display.delete(1.0, tk.END)
        self.info_display.insert(tk.END, "Waiting for data...")

    def update_map_and_marker(self, data: Dict[str, Any]):
        """Update the map view and aircraft marker with the latest data."""
        gps_data: GPSData = data['gps']
        attitude_data: AttitudeData = data['attitude']

        if not self.initial_position_set:
            self.map_widget.set_position(gps_data.latitude, gps_data.longitude)
            self.map_widget.set_zoom(12)
            self.initial_position_set = True

        self.rotated_image = self.rotate_image(attitude_data.true_heading)

        if self.aircraft_marker:
            self.aircraft_marker.delete()

        self.aircraft_marker = self.map_widget.set_marker(
            gps_data.latitude, gps_data.longitude,
            icon=self.rotated_image,
            icon_anchor="center"
        )

        # Only auto-center if enabled
        if self.auto_center_enabled.get():
            self.map_widget.set_position(gps_data.latitude, gps_data.longitude)

    def update_info_display(self, data: Dict[str, Any]):
        """Update the information display with the latest aircraft data."""
        gps_data: GPSData = data['gps']
        attitude_data: AttitudeData = data['attitude']

        if self.use_metric_units.get():
            # Metric units
            altitude = gps_data.altitude  # meters
            ground_speed = gps_data.ground_speed * 3.6  # m/s to km/h
            alt_unit = "m"
            speed_unit = "km/h"
        else:
            # Imperial units
            altitude = gps_data.altitude * 3.28084  # meters to feet
            ground_speed = gps_data.ground_speed * 1.94384  # m/s to knots
            alt_unit = "ft"
            speed_unit = "kts"

        info_text = f"{'Lat:':<10}{gps_data.latitude:>9.4f}°\n"
        info_text += f"{'Lon:':<10}{gps_data.longitude:>9.4f}°\n"
        info_text += f"{'Alt:':<10}{altitude:>7.0f} {alt_unit}\n"
        info_text += f"{'Speed:':<10}{ground_speed:>7.1f} {speed_unit}\n"
        info_text += f"{'Heading:':<10}{attitude_data.true_heading:>7.1f}°\n"
        info_text += f"{'Pitch:':<10}{attitude_data.pitch:>7.1f}°\n"
        info_text += f"{'Roll:':<10}{attitude_data.roll:>7.1f}°\n"

        self.info_display.delete(1.0, tk.END)
        self.info_display.insert(tk.END, info_text)

    def rotate_image(self, angle: float) -> ImageTk.PhotoImage:
        """Rotate the aircraft icon image by the given angle."""
        return ImageTk.PhotoImage(self.aircraft_image.rotate(-angle))

    def update_flight_path(self, gps_data: GPSData):
        """Update the flight path trail on the map."""
        current_pos = (gps_data.latitude, gps_data.longitude)

        # Add point if it's far enough from the last one (avoid clutter)
        if not self.flight_path_points or self._calculate_distance(
            self.flight_path_points[-1], current_pos
        ) > PATH_MIN_DISTANCE:
            self.flight_path_points.append(current_pos)

            # Draw the path if we have at least 2 points
            if len(self.flight_path_points) >= 2:
                if self.path_line:
                    self.path_line.delete()
                self.path_line = self.map_widget.set_path(
                    self.flight_path_points,
                    color=PATH_COLOR,
                    width=3
                )

    def update_statistics(self, gps_data: GPSData):
        """Update flight statistics."""
        current_pos = (gps_data.latitude, gps_data.longitude)
        alt_ft = gps_data.altitude * 3.28084
        speed_kts = gps_data.ground_speed * 1.94384

        # Initialize flight start if not set
        if self.flight_start_time is None and speed_kts > 5:  # Start tracking when moving
            self.flight_start_time = datetime.now()
            self.flight_start_position = current_pos

        # Update max values
        self.max_altitude = max(self.max_altitude, alt_ft)
        self.max_speed = max(self.max_speed, speed_kts)
        self.speed_samples.append(speed_kts)

        # Keep only last 100 samples for average calculation
        if len(self.speed_samples) > 100:
            self.speed_samples.pop(0)

        # Calculate distance traveled
        if self.last_position:
            distance_nm = self._calculate_distance_nm(self.last_position, current_pos)
            self.total_distance += distance_nm

        self.last_position = current_pos

        # Update display
        self._update_stats_display()

    def _update_stats_display(self):
        """Update the statistics display text."""
        if self.flight_start_time:
            flight_time = datetime.now() - self.flight_start_time
            hours = int(flight_time.total_seconds() // 3600)
            minutes = int((flight_time.total_seconds() % 3600) // 60)
            seconds = int(flight_time.total_seconds() % 60)
            time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"
        else:
            time_str = "--:--:--"

        avg_speed = sum(self.speed_samples) / len(self.speed_samples) if self.speed_samples else 0

        if self.use_metric_units.get():
            # Metric units
            distance = self.total_distance * 1.852  # nm to km
            avg_speed_display = avg_speed * 1.852  # knots to km/h
            max_speed_display = self.max_speed * 1.852  # knots to km/h
            max_altitude_display = self.max_altitude * 0.3048  # feet to meters
            dist_unit = "km"
            speed_unit = "km/h"
            alt_unit = "m"
        else:
            # Imperial units
            distance = self.total_distance
            avg_speed_display = avg_speed
            max_speed_display = self.max_speed
            max_altitude_display = self.max_altitude
            dist_unit = "nm"
            speed_unit = "kts"
            alt_unit = "ft"

        stats_text = f"{'Time:':<12}{time_str}\n"
        stats_text += f"{'Distance:':<12}{distance:>6.1f} {dist_unit}\n"
        stats_text += f"{'Avg Speed:':<12}{avg_speed_display:>6.1f} {speed_unit}\n"
        stats_text += f"{'Max Speed:':<12}{max_speed_display:>6.1f} {speed_unit}\n"
        stats_text += f"{'Max Alt:':<12}{max_altitude_display:>6.0f} {alt_unit}\n"

        if self.flight_start_position:
            stats_text += f"{'Start:':<12}{self.flight_start_position[0]:>7.3f}°\n"
            stats_text += f"{'        ':<12}{self.flight_start_position[1]:>7.3f}°\n"
        else:
            stats_text += f"{'Start:':<12}  Not set\n"

        stats_text += f"{'Points:':<12}{len(self.flight_path_points):>6}\n"

        self.stats_display.delete(1.0, tk.END)
        self.stats_display.insert(tk.END, stats_text)

    def _calculate_distance(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """Calculate simple Euclidean distance between two points (for filtering)."""
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)

    def _calculate_distance_nm(self, pos1: Tuple[float, float], pos2: Tuple[float, float]) -> float:
        """Calculate distance in nautical miles using Haversine formula."""
        lat1, lon1 = math.radians(pos1[0]), math.radians(pos1[1])
        lat2, lon2 = math.radians(pos2[0]), math.radians(pos2[1])

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a))

        # Earth radius in nautical miles
        r_nm = 3440.065

        return c * r_nm

    def clear_flight_path(self):
        """Clear the flight path trail from the map."""
        self.flight_path_points.clear()
        if self.path_line:
            self.path_line.delete()
            self.path_line = None
        print("Flight path cleared")

    def reset_statistics(self):
        """Reset all flight statistics to initial values."""
        self.flight_start_time = None
        self.flight_start_position = None
        self.total_distance = 0.0
        self.max_altitude = 0.0
        self.max_speed = 0.0
        self.speed_samples.clear()
        self.last_position = None
        self._update_stats_display()
        print("Statistics reset")

    def toggle_units(self):
        """Toggle between imperial and metric units."""
        self.use_metric_units.set(not self.use_metric_units.get())
        if self.use_metric_units.get():
            self.unit_toggle_btn.config(text="⇄ Switch to Imperial")
            print("Units changed to Metric")
        else:
            self.unit_toggle_btn.config(text="⇄ Switch to Metric")
            print("Units changed to Imperial")

    def recenter_map(self):
        """Manually re-center the map on the aircraft."""
        data = self.udp_receiver.get_latest_data()
        if data['connected'] and data['gps']:
            gps_data = data['gps']
            self.map_widget.set_position(gps_data.latitude, gps_data.longitude)
            print("Map re-centered on aircraft")

    def change_map(self):
        """Change the map tile server based on the user's selection."""
        selected_indices = self.map_listbox.curselection()
        if selected_indices:
            _, tile_server = self.get_map_options()[selected_indices[0]]
            self.map_widget.set_tile_server(tile_server)

    @staticmethod
    def get_map_options() -> List[Tuple[str, str]]:
        """Return a list of available map options with their tile server URLs."""
        return [
            ("OpenStreetMap", "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png"),
            ("OpenStreetMap DE", "https://tile.openstreetmap.de/tiles/osmde/{z}/{x}/{y}.png"),
            ("OpenStreetMap FR", "https://a.tile.openstreetmap.fr/osmfr/{z}/{x}/{y}.png"),
            ("OpenTopoMap", "https://a.tile.opentopomap.org/{z}/{x}/{y}.png"),
            ("Google Normal", "https://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}"),
            ("Google Satellite", "https://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}"),
            ("Google Terrain", "https://mt0.google.com/vt/lyrs=p&hl=en&x={x}&y={y}&z={z}"),
            ("Google Hybrid", "https://mt0.google.com/vt/lyrs=y&hl=en&x={x}&y={y}&z={z}"),
            ("Carto Dark Matter", "https://cartodb-basemaps-a.global.ssl.fastly.net/dark_all/{z}/{x}/{y}.png"),
            ("Carto Positron", "https://cartodb-basemaps-a.global.ssl.fastly.net/light_all/{z}/{x}/{y}.png"),
            ("ESRI World Imagery", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}"),
            ("ESRI World Street Map", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Street_Map/MapServer/tile/{z}/{y}/{x}"),
            ("ESRI World Topo Map", "https://server.arcgisonline.com/ArcGIS/rest/services/World_Topo_Map/MapServer/tile/{z}/{y}/{x}")
        ]

    def close_application(self):
        """Clean up resources and close the application."""
        print("Closing Aircraft Tracker...")
        self.udp_receiver.stop()
        self.master.destroy()

if __name__ == "__main__":
    print("Starting Aircraft Tracker...")
    print(f"Listening for UDP data on port {UDP_PORT}...")
    root = tk.Tk()
    app = AircraftTrackerApp(root)
    root.mainloop()