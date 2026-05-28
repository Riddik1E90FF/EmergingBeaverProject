# EmergingBeaverProject
A repo for our Robot Car project in Emerging Platforms class

Running Car:
 - to open smart car pi terminal, run "ssh corona@BeaverProject.local" in power shell, password: password1
 - to push file to smart car, run this in the terminal for this project: "scp smart_car_functions.py smart_car_integration.ipynb corona@172.20.10.4:~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server/"
 - run "python smart_car_functions.py" in the pi terminal to execute the code on the smart car
 - Use "cd ~/Freenove_4WD_Smart_Car_Kit_for_Raspberry_Pi/Code/Server
jupyter-notebook --ip=0.0.0.0 --no-browser" in pi terminalto get link to online jupyter notebook to run code without having to push it to the car everytime