# ADD_GUIDANCE.md

## Problem

When using the ASUS battery charge threshold functionality on Linux, the battery threshold (e.g., 60% or 80%) resets to 100% after power events like unplugging or rebooting. This behavior is often seen on ASUS ExpertBook laptops and similar models.

## Cause

Most ASUS laptops use the `asus-nb-wmi` or `asus-wmi` kernel modules which reset the battery charging threshold to 100% on boot or when power is unplugged/replugged. This is not persistent and must be re-applied after such events.

## Solution

Create a `udev` rule or systemd service to automatically reapply your preferred charge threshold on power events.

---

### Option 1: `udev` Rule

1. Create a script to set the threshold:

```bash
sudo nano /usr/local/bin/set_charge_limit.sh
```

```bash
#!/bin/bash
echo 60 > /sys/class/power_supply/BAT0/charge_control_end_threshold
```

Make it executable:

```bash
sudo chmod +x /usr/local/bin/set_charge_limit.sh
```

2. Create the udev rule:

```bash
sudo nano /etc/udev/rules.d/99-battery-charge-limit.rules
```

```text
ACTION=="change", SUBSYSTEM=="power_supply", KERNEL=="AC", RUN+="/usr/local/bin/set_charge_limit.sh"
```

3. Reload udev:

```bash
sudo udevadm control --reload-rules
```

> ⚠️ This works best when you use a single power supply event handler like `AC`. If you use USB-C charging, you may need to adapt the rule to handle `ucsi-source-psy-*` devices.

---

### Option 2: `systemd` Service

1. Create a script:

```bash
sudo nano /usr/local/bin/set_charge_limit.sh
```

```bash
#!/bin/bash
echo 60 > /sys/class/power_supply/BAT0/charge_control_end_threshold
```

2. Make the script executable:

```bash
sudo chmod +x /usr/local/bin/set_charge_limit.sh
```

3. Create a systemd service:

```bash
sudo nano /etc/systemd/system/set-battery-threshold.service
```

```ini
[Unit]
Description=Set battery charge limit after boot
After=multi-user.target

[Service]
Type=oneshot
ExecStart=/usr/local/bin/set_charge_limit.sh

[Install]
WantedBy=multi-user.target
```

4. Enable the service:

```bash
sudo systemctl enable set-battery-threshold.service
```

This ensures the battery limit is reapplied after every reboot.

---

## Notes

- If the threshold is not applying correctly, check `dmesg | grep BAT0` to ensure the battery path is correct.
- Use `pkexec` inside scripts only if necessary. Direct `echo` redirection to `/sys/...` works only with root permissions.
- If the battery tray app uses `pkexec`, `polkit` rules can also be added to suppress repeated password prompts.

---

## Optional: Add to Tray Icon Behavior

In your tray app, you can add:

```python
def reapply_threshold_on_startup():
    set_threshold(60)  # or whatever value you prefer
```

And call it from `main()` to force consistency on each start.