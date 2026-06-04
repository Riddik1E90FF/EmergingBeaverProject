# maze_main.py
import os, sys, time
from maze_config import Maze_Config
from maze_motors import motor_functions
from maze_sensors import sensor_logic

config  = Maze_Config()
motors  = motor_functions()
sensors = sensor_logic()

_smart_car_dir = os.path.expanduser("~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server")
if os.path.isdir(_smart_car_dir) and _smart_car_dir not in sys.path:
    sys.path.insert(0, _smart_car_dir)

# Set this to the direction the car is physically facing at the start:
# 0=north  1=east  2=south  3=west
heading = 1

SENSOR_DIR = {
    0: {"left": 3, "middle": 0, "right": 1},
    1: {"left": 0, "middle": 1, "right": 2},
    2: {"left": 1, "middle": 2, "right": 3},
    3: {"left": 2, "middle": 3, "right": 0},
}


def turn_to(target):
    global heading
    rotation = (target - heading) % 4
    if rotation == 1:
        motors.turn_right()
    elif rotation == 3:
        motors.turn_left()
    elif rotation == 2:
        motors.turn_right()
        motors.turn_right()
    heading = target


def get_open_dirs():
    sensor_map  = SENSOR_DIR[heading]
    sensor_vals = sensors.read_sensor()
    open_dirs = []
    for sensor_key, direction in sensor_map.items():
        if sensor_vals[sensor_key] == "0":   # "0" = open floor
            open_dirs.append(direction)
    return open_dirs


def drive_until_wall():
    while True:
        motors.start_forward()
        time.sleep(0.05)
        motors.stop_moving()
        reading = sensors.read_sensor()
        if reading["middle"] == "9":
            motors.start_backward()
            time.sleep(.8)        # reverse for a fixed time to get back behind the tape
            motors.stop_moving()
            print(f"Heading: {heading} | Sensors: {sensors.read_sensor()}")
            time.sleep(0.8)        # pause before sensing
            return "wall"


print("Starting — place car in corridor facing forward.")
while True:
    drive_until_wall()
    open_dirs = get_open_dirs()
    came_from = (heading + 2) % 4
    forward_options = [d for d in open_dirs if d != came_from]
    if forward_options:
        turn_to(forward_options[0])
    else:
        turn_to(came_from)