# EmergingBeaverProject
A repo for our Robot Car project in Emerging Platforms class

Running Car:
 - to open smart car pi terminal, run "ssh corona@BeaverProject.local" in PowerShell, password: password1
 - to push files to the smart car, run this in the terminal for this project:
   "scp smart_car_functions.py smart_car_integration.ipynb corona@172.20.10.4:~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server/"
 - run "python smart_car_functions.py" in the pi terminal to execute the code on the smart car
 - use:
   "cd ~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server && jupyter-notebook --ip=0.0.0.0 --no-browser"
   in the pi terminal to get a link to an online Jupyter notebook and run code without pushing it to the car every time

Maze Logic Folder:
 - The `full_logic` folder contains the complete maze navigation logic for the project.
 - It includes:
   - `maze_main.py` - main entry point for the maze algorithm and overall control flow
   - `maze_mapper.py` - mapping and path planning utilities
   - `maze_sensors.py` - sensor handling code for maze navigation
   - `maze_motors.py` - motor control functions for the robot car
   - `maze_config.py` - configuration settings used by the maze logic
 - Use these modules together when developing or testing the full maze navigation system.