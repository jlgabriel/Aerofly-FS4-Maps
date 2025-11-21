# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Version 26] - 2024

### Added
- **Flight Path Recording**: Visual trail on map showing complete flight route
  - Cyan blue path line with automatic point filtering
  - Clear path button to reset trail
- **Flight Statistics Panel**: Comprehensive flight data tracking
  - Total flight time (HH:MM:SS format)
  - Distance traveled in nautical miles
  - Average and maximum speed tracking
  - Maximum altitude reached
  - Flight starting position coordinates
  - Path points counter
- **Auto-Center Toggle**: Map exploration control
  - Checkbox to enable/disable automatic centering
  - Manual re-center button to snap back to aircraft
  - Allows free map exploration while maintaining tracking
- **Enhanced UI Layout**: Reorganized control panel
  - Map Controls section with all new buttons
  - Improved visual hierarchy with labeled frames
  - Better color coding for different button functions
  - Larger window size (1200x700) for better visibility

### Changed
- Increased window size to accommodate new features
- Improved control panel organization with labeled frames
- Updated Aircraft Data and Statistics displays with better formatting
- Enhanced connection status indicator with bullet point
- Improved initial map zoom level (12 instead of 10)

### Technical Improvements
- Implemented Haversine formula for accurate distance calculations
- Added point filtering to prevent path clutter (minimum 50m between points)
- Optimized statistics calculations with rolling averages
- Added proper datetime handling for flight time tracking
- Improved memory management for speed samples (limited to last 100)

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
