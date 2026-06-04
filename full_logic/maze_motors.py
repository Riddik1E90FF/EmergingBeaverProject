from motor import Ordinary_Car
from maze_config import Maze_Config
import time

motor = Ordinary_Car()
speed_config = Maze_Config()

class motor_functions():
    def stop_moving(self):
        motor.set_motor_model(0, 0, 0, 0)

    def start_forward(self):
        motor.set_motor_model(-speed_config.drive_speed, -speed_config.drive_speed,
                            -speed_config.drive_speed, -speed_config.drive_speed)

    def start_backward(self):
        motor.set_motor_model(speed_config.drive_speed, speed_config.drive_speed,
                            speed_config.drive_speed, speed_config.drive_speed)

    def forward(self):
        motor.set_motor_model(-speed_config.drive_speed, -speed_config.drive_speed,
                            -speed_config.drive_speed, -speed_config.drive_speed)
        time.sleep(0.02)
        self.stop_moving()

    def backward(self):
        motor.set_motor_model(speed_config.drive_speed, speed_config.drive_speed, speed_config.drive_speed, speed_config.drive_speed)
        time.sleep(speed_config.forward_time)
        self.stop_moving()

    def turn_left(self):
        motor.set_motor_model(speed_config.drive_speed, speed_config.drive_speed, -speed_config.turn_speed, -speed_config.turn_speed)
        time.sleep(speed_config.turn_time)
        self.stop_moving()

    def turn_right(self):
        motor.set_motor_model(-speed_config.turn_speed, -speed_config.turn_speed, speed_config.drive_speed, speed_config.drive_speed)
        time.sleep(speed_config.turn_time)
        self.stop_moving()

