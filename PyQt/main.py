
# PyQt5 Video player
#!/usr/bin/env python

from PyQt5 import QtGui, uic, QtWidgets
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtWidgets import (QApplication, QFileDialog, QHBoxLayout, QLabel,
        QPushButton, QSizePolicy, QSlider, QStyle, QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QMainWindow,QWidget, QPushButton, QAction
from PyQt5.QtGui import QIcon
import sys

from os import walk

import cv2
import threading
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtMultimedia import QMediaContent, QMediaPlayer
from PyQt5.QtCore import QDir, Qt, QUrl
from PyQt5 import QtWidgets
import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from threading import Timer
import time
import os
import rospy
from std_msgs.msg import String
from PyQt5 import QtCore, QtGui, QtWidgets


VERSION = "Cam_display v0.10"

import sys, time, threading, cv2
try:
    from PyQt5.QtCore import Qt
    pyqt5 = True
except:
    pyqt5 = False
if pyqt5:
    from PyQt5.QtCore import QTimer, QPoint, pyqtSignal
    from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QLabel
    from PyQt5.QtWidgets import QWidget, QAction, QVBoxLayout, QHBoxLayout
    from PyQt5.QtGui import QFont, QPainter, QImage, QTextCursor
else:
    from PyQt4.QtCore import Qt, pyqtSignal, QTimer, QPoint
    from PyQt4.QtGui import QApplication, QMainWindow, QTextEdit, QLabel
    from PyQt4.QtGui import QWidget, QAction, QVBoxLayout, QHBoxLayout
    from PyQt4.QtGui import QFont, QPainter, QImage, QTextCursor
try:
    import Queue as Queue
except:
    import queue as Queue

IMG_SIZE    = 1280,720          # 640,480 or 1280,720 or 1920,1080
IMG_FORMAT  = QImage.Format_RGB888
DISP_SCALE  = 2                # Scaling factor for display image
DISP_MSEC   = 50                # Delay between display cycles
CAP_API     = cv2.CAP_ANY       # API: CAP_ANY or CAP_DSHOW etc...
EXPOSURE    = 0                 # Zero for automatic exposure
TEXT_FONT   = QFont("Courier", 10)

camera_num  = 1               # Default camera (first in list)
image_queue = Queue.Queue()     # Queue to hold images
capturing   = True              # Flag to indicate capturing

class videowindow(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(videowindow, self).__init__(parent)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)

        self.positionSlider = QSlider(Qt.Horizontal)
        self.positionSlider.setRange(0, 0)
        self.positionSlider.sliderMoved.connect(self.setPosition)

        self.errorLabel = QLabel()
        self.errorLabel.setSizePolicy(QSizePolicy.Preferred,
                QSizePolicy.Maximum)

        # Create new action
        openAction = QAction(QIcon('open.png'), '&Open', self)        
        openAction.setShortcut('Ctrl+O')
        openAction.setStatusTip('Open movie')
        filepath = "/home/moonsuelym/opencv/PlasticCup.mp4"
        self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filepath)))
        self.playButton.setEnabled(True)
        openAction.triggered.connect(self.openFile)
        self.mediaPlayer.setPlaybackRate(1.0)
        self.mediaPlayer.play()

        # Create exit action
        exitAction = QAction(QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(self.exitCall)

        # Create menu bar and add action
        # menuBar = self.menuBar()
        # fileMenu = menuBar.addMenu('&File')
        # #fileMenu.addAction(newAction)
        # fileMenu.addAction(openAction)
        # fileMenu.addAction(exitAction)

        # Create a widget for window contents
        wid = QWidget(self)
        self.setCentralWidget(wid)

        # Create layouts to place inside widget
        controlLayout = QHBoxLayout()
        controlLayout.setContentsMargins(0, 0, 0, 0)
        # controlLayout.addWidget(self.playButton)
        # controlLayout.addWidget(self.positionSlider)

        layout = QVBoxLayout()
        layout.addWidget(videoWidget)
        layout.addLayout(controlLayout)
        layout.addWidget(self.errorLabel)

        # Set widget to contain window contents
        wid.setLayout(layout)

        self.mediaPlayer.setVideoOutput(videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)



    def openFile(self):
        print("openfile")
        fileName, _ = QFileDialog.getOpenFileName(self, "video_test.mp4",
                QDir.homePath())
        print(fileName)

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        print("openfile end")

    def exitCall(self):
        print("end video")
        self.mediaPlayer.play()
        # sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        print("enter mediastatechagned")
        # print(self.mediaPlayer.mediaStatus())
        if(self.mediaPlayer.mediaStatus() == 7):
            self.mediaPlayer.play()
            print("end1")
        
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def positionChanged(self, position):
        self.positionSlider.setValue(position)

    def durationChanged(self, duration):
        self.positionSlider.setRange(0, duration)

    def setPosition(self, position):
        self.mediaPlayer.setPosition(position)

    def handleError(self):
        self.playButton.setEnabled(False)
        self.errorLabel.setText("Error: " + self.mediaPlayer.errorString())


   
# Grab images from the camera (separate thread)
def grab_images(cam_num, queue):
    cap = cv2.VideoCapture(cam_num-1 +CAP_API)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_SIZE[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_SIZE[1])
    if EXPOSURE:
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0)
        cap.set(cv2.CAP_PROP_EXPOSURE, EXPOSURE)
    else:
        cap.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
    while capturing:
        if cap.grab():
            retval, image = cap.retrieve(0)
            if image is not None and queue.qsize() < 2:
                queue.put(image)
            else:
                time.sleep(DISP_MSEC / 1000.0)
        else:
            print("Error: can't grab camera image")
            break
    cap.release()

