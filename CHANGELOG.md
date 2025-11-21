# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Version 25] - 2024

### Added
- Connection status label showing real-time connection state
- Visual indicator (green/red) for connection status
- Improved error handling for UDP data reception
- Socket timeout configuration for better connection management
- Last receive time tracking for connection monitoring

### Changed
- Enhanced UDP receiver with timeout detection
- Improved user feedback with connection status display

### Fixed
- Better handling of connection drops
- Improved error messages for UDP reception issues

## [Previous Versions]

### Features Implemented
- Real-time UDP data reception from Aerofly FS4
- Interactive map display with aircraft position
- Multiple map tile server options (13 different styles)
- Aircraft icon rotation based on true heading
- Real-time flight information display:
  - Latitude and Longitude
  - Altitude (in feet)
  - Ground Speed (in knots)
  - True Heading, Pitch, and Roll
- GPS data parsing (XGPS messages)
- Attitude data parsing (XATT messages)
- Tkinter-based GUI with map widget
- Map style selection via listbox
- Information display panel
- Close button for application shutdown
- Proper resource cleanup on exit

## Future Plans

See [Issues](https://github.com/jlgabriel/Aerofly-FS4-Maps/issues) for planned features and enhancements.

### Potential Features
- [ ] Flight path recording and playback
- [ ] Export flight data to various formats (GPX, KML, CSV)
- [ ] Configurable update intervals
- [ ] Custom aircraft icons
- [ ] Multiple aircraft tracking
- [ ] Altitude graph/history
- [ ] Speed graph/history
- [ ] Waypoint markers
- [ ] Distance measurement tools
- [ ] Flight statistics dashboard
- [ ] Dark mode UI
- [ ] Configuration file support
- [ ] Auto-reconnection on connection loss
- [ ] Audio alerts for connection status
- [ ] Plugin system for extensions

---

For detailed commit history, see the [commit log](https://github.com/jlgabriel/Aerofly-FS4-Maps/commits/).
