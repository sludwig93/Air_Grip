from dorna import Dorna
import msvcrt
import time
import json
import linecache
import random
import socket

robot = Dorna()
connected = False

class Joint(object):
    
    def __init__(self, joint, joint_number):
        self.name = joint
        self.number = joint_number
        
    def move_abs(self, angle):
        try:
            self.current_position = json.loads(robot.position())[self.number]
            short_path = shortest_path(float(angle), self.current_position)
            robot.move({'path':'joint','movement':1,self.name:short_path}, fulfill=True, append=True)
            self.moved_position = self.current_position + short_path
            print('Moving ' + self.name + ' ' + str(short_path) + ' degrees.\n')
        except ValueError:
            print('You must enter a numeric angle.\n')           

    def move_rel(self, angle):
        self.current_position = json.loads(robot.position())[self.number]
        short_path = shortest_path(angle + self.current_position, self.current_position)
        robot.move({'path':'joint', 'movement':1, self.name:short_path}, fulfill=True, append=True)
        print('Moving ' + self.name + ' ' + str(short_path) + ' degrees.\n')
    
    def home(self):
        robot.home(self.name)
        
    def calibrate(self):
        robot.calibrate({self.name:0})
    
    def locate(self):
        self.current_position = json.loads(robot.position())[self.number]


def check_connect():
    global connected
    
    if '"connection": 0' in robot.device():
        print('Failed to connect to robot.')
        connected = False
        
    elif '"connection": 2' in robot.device():
        print('Robot connected.')
        connected = True
        
    return connected



def dorna_connect():

    robot.connect(port_name = None)
            
    
def dorna_zeros():
    robot.move({'path':'joint', 'movement':0, 'j0':0, 'j1':0, 'j2':0, 'j3':0, 'j4':0})


def dorna_home():
    homes = json.loads(robot.homed())
    for joint in homes.keys():
            robot.home(joint)
            print(joint + ' is homed.\n')


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


def limit360(value):
    if value > 360:
        while value > 360:
            value -= 360
        return value
    elif value < 0:
        while value < 0:
            value += 360
        return value
    else:
        return value


def shortest_path(desired_position, current_position):

    desired_position = limit360(desired_position)
    current_position = limit360(current_position)
    
    difference = desired_position - current_position

    if difference > 180: # not shortest path
        difference -= 360
    elif difference < -180: # not shortest path
        difference += 360
    return difference    


def dorna_position():
    current_position = json.loads(robot.position())
    return current_position


def write_rand():
    
    outList = ['','','','','']
    for i in range(0,5):
        if i == 0:
            upper = 90
            lower = 0
        elif i == 1:
            upper = 60
            lower = 0
        elif i == 2:
            upper = 20
            lower = -80
        elif i == 3:
            upper = 15
            lower = -90
        else:
            upper = 1
            lower = 0
        outList[i] = str(random.randint(lower,upper))+ '\n'
    print(outList)
    outText = open('positions.txt','w')
    outText.writelines(outList)
    outText.close()


def go_to_positions():
    move_pos = [0,0,0,0,0]
    current_loc = ['','','','','']
    short_path = [0,0,0,0,0]
    #while True:
    current_pos = dorna_position()
    for i in range(len(move_pos)):
        pos = linecache.getline('positions.txt',i+1)
        move_pos[i] = float(pos.strip("\n"))
        linecache.clearcache()
        short_path[i] = shortest_path(move_pos[i], current_pos[i])
    if current_pos != move_pos:
        robot.move({'path':'joint','movement':1,'j0':short_path[0],'j1':short_path[1],'j2':short_path[2],'j3':short_path[3],'j4':short_path[4]}, fulfill=True, append=False)
    for i in range(len(current_pos)):
        current_loc[i] = str(current_pos[i]) + '\n'
    #print(current_loc)
    out_pos = open('current_position.txt','w')
    out_pos.writelines(current_loc)
    out_pos.close()
    print('Updating position\n')
    
    
def automate_motion():
    while True:
        write_rand()
        go_to_positions()
        time.sleep(10)
        

def VR_server():
    incoming_pos = [0,0,0,0,0]
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    HOST = '10.206.16.65'
    PORT = 6000
    s.bind((HOST, PORT))
    s.listen(5)
    print('Listening for client')
    (clientsocket, address) = s.accept()
    print('Connection found')
    while True:
        data = clientsocket.recv(1024).decode()
        incoming_pos = data.split("\n")
        for i in range(len(incoming_pos)):
            incoming_pos[i] = float(incoming_pos[i])
        robot.move({'path':'joint','movement':0,'j0':incoming_pos[0],'j1':incoming_pos[1],'j2':incoming_pos[2],'j3':incoming_pos[3],'j4':incoming_pos[4]})
        r = 'Recieved'
        clientsocket.send(r.encode()) 


def motion_test():
    robot.move({'path':'joint', 'movement':0, 'j0':90, 'j1':0}, fulfill=True, append =True)
    robot.move({'path':'joint', 'movement':0, 'j0':45, 'j1':30}, fulfill=True, append =True)
    robot.move({'path':'joint', 'movement':0, 'j0':0, 'j1':45}, fulfill=True, append =True)
    
    

print('Functions Loaded\n')





        

