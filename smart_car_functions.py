# to open smart car pi terminal, run "ssh corona@BeaverProject" in power shell, password: password1
# to push file to smart car, run this in the terminal for this project: "scp smart_car_functions.py corona@192.168.1.37:~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server/"
# run "python smart_car_functions.py" in the pi terminal to execute the code on the smart car
# go to http://192.168.1.37:8888/notebooks/smart_car_integration.ipynb to run the notebook live without having to ssh into the pi terminal

import time
from motor import Ordinary_Car

car = Ordinary_Car()

SPEED = 660
TURN_SPEED = 1000
CELL_SIZE_INCHES = 12

def stop():
    print("[stop]")
    car.set_motor_model(0, 0, 0, 0)


def forward(duration=1.0, speed=SPEED):
    print(f"[forward] speed={speed} duration={duration}s")
    car.set_motor_model(-speed, -speed, -speed, -speed)
    time.sleep(duration)
    stop()


def backward(duration=1.0, speed=SPEED):
    print(f"[backward] speed={speed} duration={duration}s")
    car.set_motor_model(speed, speed, speed, speed)
    time.sleep(duration)
    stop()


def turn_left(duration=0.5, speed=TURN_SPEED):
    print(f"[turn_left] speed={speed} duration={duration}s")
    car.set_motor_model(speed, speed, -speed, -speed)
    time.sleep(duration)
    stop()

def full_circle(duration=2, speed=TURN_SPEED):
    print(f"[full_circle] speed={speed} duration={duration}s")
    car.set_motor_model(speed, speed, -speed, -speed)
    time.sleep(duration)
    stop()

def turn_right(duration=0.5, speed=TURN_SPEED):
    print(f"[turn_right] speed={speed} duration={duration}s")
    car.set_motor_model(-speed, -speed, speed, speed)
    time.sleep(duration)
    stop()


def spin_test():
    turn_left(1.0)
    time.sleep(0.5)
    turn_right(1.0)


def square_test(side_duration=1.0):
    for _ in range(4):
        forward(side_duration)
        time.sleep(0.3)
        turn_right(0.6)
        time.sleep(0.3)


def full_movement_test():
    forward(0.8)
    time.sleep(0.5)
    # backward(0.5)
    # time.sleep(0.5)
    # turn_left(0.6)
    # time.sleep(0.5)
    # turn_right(0.6)
    full_circle(2.8)
    time.sleep(0.5)
    full_circle(2.8)
    time.sleep(0.5)
    full_circle(2.8)
    time.sleep(0.5)
    stop()


if __name__ == "__main__":
    print("smart_car_functions: starting full_movement_test")
    try:
        full_movement_test()
    finally:
        stop()
        if hasattr(car, "close"):
            car.close()
        print("smart_car_functions: done")