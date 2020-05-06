# Air_Grip
Software to run Dorna robot arm and pneumatic control system

# Robotic Arm:
I uploaded everything I worked on here, but only a few files are really important.
- dorna_functions_v2.py houses the functions used to operate the robot arm
- dorna_GUI_v2.py runs the GUI for simple use of the robot arm
      Neither of these files were really finished, there are probably many errors in the code which we were not able to fix due to the COVID situation.
- rev2.ui is the QtDesigner file for the GUI (QtDesigner is the GOAT and you should 100% learn it when updating the GUI)


Everything is in Python- make sure you read our final project paper which is also uploaded here for a brief background on what we did.


Modules you'll need to run these programs (off the top of my head, see the imports in the files themselves for a more accurate list)
- dorna
- json
- PyQt5


Before trying to run these programs, you should visit Dorna's website and use their browser based software to become familiar with the robot. Then, look at the documentation for their API for a basic understanding of the commands that are available. 

# Pneumatic Control System:
The pneumatic control system is driven by an Arduino. The only code in here needed to run the Arduino is the Final_PID.ino file. To edit/upload this file you need to download the Arduino environment. When that is done, go to Tools-->Board-->Arduino Mega. This will let the environment know what Arduino board you are working with. 

The code is completed. The only changes you should need to make to this code is to change the Kp, Ki, and Kd values of the PID controller to make the response quicker. You might need to alter the pressure target for the claw as the amount of air pressure needed to fully inflate the claw will vary claw to claw.

For testing of the PID response, I would recommend making a second copy of the Arduino code and changing the initiation of the control system from when virtual reality tells it to initiate to when a switch tells it to initiate. That way you don't have to turn on virtual reality to test the response of the PID system.
