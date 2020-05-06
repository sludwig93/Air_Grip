from MainWindow import Ui_MainWindow
from dorna_functions_v2 import *
from PyQt5 import QtWidgets, uic
import sys, time


class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        self.ui.push_connect.clicked.connect(dorna_connect)
        self.ui.push_home.clicked.connect(dorna_home)
        self.ui.push_zeros.clicked.connect(dorna_zeros)
        self.ui.push_calibrate.clicked.connect(self.calibrate)
        self.ui.push_reset.clicked.connect(dorna_reset)
        self.ui.push_disconnect.clicked.connect(dorna_disconnect)
        
        
        self.ui.j0_absolute_push.clicked.connect(self.j0_absolute)
        self.ui.j1_absolute_push.clicked.connect(self.j1_absolute)
        self.ui.j2_absolute_push.clicked.connect(self.j2_absolute)
        self.ui.j3_absolute_push.clicked.connect(self.j3_absolute)
        self.ui.j4_absolute_push.clicked.connect(self.j4_absolute)
        
        
        self.ui.j0_relative_push.clicked.connect(self.j0_relative)
        self.ui.j1_relative_push.clicked.connect(self.j1_relative)
        self.ui.j2_relative_push.clicked.connect(self.j2_relative)
        self.ui.j3_relative_push.clicked.connect(self.j3_relative)
        self.ui.j4_relative_push.clicked.connect(self.j4_relative)
        
        
    def j0_absolute(self):
        val = self.ui.j0_abs_line_edit.text()
        val = float(val)
        j0.move_abs(val)

        
    def j1_absolute(self):
        val = self.ui.j1_abs_line_edit.text()
        val = float(val)
        j1.move_abs(val)

        
    def j2_absolute(self):
        val = self.ui.j2_abs_line_edit.text()
        val = float(val)
        j2.move_abs(val)

        
    def j3_absolute(self):
        val = self.ui.j3_abs_line_edit.text()
        val = float(val)
        j3.move_abs(val)


    def j4_absolute(self):
        val = self.ui.j4_abs_line_edit.text()
        val = float(val)
        j4.move_abs(val)
        
        
    def j0_relative(self):
        val = self.ui.j0_rel_line_edit.text()
        val = float(val)
        j0.move_rel(val)

        
    def j1_relative(self):
        val = self.ui.j1_rel_line_edit.text()
        val = float(val)
        j1.move_rel(val)

        
    def j2_relative(self):
        val = self.ui.j2_rel_line_edit.text()
        val = float(val)
        j2.move_rel(val)

        
    def j3_relative(self):
        val = self.ui.j3_rel_line_edit.text()
        val = float(val)
        j3.move_rel(val)


    def j4_relative(self):
        val = self.ui.j4_rel_line_edit.text()
        val = float(val)
        j4.move_rel(val)
        
    def calibrate(self):
        j0.calibrate()
        j1.calibrate()
        j2.calibrate()
        j3.calibrate()
        j4.calibrate()


dorna_connect()
connected = check_connect()

robot.set_limit({'j0':[-360, 720]})

if connected == False:
    print('Try reconnecting USB and restarting program.\n\n')
    sys.exit()

j0 = Joint('j0', 0)
j1 = Joint('j1', 1)
j2 = Joint('j2', 2)
j3 = Joint('j3', 3)
j4 = Joint('j4', 4)

jointList = [j0, j1, j2, j3, j4]

app = QtWidgets.QApplication(sys.argv)

window = Window()
window.show()

app.exec()


