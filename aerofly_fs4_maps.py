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

Version 25: Added a connection status label and improved error handling for UDP data reception.

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
import time

# Constants
UDP_PORT = 49002
WINDOW_SIZE = "1000x600"
MAP_SIZE = (800, 600)
CONTROL_FRAME_WIDTH = 200
INFO_DISPLAY_SIZE = (24, 9)
UPDATE_INTERVAL = 100  # milliseconds
RECEIVE_TIMEOUT = 5.0  # seconds

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
        self.master.title("Aircraft Tracker")
        self.master.geometry(WINDOW_SIZE)
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

        self.setup_map_selection()
        self.setup_info_display()

        # Add a connection status label
        self.connection_status = tk.Label(self.control_frame, text="Disconnected", fg="red")
        self.connection_status.pack(pady=5)

        # Add a close button
        self.close_button = tk.Button(self.control_frame, text="Close Map", command=self.close_application)
        self.close_button.pack(side="bottom", pady=10)

        # Set up the window close protocol
        self.master.protocol("WM_DELETE_WINDOW", self.close_application)

    def setup_map_selection(self):
        """Set up the map selection listbox."""
        tk.Label(self.control_frame, text="Select Map:").pack(pady=(10, 5))

        listbox_frame = tk.Frame(self.control_frame)
        listbox_frame.pack(padx=0, pady=5)

        self.map_listbox = tk.Listbox(listbox_frame, width=24, height=13)
        self.map_listbox.pack(side="left")

        for option, _ in self.get_map_options():
            self.map_listbox.insert(tk.END, option)

        self.map_listbox.bind('<<ListboxSelect>>', lambda e: self.change_map())

    def setup_info_display(self):
        """Set up the information display area."""
        tk.Label(self.control_frame, text="Aircraft Position:").pack(pady=(10, 5))

        info_font = tkfont.Font(family="Consolas", size=9)
        self.info_display = tk.Text(self.control_frame, width=INFO_DISPLAY_SIZE[0], height=INFO_DISPLAY_SIZE[1],
                                    wrap=tk.NONE, font=info_font)
        self.info_display.pack(padx=10, pady=10)

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
            self.connection_status.config(text="Connected", fg="green")
            if data['gps'] and data['attitude']:
                self.update_map_and_marker(data)
                self.update_info_display(data)
        else:
            self.connection_status.config(text="Disconnected", fg="red")
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
            self.map_widget.set_zoom(10)
            self.initial_position_set = True

        self.rotated_image = self.rotate_image(attitude_data.true_heading)

        if self.aircraft_marker:
            self.aircraft_marker.delete()

        self.aircraft_marker = self.map_widget.set_marker(
            gps_data.latitude, gps_data.longitude,
            icon=self.rotated_image,
            icon_anchor="center"
        )

        self.map_widget.set_position(gps_data.latitude, gps_data.longitude)

    def update_info_display(self, data: Dict[str, Any]):
        """Update the information display with the latest aircraft data."""
        gps_data: GPSData = data['gps']
        attitude_data: AttitudeData = data['attitude']

        alt_ft = gps_data.altitude * 3.28084  # Convert meters to feet
        ground_speed_kts = gps_data.ground_speed * 1.94384  # Convert m/s to knots

        info_text = "=" * 24 + "\n"
        info_text += f"{'Latitude:':<15}{gps_data.latitude:>8.2f}°\n"
        info_text += f"{'Longitude:':<15}{gps_data.longitude:>8.2f}°\n"
        info_text += f"{'Altitude:':<15}{alt_ft:>6.0f} ft\n"
        info_text += f"{'Ground Speed:':<15}{ground_speed_kts:>5.2f} kts\n"
        info_text += f"{'True Heading:':<15}{attitude_data.true_heading:>8.2f}°\n"
        info_text += f"{'Pitch:':<15}{attitude_data.pitch:>8.2f}°\n"
        info_text += f"{'Roll:':<15}{attitude_data.roll:>8.2f}°\n"
        info_text += "=" * 24 + "\n"

        self.info_display.delete(1.0, tk.END)
        self.info_display.insert(tk.END, info_text)

    def rotate_image(self, angle: float) -> ImageTk.PhotoImage:
        """Rotate the aircraft icon image by the given angle."""
        return ImageTk.PhotoImage(self.aircraft_image.rotate(-angle))

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