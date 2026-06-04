# This is the mazes config your able to adjust any of these measurements and it will adjust to what you are
# looking for ill also leave these line of code here and way to find them easily
# so you can change the equation for the measurements of corridor since everyone uses different measurements:
# line use crtl + f some word to find this
class Maze_Config():
    wall_color = "Black"
    exit_color = "White"
    corridor_width = 152 #cm for now at least we can adjust to something more visually understanding later
    drive_speed = 600 # range of speed is 0-4096
    turn_speed = 2000 # range of speed is the same as drive speed
    turn_time = .8 # this is the turn time measured in seconds
    forward_time = .3 # same measurement as the turn time