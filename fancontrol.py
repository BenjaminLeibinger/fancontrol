
from __future__ import print_function
from time import sleep
import os

auto_detect_sensors = True
auto_detect_path = "/sys/devices/platform"

default_sensors = ["/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp3_input",
                   "/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp2_input",
                   "/sys/devices/platform/coretemp.0/hwmon/hwmon2/temp1_input"]

fan_control = "/proc/acpi/ibm/fan"

full_speed_temp = 75
auto_speed_temp = 60

# debug = True
debug = False

tmp_file = "/tmp/fancontrol"


def main():
    if auto_detect_sensors:
        sensors = find_sensors(auto_detect_path)
    else:
        sensors = default_sensors

    avg_temp = read_sensors(sensors)

    if debug:
        print("current avg: ", avg_temp)

    if avg_temp >= full_speed_temp:
        write_speed(fan_control, "full-speed")
    elif avg_temp <= auto_speed_temp:
        write_speed(fan_control, "auto", 30)
    else:
        write_speed(fan_control, "7")


def read_sensors(sensors):
    total_temp = 0
    sensor_count = 0
    for i in range(10):
        for sensor in sensors:
            try:
                with open(sensor) as f:
                    input_line = f.readline()
                    total_temp += int(input_line) / 1000
                    sensor_count += 1

                    if debug:
                        print("{} | {}".format(sensor, int(input_line)/1000))
            except (FileNotFoundError):
                print("file not found, skipping")
                continue
        sleep(1)

    return int(total_temp/sensor_count)


def write_speed(fan_control, speed, watchdog=0):
    try:
        with open(fan_control, 'w') as f:
            if debug:
                print("write speed: {}".format(speed))

            print("level {}".format(speed), file=f)
    except (FileNotFoundError):
        print("File not found, cant write speed")
        return False
    except (PermissionError):
        print("need to run as root...")

    write_watchdog(watchdog)
    return True


def write_watchdog(time):
    try:
        with open(fan_control, 'w') as f:
            print("watchdog {}".format(time), file=f)

            if debug:
                print("watchdog: {}".format(time))
    except (FileNotFoundError):
        print("File not found, cant write watchdog")
        return False
    except (PermissionError):
        print("need to run as root...")

    return True


def find_sensors(path):
    command = '/usr/bin/find {} -type f -name "temp*_input"'.format(path)
    return run_command(command)


def run_command(command):
    os.system('{} > {}'.format(command, tmp_file))
    lines = []
    with open(tmp_file) as f:
        for line in f:
            lines.append(line.rstrip())

    os.remove(tmp_file)
    return lines


if __name__ == "__main__":
    main()
