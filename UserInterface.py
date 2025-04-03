#file to control interface using PyQT5
#Contains functions to connect button clicks to the cube solving method and cube model
#Textbox included to store the list of actions required to solve the cube in notation

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
import cube_recognition
#from PyQt5.QtGui import *
#from PyQt5.QtCore import *
from Cube_internal import *
from cube_model import *


class MyWindow(QMainWindow):
    def __init__(self):
        #Inheritance from QMainWindow class using super()
        super(MyWindow,self).__init__()
        self.initUI()
        self._createMenu()

        
    def initUI(self):
        #setting window dimensions
        self.setGeometry(0,0, 1900, 955)
        self.setWindowTitle("Rubik's Cube Solver")

        #button to enter cube's state
        self.b1 = QtWidgets.QPushButton("Or manually input the cube's scrambled state",self)
        self.b1.resize(700,30)
        self.b1.move(1000,480)

        #instuctions for text entry
        self.label1 = QtWidgets.QLabel("Enter Configuration in order BDFLRU:",self)
        self.update()
        self.label1.move(1000,550)
        self.label1.resize(300, 30)
        #initialising textbox that user will use to enter scrambled state
        self.textbox = QLineEdit(self)
        self.textbox.move(1000, 580)
        self.textbox.resize(700,40)

        #Button to enter cube's permutation
        self.button =QtWidgets.QPushButton('Enter', self)
        self.button.move(1600,620)
        
        # connect button to function on_click
        self.button.clicked.connect(self.button_clicked1)
        

        #button to enter scrambled state via webcam
        self.b2 = QtWidgets.QPushButton(self)
        self.b2.setText("Click to start video capture of cube")
        self.b2.resize(700,300)
        #self.b2.setStyleSheet()
        self.b2.setStyleSheet(
                              "QPushButton::hover"
                              "{"
                              "border : 2px solid blue ;border-radius : 60px;"
                              "background-color : lightblue;"
                              "}")
        self.b2.clicked.connect(self.button_clicked)
        self.b2.move(150,450)

        #Initialising textbox that will display solving steps 
        self.textbox1 = QPlainTextEdit(self)
        self.textbox1.move(600, 150)
        self.textbox1.resize(700,200)
        self.textbox1.insertPlainText("Steps to Solve Cube:")


# If videocam input button is clicked
    def button_clicked(self):
        #self.label.setText("you pressed the button")        
        state=cube_recognition.screen_record()
        print(state)
        self.textbox1.insertPlainText(str(state)+'/n')


#If maunal text entry for permutation of cube is selected
    def button_clicked1(self):
        textboxValue = self.textbox.text()
        state={'B': [],'D': [],'F': [],'L': [],'R': [],'U': []}


        n=0
        for i in state:
            for j in range(3):
                state[i].append(list(textboxValue[n:n+3]))
                n+=3
        self.solver(state)


# inputs the scrambled state of the cube, applies the solving algorithm and displays the model
# using the DisplayCube() class 

    def solver(self,state):
        textboxValue=str(state)
        self.textbox1.insertPlainText(textboxValue+'\n\n')
        cube = DisplayCube(state)
        #cube_model = DisplayCube(state)
        cube.print_cube()

        stage = cube.get_cur_stage()
        print('initial stage: ', stage)

        cube.solve()
        cube.print_cube()

        #displays steps to solve in textbox
        self.textbox1.insertPlainText("Actions:\n\n" + ' '.join(cube._actions)+'\n')

        
        cube.display_sequence_algorithm(cube._actions)




#menu button to help user exit the application
    def _createMenu(self):
        self.menu = self.menuBar().addMenu("&Menu")
        self.menu.addAction('&Exit', self.close)


#stylesheet of the main window which applies the background image to the UI

stylesheet = """
    MyWindow {
        border-image: url("background.png"); 
        background-repeat: no-repeat; 
        background-position: center;
    }
"""



#Starts up the window and applies the style sheet above to the window

def window():
    app = QApplication(sys.argv)
    app.setStyleSheet(stylesheet)
    win = MyWindow()
    win.show()
    sys.exit(app.exec_())


window()