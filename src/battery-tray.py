#!/usr/bin python3

# battery-tray.py
# A simple battery charge limit indicator for Linux
import os
import signal
import gi
gi.require_version('Gtk', '3.0')
gi.require_version('AppIndicator3', '0.1')
from gi.repository import Gtk, AppIndicator3

APPINDICATOR_ID = 'batterytray'

# Get the directory of the current script
BASE_DIR = os.path.dirname(os.path.abspath(__file__).replace('/src', ''))

# Define paths to the icons relative to the script's directory
ICON_100 = os.path.join(BASE_DIR, 'icons', '100_32x32.png')
ICON_80 = os.path.join(BASE_DIR, 'icons', '80_32x32.png')
ICON_60 = os.path.join(BASE_DIR, 'icons', '60_32x32.png')

# Function to read the current charge control threshold
def read_threshold():
    try:
        with open('/sys/class/power_supply/BAT0/charge_control_end_threshold', 'r') as f:
            return int(f.read().strip())
    except Exception as e:
        print(f"Error reading current threshold: {e}")
        return 100  # Fallback to 100 if there's an error


# Function to set the charge control threshold
# This function requires root privileges to modify the system file
# You can use pkexec to run the command as root
# Alternatively, you can use a script with sudo permissions
# def set_threshold(value):
def set_threshold(value):
    os.system(f"pkexec bash -c 'echo {value} > /sys/class/power_supply/BAT0/charge_control_end_threshold'")
    #os.system(f"sudo /usr/local/bin/set_charge_limit.sh {value}")

def limit_60(_):
    set_threshold(60)
    #indicator.set_icon(ICON_60)
    indicator.set_icon_full(ICON_60, "Battery icon 60%")

def limit_80(_):
    set_threshold(80)
    #indicator.set_icon(ICON_80)
    indicator.set_icon_full(ICON_80, "Battery icon 80%")

def full_100(_):
    set_threshold(100)
    #indicator.set_icon(ICON_100)
    indicator.set_icon_full(ICON_100, "Battery icon 100%")

def quit(_):
    Gtk.main_quit()

def main():
    global indicator
   
    current_threshold = read_threshold()

    if current_threshold == 60:
        default_icon = ICON_60
    elif current_threshold == 80:
        default_icon = ICON_80
    else:
        default_icon = ICON_100

    indicator = AppIndicator3.Indicator.new(
        APPINDICATOR_ID,
        default_icon,  # Set icon based on current threshold
        AppIndicator3.IndicatorCategory.SYSTEM_SERVICES
    )
    indicator.set_status(AppIndicator3.IndicatorStatus.ACTIVE)

    menu = Gtk.Menu()

    item_limit = Gtk.MenuItem(label="🔋 Limit to 60%")
    item_limit.connect("activate", limit_60)
    menu.append(item_limit)

    item_limit = Gtk.MenuItem(label="🔋 Limit to 80%")
    item_limit.connect("activate", limit_80)
    menu.append(item_limit)

    item_full = Gtk.MenuItem(label="⚡ Full Charge (100%)")
    item_full.connect("activate", full_100)
    menu.append(item_full)

    item_quit = Gtk.MenuItem(label="❌ Quit")
    item_quit.connect("activate", quit)
    menu.append(item_quit)

    menu.show_all()
    indicator.set_menu(menu)

    Gtk.main()

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()

