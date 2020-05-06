from dorna import Dorna
import json, linecache

robot = Dorna()
robot.connect()

move_pos = [0,0,0,0,0]

def go_to_positions():
    while True:
        for i in range(len(move_pos)):
            pos = linecache.getline('positions.txt',i+1)
            move_pos[i] = float(pos.strip("\n"))
        current_pos = json.loads(robot.position())
        if move_pos != current_pos:
            robot.move({'path':'joint','movement':0,'j0':move_pos[0],'j1':move_pos[1],'j2':move_pos[2],'j3':move_pos[3],'j4':move_pos[4]}, fulfill=True, append=True)
        linecache.clearcache()
        print('Updating position\n')
