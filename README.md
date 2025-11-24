# Aerofly FS4 Maps - Aircraft Tracker

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

An open-source real-time aircraft tracker for **Aerofly FS4** flight simulator. Visualize your aircraft position on an interactive map with detailed flight information.

## 🚀 Features

### Core Features
- **Real-time UDP data reception** from Aerofly FS4
- **Interactive map** displaying aircraft position
- **Live flight information**: latitude, longitude, altitude, ground speed, heading, pitch, and roll
- **Multiple map styles**: OpenStreetMap, Google Maps (Normal, Satellite, Terrain, Hybrid), ESRI, CartoDB, and more
- **Real-time updates** of aircraft position and orientation
- **User-friendly GUI** built with Tkinter
- **Connection status indicator** to know when receiving simulator data
- **Rotating aircraft icon** reflecting actual heading

### New in Version 27 ✨
- **Unit Conversion System**: Toggle between Imperial and Metric units with one click
  - **Imperial**: feet (ft), knots (kts), nautical miles (nm)
  - **Metric**: meters (m), kilometers/hour (km/h), kilometers (km)
  - Perfect for glider pilots in Europe and regions preferring metric measurements

### Version 26 Features
- **Flight Path Recording**: Visual trail showing your complete flight route on the map
- **Flight Statistics Panel**: Track distance traveled, flight time, average/max speed, max altitude, and more
- **Auto-Center Toggle**: Disable auto-centering to freely explore the map while tracking continues
- **Manual Re-center**: Quick button to snap back to aircraft position
- **Clear Path**: Reset flight trail with one click
- **Reset Statistics**: Start a fresh statistics session anytime

## 📋 Prerequisites

- Python 3.7 or higher
- Aerofly FS4 Flight Simulator
- Operating System: Windows, Linux, or macOS

## 🔧 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/jlgabriel/Aerofly-FS4-Maps.git
   cd Aerofly-FS4-Maps
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Aircraft icon** (included):
   - The repository includes an `aircraft_icon.png` file for the aircraft marker
   - The icon is already in the root directory and ready to use
   - If needed, you can replace it with your own custom icon (32x32 pixels recommended)

## 🎮 Aerofly FS4 Configuration

For this tracker to work, you must enable UDP broadcasting in Aerofly FS4:

1. Open Aerofly FS4
2. Go to **Settings**
3. Look for **UDP Output** or **Data Output** option
4. Enable GPS data (XGPS) and attitude data (XATT) transmission
5. Configure UDP port to **49002** (or modify the `UDP_PORT` constant in the code)
6. Ensure data is sent to `localhost` or `broadcast`

## 🚁 Usage

1. **Start Aerofly FS4** and load a flight

2. **Run the tracker**:
   ```bash
   python aerofly_fs4_maps.py
   ```

3. **Interface interaction**:
   - The map will automatically display your aircraft position when data is detected
   - Select different map styles from the sidebar
   - The information panel shows real-time flight data
   - The status indicator shows "Connected" (green) when receiving data

4. **Using the new features**:
   - **Flight Path**: Automatically records your flight trail in cyan blue on the map
   - **Auto-Center**: Uncheck to explore the map freely; use "Re-Center" button to return to aircraft
   - **Statistics**: View real-time flight stats including time, distance, speeds, and altitude
   - **Clear Path**: Click to remove the flight trail and start fresh
   - **Reset Stats**: Click to reset all statistics (useful for starting a new flight session)
   - **Unit Conversion**: Click "⇄ Switch to Metric" to toggle between Imperial and Metric units

5. **Close the application**:
   - Click the "Close" button
   - Or close the window normally

## 📊 Displayed Data

### Aircraft Data Panel
The tracker displays the following real-time information:

| Parameter | Unit (Imperial / Metric) | Description |
|-----------|--------------------------|-------------|
| Latitude | Degrees | Current latitude |
| Longitude | Degrees | Current longitude |
| Altitude | Feet (ft) / Meters (m) | Altitude above sea level |
| Ground Speed | Knots (kts) / Kilometers/hour (km/h) | Speed relative to ground |
| True Heading | Degrees | True heading |
| Pitch | Degrees | Pitch angle |
| Roll | Degrees | Roll angle |

