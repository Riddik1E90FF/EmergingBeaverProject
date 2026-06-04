# we are importing infrared from the github that we are using for this project
# we are initializing Infrared
# then we are making a dict that hold the current sensor values
# calling the sensors to activate them
# if the sensors see something they give an output of 0
# return the dict with new values

from infrared import Infrared
infrared = Infrared()
class sensor_logic():
    def read_sensor(self):
        sensor_output = {
            "left": "9",
            "middle": "9",
            "right": "9"
        } # Value is what is returned from the sensor, key is the sensor themselves
        left_sensor = infrared.read_one_infrared(1)
        middle_sensor = infrared.read_one_infrared(2)
        right_sensor = infrared.read_one_infrared(3)
        # Values: 0- line was seen, 9- floor was seen
        # this works because the sensors dont need to know what these numbers mean 
        if not left_sensor:
            sensor_output["left"] = "0"
        if not middle_sensor:
            sensor_output["middle"] = "0"
        if not right_sensor:
            sensor_output["right"] = "0"
        return sensor_output