# Installation Guide - Aerofly FS4 Maps

This guide provides detailed installation instructions for different operating systems.

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation on Windows](#installation-on-windows)
- [Installation on Linux](#installation-on-linux)
- [Installation on macOS](#installation-on-macos)
- [Creating the Aircraft Icon](#creating-the-aircraft-icon)
- [Verifying Installation](#verifying-installation)
- [Troubleshooting](#troubleshooting)

---

## Prerequisites

All platforms require:
- **Python 3.7 or higher**
- **Aerofly FS4 Flight Simulator**
- **Internet connection** (for downloading map tiles)

---

## Installation on Windows

### Step 1: Install Python

1. Download Python from [python.org](https://www.python.org/downloads/)
2. Run the installer
3. **Important**: Check "Add Python to PATH" during installation
4. Verify installation:
   ```cmd
   python --version
   ```

### Step 2: Install Git (Optional)

1. Download Git from [git-scm.com](https://git-scm.com/download/win)
2. Install with default settings

### Step 3: Download the Project

**Option A: Using Git**
```cmd
git clone https://github.com/jlgabriel/Aerofly-FS4-Maps.git
cd Aerofly-FS4-Maps
```

**Option B: Download ZIP**
1. Download ZIP from GitHub
2. Extract to a folder
3. Open Command Prompt in that folder

### Step 4: Install Dependencies

```cmd
pip install -r requirements.txt
```

If you encounter issues with tkinter:
- Tkinter comes pre-installed with Python from python.org
- If missing, reinstall Python ensuring "tcl/tk and IDLE" is selected

### Step 5: Create Aircraft Icon

See [Creating the Aircraft Icon](#creating-the-aircraft-icon)

### Step 6: Run the Application

```cmd
python aerofly_fs4_maps.py
```

---

## Installation on Linux

### Step 1: Install Python and Dependencies

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-tk git
```

**Fedora:**
```bash
sudo dnf install python3 python3-pip python3-tkinter git
```

**Arch Linux:**
```bash
sudo pacman -S python python-pip tk git
```

### Step 2: Download the Project

```bash
git clone https://github.com/jlgabriel/Aerofly-FS4-Maps.git
cd Aerofly-FS4-Maps
```

### Step 3: Install Python Dependencies

```bash
pip3 install -r requirements.txt
# or
python3 -m pip install -r requirements.txt
```

### Step 4: Create Aircraft Icon

See [Creating the Aircraft Icon](#creating-the-aircraft-icon)

### Step 5: Run the Application

```bash
python3 aerofly_fs4_maps.py
```

**Optional: Create a Desktop Launcher**

Create `aerofly-tracker.desktop`:
```ini
[Desktop Entry]
Version=1.0
Type=Application
Name=Aerofly FS4 Tracker
Comment=Aircraft tracker for Aerofly FS4
Exec=/usr/bin/python3 /path/to/aerofly_fs4_maps.py
Icon=/path/to/aircraft_icon.png
Terminal=false
Categories=Game;Utility;
```

---

## Installation on macOS

### Step 1: Install Homebrew (if not installed)

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

### Step 2: Install Python

```bash
brew install python
# or download from python.org
```

### Step 3: Install Git

```bash
brew install git
# or use Xcode Command Line Tools
```

### Step 4: Download the Project

```bash
git clone https://github.com/jlgabriel/Aerofly-FS4-Maps.git
cd Aerofly-FS4-Maps
```

### Step 5: Install Dependencies

```bash
pip3 install -r requirements.txt
```

### Step 6: Create Aircraft Icon

See [Creating the Aircraft Icon](#creating-the-aircraft-icon)

### Step 7: Run the Application

```bash
python3 aerofly_fs4_maps.py
```

---

## Creating the Aircraft Icon

The application requires an `aircraft_icon.png` file (32x32 pixels recommended).

### Option 1: Create Your Own

Use any image editor (GIMP, Photoshop, Paint.NET, etc.) to create a simple airplane icon.

### Option 2: Download from Internet

Search for "airplane icon png" and download a suitable image.

### Option 3: Simple Text-Based Icon

Create a simple icon using Python:

```python
from PIL import Image, ImageDraw

img = Image.new('RGBA', (32, 32), (255, 255, 255, 0))
draw = ImageDraw.Draw(img)

# Draw a simple airplane shape
draw.polygon([(16, 2), (18, 16), (30, 14), (18, 18), (18, 28),
              (20, 30), (16, 28), (12, 30), (14, 28), (14, 18),
              (2, 14), (14, 16)], fill='blue', outline='black')

img.save('aircraft_icon.png')
print("Icon created successfully!")
```

Save this as `create_icon.py` and run:
```bash
python create_icon.py
```

### Place the Icon

Ensure `aircraft_icon.png` is in the same directory as `aerofly_fs4_maps.py`.

---

## Verifying Installation

1. **Check Python installation:**
   ```bash
   python --version
   # or
   python3 --version
   ```

2. **Check installed packages:**
   ```bash
   pip list | grep -E "tkintermapview|Pillow"
   ```

3. **Test tkinter:**
   ```bash
   python -m tkinter
   # Should open a small window
   ```

4. **Run the application:**
   ```bash
   python aerofly_fs4_maps.py
   ```

   You should see:
   - "Starting Aircraft Tracker..." message
   - A window with a map
   - "Disconnected" status (until Aerofly FS4 sends data)

---

## Troubleshooting

### "No module named 'tkinter'"

**Windows:** Reinstall Python with tkinter support enabled

**Linux:**
```bash
sudo apt install python3-tk  # Ubuntu/Debian
sudo dnf install python3-tkinter  # Fedora
```

**macOS:** Tkinter should be included. Try reinstalling Python from python.org

### "No module named 'tkintermapview'" or "No module named 'PIL'"

```bash
pip install tkintermapview Pillow
# or
pip install -r requirements.txt
```

### "aircraft_icon.png not found"

Create the icon using one of the methods in [Creating the Aircraft Icon](#creating-the-aircraft-icon)

### Application won't connect to Aerofly FS4

1. Check Aerofly FS4 UDP output is enabled
2. Verify port 49002 is not blocked by firewall
3. Ensure Aerofly FS4 is running and in-flight

### Map tiles won't load

1. Check internet connection
2. Try a different map style
3. Some tile servers may have rate limits

### Permission denied errors (Linux/macOS)

```bash
chmod +x aerofly_fs4_maps.py
```

### Port already in use

Close other applications using port 49002 or modify `UDP_PORT` in the script.

---

## Next Steps

After successful installation:

1. Read the [README.md](README.md) for usage instructions
2. Configure Aerofly FS4 UDP output (see README)
3. Start flying and tracking!

---

## Need Help?

If you encounter issues not covered here:

1. Check [GitHub Issues](https://github.com/jlgabriel/Aerofly-FS4-Maps/issues)
2. Open a new issue with:
   - Your OS and version
   - Python version
   - Error messages
   - Steps to reproduce

Happy flying! ✈️