# Image widget
class ImageWidget(QWidget):
    def __init__(self, parent=None):
        super(ImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        self.setMinimumSize(image.size())
        self.update()

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QPoint(0, 0), self.image)
        qp.end()

# Main window
class MyWindow2(QMainWindow):
    text_update = pyqtSignal(str)

    # Create main window
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        rospy.init_node('pyqt', anonymous=True)
        self.listener()
        self.central = QWidget(self)
        self.textbox = QTextEdit(self.central)
        self.textbox.setFont(TEXT_FONT)
        self.textbox.setMinimumSize(300, 100)
        # self.text_update.connect(self.append_text)
        sys.stdout = self

        print("Camera number %u" % camera_num)
        print("Image size %u x %u" % IMG_SIZE)
        if DISP_SCALE > 1:
            print("Display scale %u:1" % DISP_SCALE)

        self.vlayout = QVBoxLayout()        # Window layout
        self.displays = QHBoxLayout()
        self.disp = ImageWidget(self)    
        self.displays.addWidget(self.disp)
        self.vlayout.addLayout(self.displays)
        self.label = QLabel(self)
        self.vlayout.addWidget(self.label)
        self.vlayout.addWidget(self.textbox)
        self.central.setLayout(self.vlayout)
        self.setCentralWidget(self.central)

        self.mainMenu = self.menuBar()      # Menu bar
        exitAction = QAction('&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(self.close)
        self.fileMenu = self.mainMenu.addMenu('&File')
        self.fileMenu.addAction(exitAction)
    
    def callback(self, data):
        if(data.data == "3"):
            self.change_stack()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

    def listener(self):
        rospy.init_node('pyqt', anonymous=True)
        rospy.Subscriber('chatter', String, self.callback)

    def change_stack(self):
        self.parent().stack.setCurrentIndex(2)

    def write(self, text):
        self.text_update.emit(str(text))

    def flush(self):
        pass

    # def stack_reset(self):
    #     self.parent().stack.setCurrentIndex(2)


#EOF
class Thankyou(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.setStyleSheet(MAIN_COLOR)
        self.listener()
        # layout = QtWidgets.QVBoxLayout(self)
        layout = QtWidgets.QHBoxLayout(self)

        self.label = QtWidgets.QLabel("감사합니다",self)
        # self.label.setAlignment(Qt.AlignCenter)
        # self.label.setGeometry(500, 300, 800, 600) #(,down,,right)
        # self.label.setAttribute(Qt.WA_TranslucentBackground, True) # 배경 투명
        self.label.setFont(QFont('Arial', 30)) # 글자 폰트, 사이즈 수정
        layout.addWidget(self.label)

    # ros 메세지 받는 부분
    def callback(self, data):
        if(data.data == "1"):
            self.change_stack()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

    def listener(self):
        rospy.init_node('pyqt', anonymous=True)
        rospy.Subscriber('chatter', String, self.callback)

    def change_stack(self):
        self.parent().stack.setCurrentIndex(1)



class FirstWidget(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.setStyleSheet(MAIN_COLOR)
        self.listener()
        # layout = QtWidgets.QVBoxLayout(self)
        layout = QtWidgets.QHBoxLayout(self)

        self.label = QtWidgets.QLabel("버릴 일회용음료수 컵 있으세요?",self)
        # self.label.setAlignment(Qt.AlignCenter)
        # self.label.setGeometry(500, 300, 800, 600) #(,down,,right)
        # self.label.setAttribute(Qt.WA_TranslucentBackground, True) # 배경 투명
        self.label.setFont(QFont('Arial', 30)) # 글자 폰트, 사이즈 수정
        self.button = QtWidgets.QPushButton("네", self)
        self.button.resize(100,200)

        # self.button.setStyleSheet(MAIN_COLOR)
        # self.button.setStyleSheet(
        # "border-style : solid;"
        # "border-width : 2px;"
        # "border-radius :3px;"
        # )
        self.button.setStyleSheet("color : white;""background : black;""border:1px solid;""border-width :5px;""border-radius : 3px;")
        # self.button.QLineEdit("margin : 30px")
        self.button.clicked.connect(self.stack_reset)

        #  아니오버튼
        self.button2 = QtWidgets.QPushButton("아니오", self)
        self.button2.resize(100,200)
        self.button2.setStyleSheet("color : white;""background : black;")
        self.button2.clicked.connect(self.change_stack)
        self.text = QtWidgets.QTextEdit
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)

    # ros 메세지 받는 부분
    def callback(self, data):
        if(data.data == "2"):
            self.stack_reset1()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

    def listener(self):
        rospy.init_node('pyqt', anonymous=True)
        rospy.Subscriber('chatter', String, self.callback)

    def change_stack(self):
        self.parent().stack.setCurrentIndex(1)

    def stack_reset(self):
        self.parent().stack.setCurrentIndex(0)

    def stack_reset1(self):
        self.parent().stack.setCurrentIndex(3)



class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        if len(sys.argv) > 1:
            try:
                camera_num = int(sys.argv[1])
            except:
                camera_num = 0
        self.stack = QtWidgets.QStackedLayout(self)
        # self.stack0 = FirstWidget(self)
        # self.stack1 = videowindow(self)
        # self.stack2 = MyWindow2(self)
        self.stack0 = MyWindow2(self)
        self.stack1 = videowindow(self)
        self.stack2 = FirstWidget(self)
        self.stack3 = Thankyou(self)
        # print(self.stack2)
        
        self.stack.addWidget(self.stack0)
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.show()

# app = QApplication(sys.argv)
# player = videowindow()
# player.resize(1240, 980)
# # player.showFullScreen()
# player.show()
app = QtWidgets.QApplication([])
main = MainWindow()
main.resize(1280, 880)
# main.showFullScreen()
app.exec()