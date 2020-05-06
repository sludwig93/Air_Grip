from dorna import Dorna
import msvcrt
import time
import json
import linecache

robot = Dorna()
connected = False

def check_connect():
    global connected
    
    if '"connection": 0' in robot.device():
        print('Failed to connect to robot.')
        connected = False
        
    elif '"connection": 2' in robot.device():
        print('Robot connected.')
        connected = True


def dorna_connect():

    robot.connect(port_name = None)

    robot.set_limit({'j0': [-180, 180]})

    check_connect()



def j3_home():
    
    print('''You are calibrating j3.
Press up or down arrow to make large adjustments up or down.
Press u or d to make minor adjustments up or down.
Press e to exit.''')

    robot.set_default_speed({"joint":3000,"xyz":300})
    robot.set_default_jerk({"joint": [1000, 1000, 1000, 1000, 1000]})
    robot.set_motion({"ct": 0.1, "gpa": 1, "jt": 4})

    flag = True

    while flag:
        while msvcrt.kbhit():
            char = str(msvcrt.getch())
            if char == "b'e'":
                flag = False
                robot.set_joint({'j3':0})
                print('j3 has been calibrated.')
                break
            elif char == "b'u'":
                robot.move({'path': 'joint', 'movement':1, 'j3':2}, fulfill = True, append = True)
                continue
            elif char == "b'd'":
                robot.move({'path': 'joint', 'movement':1, 'j3':-2}, fulfill = True, append = True)
                continue
            elif char == "b'H'":
                robot.move({'path': 'joint', 'movement':1, 'j3':15}, fulfill = True, append = True)
                continue
            elif char == "b'P'":
                robot.move({'path': 'joint', 'movement':1, 'j3':-15}, fulfill = True, append = True)
                continue
            else:
                continue
        

def dorna_startup():

    dorna_connect()

    if connected == True:
    
        joints = ['j0', 'j1', 'j2']

        for joint in joints:
            robot.home(joint)

        robot.set_unit({'length':'mm'})

        #robot.move({'path': 'joint', 'movement':0, 'j0':0, 'j1':0, 'j2':0, 'j3':0, 'j4': 0}, fulfill = True, append = True)

        #j3_home()

        robot.move({'path': 'joint', 'movement':0, 'j0':0, 'j1':45, 'j2':-45, 'j3':0, 'j4': 0}, fulfill = True, append = True)

        print('Startup complete')

    elif connected == False:

        print('The robot is not connected. Try unplugging.')


def dorna_reset():

    robot.move({'path': 'joint', 'movement':0, 'j0':0, 'j1':160, 'j2':-130, 'j3':0, 'j4': 0}, fulfill = True, append = True)

def dorna_reach():
    
    robot.move({'path': 'joint', 'movement':0, 'j0':0, 'j1':45, 'j2':-45, 'j3':0, 'j4': 0}, fulfill = True, append = True)

def dorna_disconnect():
    
    robot.disconnect()
    
    robot.terminate()

    print('Robot disconnected. Session terminated.')


def combine_funcs(*funcs):
    def combined_func(*args, **kwargs):
        for f in funcs:
            f(*args, **kwargs)
    return combined_func

def limit180(value):
    if value > 180:
        while value > 180:
            value = value - 360
        return value
    elif value < -180:
        while value < -180:
            value = value + 360
        return value
    else:
        return value


def dorna_position():
    current_position = json.loads(robot.position())
    return current_position


def go_to_positions():
    move_pos = [0,0,0,0,0]
    current_loc = ['','','','','']
    while True:
        for i in range(len(move_pos)):
            pos = linecache.getline('positions.txt',i+1)
            move_pos[i] = float(pos.strip("\n"))
            linecache.clearcache()
        current_pos = json.loads(robot.position())
        if move_pos != current_pos:
            robot.move({'path':'joint','movement':0,'j0':move_pos[0],'j1':move_pos[1],'j2':move_pos[2],'j3':move_pos[3],'j4':move_pos[4]}, fulfill=True, append=True)
        for i in range(len(current_pos)):
            current_loc[i] = str(current_pos[i]) + '\n'
        print(current_loc)
        out_pos = open('current_position.txt','w')
        out_pos.writelines(current_loc)
        out_pos.close()
        time.sleep(1)
        print('Updating position\n')

    


print('Functions Loaded')





        