### Flight Statistics Panel
Cumulative flight statistics tracked throughout your session:

| Statistic | Unit (Imperial / Metric) | Description |
|-----------|--------------------------|-------------|
| Time | HH:MM:SS | Total flight time (starts when moving) |
| Distance | Nautical Miles (nm) / Kilometers (km) | Total distance traveled |
| Avg Speed | Knots (kts) / Kilometers/hour (km/h) | Average speed during flight |
| Max Speed | Knots (kts) / Kilometers/hour (km/h) | Maximum speed reached |
| Max Alt | Feet (ft) / Meters (m) | Maximum altitude reached |
| Start Position | Lat/Lon | Flight starting coordinates |
| Points | Count | Number of path points recorded |

## 🗺️ Available Maps

The tracker includes 13 different map styles:

- **OpenStreetMap** (standard, DE, FR)
- **OpenTopoMap** (topographic)
- **Google Maps** (Normal, Satellite, Terrain, Hybrid)
- **CartoDB** (Dark Matter, Positron)
- **ESRI** (World Imagery, Street Map, Topo Map)

## 🛠️ Code Structure

```
aerofly_fs4_maps.py
├── UDPReceiver          # Class for receiving and parsing UDP data
│   ├── start_receiving()
│   ├── _receive_data()
│   ├── _parse_gps_data()
│   └── _parse_attitude_data()
│
└── AircraftTrackerApp   # Main GUI application class
    ├── setup_ui()
    ├── setup_aircraft_marker()
    ├── update_aircraft_position()
    ├── update_map_and_marker()
    └── update_info_display()
```

## 🔧 Advanced Configuration

You can modify the following constants in `aerofly_fs4_maps.py`:

```python
UDP_PORT = 49002              # UDP port for receiving data
WINDOW_SIZE = "1000x600"      # Window size
MAP_SIZE = (800, 600)         # Map widget size
UPDATE_INTERVAL = 100         # Update interval (ms)
RECEIVE_TIMEOUT = 5.0         # Connection timeout (seconds)
```

## 🐛 Troubleshooting

### Tracker doesn't show "Connected"
- Verify that Aerofly FS4 is sending UDP data on port 49002
- Ensure firewall isn't blocking the port
- Check that UDP configuration in Aerofly FS4 is enabled

### Error: "aircraft_icon.png not found"
- The icon file should be included when you clone the repository
- If missing, verify your git clone was successful: `git status`
- You can re-download the repository or get the icon from the GitHub repo directly

### Map doesn't load
- Verify your internet connection (map tiles are downloaded online)
- Some maps may have usage limitations, try a different style

## 📝 Version History

**Version 27** (Current): Added unit conversion system to toggle between Imperial (ft, kts, nm) and Metric (m, km/h, km) units. Perfect for international pilots and glider enthusiasts.

**Version 26**: Added flight path recording, flight statistics panel, and auto-center toggle for enhanced flight tracking and analysis.

**Version 25**: Added connection status indicator and improved error handling for UDP data reception.

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) for details on our code of conduct and the process for submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Juan Luis Gabriel** - [@jlgabriel](https://github.com/jlgabriel)

## 🙏 Acknowledgments

- [IPACS](https://www.aerofly.com/) for creating Aerofly FS4 Flight Simulator
- [TkinterMapView](https://github.com/TomSchimansky/TkinterMapView) for the map widget
- OpenStreetMap community and other tile providers

## ⚠️ Disclaimer

This software is not affiliated with, associated with, authorized by, endorsed by, or in any way officially connected with IPACS GbR, or any of its subsidiaries or affiliates. The official "Aerofly FS4" name as well as related names, marks, emblems, and images are registered trademarks of their respective owners.

---

**Like this project?** Give it a ⭐ on GitHub and share it with the flight simulation community!
