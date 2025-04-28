# Battery Tray

A simple battery charge limit indicator for Linux, built using Python and GTK.

## Features
- Set battery charge limit to 60%, 80%, or 100%.
- Displays a system tray icon to indicate the current charge limit.
- Easy-to-use menu for quick adjustments.

---

## Installation

### 1. Install System Dependencies
Before running the script, ensure the required system libraries are installed. Run the following commands:

```bash
sudo apt update
sudo apt install -y python3 python3-gi python3-gi-cairo gir1.2-gtk-3.0 gir1.2-appindicator3-0.1 libgirepository1.0-dev libcairo2-dev build-essential meson pkg-config
```
gi is tightly bound to the system GTK installation.
pip cannot and should not build GTK and GObject from source!
Always use the system package manager (apt) for GUI libraries.

### 2. Install Python Dependencies

---

## Run the Application
To run the application, execute the following command:

```bash
python3 src/battery-tray.py
```

---

## Project Structure

```
battery-tray/
├── src/
│   └── battery-tray.py       # Main script
├── icons/
│   ├── 100_32x32.png         # Icon for 100% charge
│   ├── 80_32x32.png          # Icon for 80% charge
│   └── 60_32x32.png          # Icon for 60% charge
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

---

## Notes
- Ensure you have the necessary permissions to modify `/sys/class/power_supply/BAT0/charge_control_end_threshold`. The script uses `pkexec` for privilege escalation.
- If icons are missing, place them in the `icons/` directory relative to the script.

---

## License
This project is licensed under the MIT License.