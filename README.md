# Thinkpad T430 Fancontrol

Bios / Ubuntu default Fancontrol runs the Fan @ 4300 RPM on 80 Degrees which leads to hard shutdowns. Thinkfan runs the Fan @ 5300 RPM which also leads to hard shutdowns. But the Fan can also run @ 6300 RPM which you need for a stable System. 

This Script reads the Sensors, calculates the avg temperature over the time_range seconds and sets a new speed.


# Installation

Install lm-sensors to find and display some sensor values
```
sudo apt-get install lm-sensors 
```

Run the script via root cronjob
```
*/1 * * * * python3 /path_to/fancontrol/fancontrol.py
```

# Configuration

```
auto_detect_sensors = True
auto_detect_path = "/sys/devices/platform"

default_sensors = ["/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp3_input",
                   "/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp2_input",
                   "/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp1_input"]

fan_control = "/proc/acpi/ibm/fan"

full_speed_temp = 75
auto_speed_temp = 60

time_range = 10
```

After an Ubuntu upgrade the paths to the sensors changed, so i added an auto detection for them. 

For all temperatures over full_speed_temp we run the fan at full-speed. (~6300RPM)
For all temperatures between 75 and 60 Degree we run the Fan at level 7. (~5300RPM)
For lower temperatures we use the auto mode. 

Maybe there are better ranges, but with those i can work without unannounced shutdowns and running at least one opened Chrome, 2 - 3 opened PhpStorm, some terminals, sublime and a virtualbox vm.


# USE AT YOUR OWN RISK