
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
from std_msgs.msg import String

from os import walk

import cv2
from cv_bridge import CvBridge,CvBridgeError
from sensor_msgs.msg import Image
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
import time


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
        self.resize(1920,1080)
        self.listener()
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)

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
        filepath = "/home/panda/panda/src/ui/LatteisPanda_movie/default_screen.mp4"
        self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filepath)))
        self.playButton.setEnabled(True)
        openAction.triggered.connect(self.openFile)
        self.mediaPlayer.setPlaybackRate(1.0)
        # self.mediaPlayer.play()

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
        # self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.showFullScreen()


    def openFile(self):
        print("openfile")
        fileName, _ = QFileDialog.getOpenFileName(self, "default_screen.mp4",
                QDir.homePath())
        print(fileName)

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        print("openfile end")

    def exitCall(self):
        print("end video")
        # self.mediaPlayer.stop()
        # self.mediaPlayer.play()
        # self.parent().stack.setCurrentIndex(4)
        # sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged(self, state):
        print("enter mediastatechagned")
        # print(self.mediaPlayer.mediaStatus())
        rospy.loginfo('mediaStatus1 %s', self.mediaPlayer.mediaStatus())
        if(self.mediaPlayer.mediaStatus() == 7):
            self.mediaPlayer.play()
        
            
            # self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        # else: 
        #     self.parent().stack.setCurrentIndex(4)

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def callback(self, data):
        if(data.data == "3"):
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.mediaPlayer.stop()
            self.change_stack()
        elif(data.data=="wait"):
            self.mediaPlayer.play()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)

          

    def listener(self):
        
        rospy.Subscriber('TerminalToPyqt', String, self.callback)

    def change_stack(self):
        #self.showNormal()
        self.parent().stack.setCurrentIndex(1)
        msg = "hi"
        self.pub.publish(msg)
        rospy.loginfo('I published hi')

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

class videowindow2(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(videowindow2, self).__init__(parent)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 
        
        self.listener()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)

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
        filepath = "/home/panda/panda/src/panda_video/Video/01_Introduce.mp4"
        self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filepath)))
        self.playButton.setEnabled(True)
        openAction.triggered.connect(self.openFile)
        self.mediaPlayer.setPlaybackRate(1.0)
        # self.mediaPlayer.play()

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
        #self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
        self.showFullScreen()



    def openFile(self):
        print("openfile")
        fileName, _ = QFileDialog.getOpenFileName(self, "PlasticCup.mp4",
                QDir.homePath())
        print(fileName)

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        print("openfile end")

    def exitCall(self):
        print("end video")
        # self.mediaPlayer.play()
        # self.parent().stack.setCurrentIndex(4)
        # sys.exit(app.exec_())

    def play(self):
        if (self.mediaPlayer.state() == QMediaPlayer.PlayingState):
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged2(self, state):
        print("enter mediastatechagned")
        print(self.mediaPlayer.mediaStatus())
        rospy.loginfo('mediaStatus2 %s', self.mediaPlayer.mediaStatus())
        if(self.mediaPlayer.mediaStatus() == 7):
            self.mediaPlayer.stop()
            self.parent().stack.setCurrentIndex(2)
        else:
            self.mediaPlayer.play() 
        
            
            

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def callback(self, data):
        if(data.data == "hi1"):
            self.mediaPlayer.play()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.mediaPlayer.stateChanged.connect(self.mediaStateChanged2)
            
            # self.mediaStateChanged(self,state)
        

    def listener(self):
        rospy.Subscriber('TerminalToPyqt', String, self.callback)

    def change_stack(self):
        self.parent().stack.setCurrentIndex(2)

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

class videowindow3(QtWidgets.QMainWindow):

    def __init__(self, parent=None):

        super(videowindow3, self).__init__(parent)
        self.resize(1920,1080)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 
       
        self.listener()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)

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
        filepath = "/home/panda/panda/src/panda_video/Video/02_Poor_panda.mp4"
        self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filepath)))
        self.playButton.setEnabled(True)
        openAction.triggered.connect(self.openFile)
        self.mediaPlayer.setPlaybackRate(1.0)
        # self.mediaPlayer.play()

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
        # self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)

        



    def openFile(self):
        print("openfile")
        fileName, _ = QFileDialog.getOpenFileName(self, "poor_panda.mp4",
                QDir.homePath())
        print(fileName)

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        print("openfile end")

    def exitCall(self):
        print("end video")
        # self.mediaPlayer.play()
        # self.parent().stack.setCurrentIndex(4)
        # sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged3(self, state):
        print("enter mediastatechagned")
        print(self.mediaPlayer.mediaStatus())
        rospy.loginfo('mediaStatus3 %s', self.mediaPlayer.mediaStatus())

        if(self.mediaPlayer.mediaStatus() == 7):
            self.mediaPlayer.stop()
            self.parent().stack.setCurrentIndex(4)

        else: 
            self.mediaPlayer.play()
            
        

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def callback(self, data):
        if(data.data =="0"):
            self.mediaPlayer.play()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.mediaPlayer.stateChanged.connect(self.mediaStateChanged3)
        # elif(data.data=="l"):
        #     self.change_stack()
            
    def change_stack(self):
        self.parent().stack.setCurrentIndex(2)
        

    def listener(self):
        rospy.Subscriber('TerminalToPyqt', String, self.callback)

  

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

class videowindow4(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(videowindow4, self).__init__(parent)
        self.resize(1920,1080)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 
       
        self.listener()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)

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
        filepath = "/home/panda/panda/src/panda_video/Video/04_Poor_Donation.mp4"
        self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filepath)))
        self.playButton.setEnabled(True)
        openAction.triggered.connect(self.openFile)
        self.mediaPlayer.setPlaybackRate(1.0)
        # self.mediaPlayer.play()

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
        # self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
       



    def openFile(self):
        print("openfile")
        fileName, _ = QFileDialog.getOpenFileName(self, "poor_panda.mp4",
                QDir.homePath())
        print(fileName)

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        print("openfile end")

    def exitCall(self):
        print("end video")
        # self.mediaPlayer.play()
        # self.parent().stack.setCurrentIndex(4)
        # sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged4(self, state):
        print("enter mediastatechagned")
        print(self.mediaPlayer.mediaStatus())
        rospy.loginfo('mediaStatus4 %s', self.mediaPlayer.mediaStatus())

        if(self.mediaPlayer.mediaStatus() == 7):
            self.mediaPlayer.stop()
            self.parent().stack.setCurrentIndex(7)

        else: 
            self.mediaPlayer.play()
            
        

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def callback(self, data):
        if(data.data =="5"):
            self.mediaPlayer.play()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.mediaPlayer.stateChanged.connect(self.mediaStateChanged4)
       
            
    def change_stack(self):
        self.parent().stack.setCurrentIndex(2)
        

    def listener(self):
        rospy.Subscriber('TerminalToPyqt', String, self.callback)

  

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

class videowindow5(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(videowindow5, self).__init__(parent)
        self.resize(1920,1080)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 
       
        self.listener()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)

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
        filepath = "/home/panda/panda/src/panda_video/Video/05_Thank_donation.mp4"
        self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filepath)))
        self.playButton.setEnabled(True)
        openAction.triggered.connect(self.openFile)
        self.mediaPlayer.setPlaybackRate(1.0)
        # self.mediaPlayer.play()

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
        # self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
      



    def openFile(self):
        print("openfile")
        fileName, _ = QFileDialog.getOpenFileName(self, "steamer_panda.mp4",
                QDir.homePath())
        print(fileName)

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        print("openfile end")

    def exitCall(self):
        print("end video")
        # self.mediaPlayer.play()
        # self.parent().stack.setCurrentIndex(4)
        # sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged5(self, state):
        print("enter mediastatechagned")
        print(self.mediaPlayer.mediaStatus())
        rospy.loginfo('mediaStatus5 %s', self.mediaPlayer.mediaStatus())

        if(self.mediaPlayer.mediaStatus() == 7):
            self.mediaPlayer.stop()
            self.parent().stack.setCurrentIndex(10)
            msg = "lastvideo"
            self.pub.publish(msg)
            rospy.loginfo('I published lastvideo')


        else: 
            self.mediaPlayer.play()
            
        

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def callback(self, data):
        if(data.data =="6"):
            self.mediaPlayer.play()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.mediaPlayer.stateChanged.connect(self.mediaStateChanged5)
   

    def listener(self):
        rospy.Subscriber('TerminalToPyqt', String, self.callback)

  

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

class videowindow6(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(videowindow6, self).__init__(parent)
        self.resize(1920,1080)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 
       
        self.listener()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)

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
        filepath = "/home/panda/panda/src/panda_video/Video/06_Bye.mp4"
        self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filepath)))
        self.playButton.setEnabled(True)
        openAction.triggered.connect(self.openFile)
        self.mediaPlayer.setPlaybackRate(1.0)
        # self.mediaPlayer.play()

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
        # self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
       



    def openFile(self):
        print("openfile")
        fileName, _ = QFileDialog.getOpenFileName(self, "default_screen.mp4",
                QDir.homePath())
        print(fileName)

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        print("openfile end")

    def exitCall(self):
        print("end video")
        # self.mediaPlayer.play()
        # self.parent().stack.setCurrentIndex(4)
        # sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged6(self, state):
        print("enter mediastatechagned")
        print(self.mediaPlayer.mediaStatus())
        rospy.loginfo('mediaStatus6 %s', self.mediaPlayer.mediaStatus())

        if(self.mediaPlayer.mediaStatus() == 7):
            self.mediaPlayer.stop()
            msg = "end"
            self.pub.publish(msg)
            rospy.loginfo('I published end')
            self.parent().stack.setCurrentIndex(0)


        else: 
            self.mediaPlayer.play()
            
        

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def callback(self, data):
        if(data.data =="7"):
            self.mediaPlayer.play()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.mediaPlayer.stateChanged.connect(self.mediaStateChanged6)
        elif(data.data =="lastvideo1"):
            self.mediaPlayer.play()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.mediaPlayer.stateChanged.connect(self.mediaStateChanged6)
        else:
            pass

        
        

    def listener(self):
        rospy.Subscriber('TerminalToPyqt', String, self.callback)

  

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

class videowindow7(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(videowindow7, self).__init__(parent)
        self.resize(1920,1080)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 
       
        self.listener()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)

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
        filepath = "/home/panda/panda/src/panda_video/Video/03-3_Right_Plastic.mp4"
        self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filepath)))
        self.playButton.setEnabled(True)
        openAction.triggered.connect(self.openFile)
        self.mediaPlayer.setPlaybackRate(1.0)
        # self.mediaPlayer.play()

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
        # self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
      



    def openFile(self):
        print("openfile")
        fileName, _ = QFileDialog.getOpenFileName(self, "default_screen.mp4",
                QDir.homePath())
        print(fileName)

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        print("openfile end")

    def exitCall(self):
        print("end video")
        # self.mediaPlayer.play()
        # self.parent().stack.setCurrentIndex(4)
        # sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged7(self, state):
        print("enter mediastatechagned")
        print(self.mediaPlayer.mediaStatus())
        rospy.loginfo('mediaStatus6 %s', self.mediaPlayer.mediaStatus())

        if(self.mediaPlayer.mediaStatus() == 7):
            self.mediaPlayer.stop()
            msg = "endvideo"
            self.pub.publish(msg)
            rospy.loginfo('I published video')
            
           

            

        else: 
            self.mediaPlayer.play()
            
        

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def callback(self, data):
        if(data.data =="putcup1"):
            self.mediaPlayer.play()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.mediaPlayer.stateChanged.connect(self.mediaStateChanged7)

        elif(data.data=="plastic"):
            self.parent().stack.setCurrentIndex(12)
        elif(data.data=="paper"):
            self.parent().stack.setCurrentIndex(13)
        else:
            pass

        
        

    def listener(self):
        rospy.Subscriber('TerminalToPyqt', String, self.callback)

  

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

class videowindow8(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(videowindow8, self).__init__(parent)
        self.resize(1920,1080)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 
       
        self.listener()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)

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
        filepath = "/home/panda/panda/src/panda_video/Video/03-3_Right_Plastic.mp4"
        self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filepath)))
        self.playButton.setEnabled(True)
        openAction.triggered.connect(self.openFile)
        self.mediaPlayer.setPlaybackRate(1.0)
        # self.mediaPlayer.play()

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
        # self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
     



    def openFile(self):
        print("openfile")
        fileName, _ = QFileDialog.getOpenFileName(self, "default_screen.mp4",
                QDir.homePath())
        print(fileName)

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        print("openfile end")

    def exitCall(self):
        print("end video")
        # self.mediaPlayer.play()
        # self.parent().stack.setCurrentIndex(4)
        # sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged8(self, state):
        print("enter mediastatechagned")
        print(self.mediaPlayer.mediaStatus())
        rospy.loginfo('mediaStatus6 %s', self.mediaPlayer.mediaStatus())

        if(self.mediaPlayer.mediaStatus() == 7):
            self.mediaPlayer.stop()
            self.parent().stack.setCurrentIndex(7)


        else: 
            self.mediaPlayer.play()
            
        

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def callback(self, data):
        if(data.data =="pla1"):
            self.mediaPlayer.play()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.mediaPlayer.stateChanged.connect(self.mediaStateChanged8)
        else:
            pass

        
        

    def listener(self):
        rospy.Subscriber('TerminalToPyqt', String, self.callback)

  

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

class videowindow9(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super(videowindow9, self).__init__(parent)
        self.resize(1920,1080)
        self.setWindowTitle("PyQt Video Player Widget Example - pythonprogramminglanguage.com") 
       
        self.listener()
        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        videoWidget = QVideoWidget()

        self.playButton = QPushButton()
        self.playButton.setEnabled(False)
        self.playButton.setIcon(self.style().standardIcon(QStyle.SP_MediaPlay))
        self.playButton.clicked.connect(self.play)
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)

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
        filepath = "/home/panda/panda/src/panda_video/Video/03-4_Left_Paper.mp4"
        self.mediaPlayer.setMedia(
                QMediaContent(QUrl.fromLocalFile(filepath)))
        self.playButton.setEnabled(True)
        openAction.triggered.connect(self.openFile)
        self.mediaPlayer.setPlaybackRate(1.0)
        # self.mediaPlayer.play()

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
        # self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)
        self.mediaPlayer.error.connect(self.handleError)
      



    def openFile(self):
        print("openfile")
        fileName, _ = QFileDialog.getOpenFileName(self, "default_screen.mp4",
                QDir.homePath())
        print(fileName)

        if fileName != '':
            self.mediaPlayer.setMedia(
                    QMediaContent(QUrl.fromLocalFile(fileName)))
            self.playButton.setEnabled(True)
        print("openfile end")

    def exitCall(self):
        print("end video")
        # self.mediaPlayer.play()
        # self.parent().stack.setCurrentIndex(4)
        # sys.exit(app.exec_())

    def play(self):
        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.mediaPlayer.pause()
        else:
            self.mediaPlayer.play()

    def mediaStateChanged9(self, state):
        print("enter mediastatechagned")
        print(self.mediaPlayer.mediaStatus())
        rospy.loginfo('mediaStatus6 %s', self.mediaPlayer.mediaStatus())

        if(self.mediaPlayer.mediaStatus() == 7):
            self.mediaPlayer.stop()
            self.parent().stack.setCurrentIndex(7)

        else: 
            self.mediaPlayer.play()
            
        

        if self.mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPause))
        else:
            self.playButton.setIcon(
                    self.style().standardIcon(QStyle.SP_MediaPlay))

    def callback(self, data):
        if(data.data =="pap1"):
            self.mediaPlayer.play()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.mediaPlayer.stateChanged.connect(self.mediaStateChanged9)
        else:
            pass

        
        

    def listener(self):
        rospy.Subscriber('TerminalToPyqt', String, self.callback)

  

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
class MyWindow2(QtWidgets.QMainWindow):
    text_update = pyqtSignal(str)
    # Create main window
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.resize(1920,1080)
        
        self.listener()
        self.central = QWidget(self)
        # self.textbox = QTextEdit(self.central)
        # self.textbox.setFont(TEXT_FONT)
        # self.textbox.setMinimumSize(300, 100)
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)

        self.bridge=CvBridge()

        self.image_sub = rospy.Subscriber("/camera/color/image_raw",Image,self.img_callback)

        # self.cv_image=bridge.imgmsg_to_cv2(image_message,desired_encoding='passthrough')
        # self.image_message=bridge.cv2_to_imgmsg(cv_image,encoding='passthrough')
        # self.text_update.connect(self.append_text)
        sys.stdout = self

        self.vlayout = QVBoxLayout()        # Window layout
        self.displays = QHBoxLayout()
        self.disp = ImageWidget(self)    
        self.displays.addWidget(self.disp)
        self.vlayout.addLayout(self.displays)
        self.label = QLabel(self)
        self.vlayout.addWidget(self.label)
        # self.vlayout.addWidget(self.textbox)
        self.central.setLayout(self.vlayout)
        self.setCentralWidget(self.central)
        # self.mask = cv2.imread("/home/panda/panda/src/panda_video/Screen/transparent_dot.png")
        # self.mask = cv2.cvtColor(self.mask, cv2.COLOR_BGR2RGB)
        self.fg = cv2.imread("/home/panda/panda/src/panda_video/Screen/transparent_only.png",cv2.IMREAD_UNCHANGED)
        # _,self.mask = cv2.threshold(self.fg[:,:,3],1,255,cv2.THRESH_BINARY)
        # self.mask_INV = cv2.bitwise_not(self.mask)

        # self.fg = cv2.cvtColor(self.fg,cv2.COLOR_BGRA2RGB)
        # self.gray_mask = cv2.cvtColor(self.mask,cv2.COLOR_BGR2GRAY)
        # _,self.mask_inv = cv2.threshold(self.gray_mask,10,255,cv2.THRESH_BINARY_INV)
        
        # self.mainMenu = self.menuBar()      # Menu bar
        # exitAction = QAction('&Exit', self)
        # exitAction.setShortcut('Ctrl+Q')
        # exitAction.triggered.connect(self.close)
        # self.fileMenu = self.mainMenu.addMenu('&File')
        # self.fileMenu.addAction(exitAction)
   
        self.start()

    # Start image capture & display
    def start(self):
        self.timer = QTimer(self)           # Timer to trigger display
        self.timer.timeout.connect(lambda: 
                    self.show_image(image_queue, self.disp, DISP_SCALE))
        self.timer.start(DISP_MSEC)         
        self.capture_thread = threading.Thread(target=grab_images, 
                    args=(camera_num, image_queue))
        self.capture_thread.start()         # Thread to grab images

    # Fetch camera image from queue, and display it
    def show_image(self, imageq, display, scale):
        if not imageq.empty():
            image = imageq.get()
            if image is not None and len(image) > 0:
                img = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                img = cv2.flip(img,1)
                #img = cv2.add(img,self.mask)
                self.display_image(img, display, scale)

    # Display an image, reduce size if required
    def display_image(self, img, display, scale=1):

        # disp_size = img.shape[1]//scale, img.shape[0]//scale
        disp_size = 1920,1080
        disp_size_1 = 1900,1000
        disp_bpl = disp_size[0] * 3

        if scale > 1:
            img = cv2.resize(img, disp_size, 
                             interpolation=cv2.INTER_CUBIC)
            fg = cv2.resize(self.fg,disp_size_1)

            _,mask = cv2.threshold(fg[:,:,3],1,255,cv2.THRESH_BINARY)
            mask_INV = cv2.bitwise_not(mask)

            fg = cv2.cvtColor(fg,cv2.COLOR_BGRA2RGB)

            h,w = fg.shape[:2]
            roi = img[0:h,0:w]

            masked_fg = cv2.bitwise_and(fg,fg,mask = mask)
            masked_img = cv2.bitwise_and(roi,roi,mask=mask_INV)

            added = masked_fg + masked_img
            img[0:h,0:w] = added

            # img_height, img_width,_=img.shape
            # mask_height, mask_width,_=self.mask.shape
            # y = (img_height-mask_height)//2
            # x = (img_width-mask_width)//2

            # roi = img[y:y+mask_height,x:x+mask_width]
            # rospy.loginfo(roi)

            # ROI_mask = cv2.add(self.mask,roi,mask=self.mask_inv)
            # img = cv2.add(ROI_mask,self.mask)

            #img = cv2.add(img,self.mask)
            #img = img + self.RGB_mask
        qimg = QImage(img.data, disp_size[0], disp_size[1], 
                      disp_bpl, IMG_FORMAT)
        display.setImage(qimg)

    # Handle sys.stdout.write: update text display
    def write(self, text):
        self.text_update.emit(str(text))
    def flush(self):
        pass

    # Append to text display
    def append_text(self, text):
        cur = self.textbox.textCursor()     # Move cursor to end of text
        cur.movePosition(QTextCursor.End) 
        s = str(text)
        while s:
            head,sep,s = s.partition("\n")  # Split line at LF
            cur.insertText(head)            # Insert text at cursor
            if sep:                         # New line if LF
                cur.insertBlock()
        self.textbox.setTextCursor(cur)     # Update visible cursor

    # Window is closing: stop video capture
    def closeEvent(self, event):
        global capturing
        capturing = False
        self.capture_thread.join()
    
    def img_callback(self, data):
        print("img test")
        try:
            image=self.bridge.imgmsg_to_cv2(data,"bgr8")
        except CvBridgeError as e:
            print(e)
        if image is not None and image_queue.qsize() < 2:
                image_queue.put(image)

    def callback(self, data) : 
        if(data.data == "plastic"):
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.parent().stack.setCurrentIndex(12)

            msg = "pla"
            self.pub.publish(msg)
            rospy.loginfo('I published pla')

        elif(data.data=="paper"):
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)
            self.parent().stack.setCurrentIndex(13)

            msg = "pap"
            self.pub.publish(msg)
            rospy.loginfo('I published pap')

    def listener(self):
        
        rospy.Subscriber('TerminalToPyqt', String, self.callback)

 
        


      






    # def stack_reset(self):
    #     self.parent().stack.setCurrentIndex(2)






class FirstWidget(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # self.setStyleSheet(MAIN_COLOR)
        self.resize(1920,1080)
        self.listener()
        # rospy.spin()
        # layout = QtWidgets.QVBoxLayout(self)
        
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)
        
   
        layout = QtWidgets.QVBoxLayout(self)
        self.label=QtWidgets.QLabel(self)
        self.label.resize(1920,1080)  
        pixmap=QPixmap("/home/panda/panda/src/panda_video/Screen/Select_help.png")
        self.label.setPixmap(QPixmap(pixmap))

        self.label.setPixmap(QPixmap(pixmap))
        self.label.resize(pixmap.width(),pixmap.height())  
        

        
        self.button = QtWidgets.QPushButton("응 좋아!", self)
        self.button.setStyleSheet("color : white;""background : #ce9945;" "border:1px solid;" "border-width :5px;" "border-radius : 20px;" "border-color:#a9711a")
        self.button.setGeometry(120,400,750,450)
        self.button.setFont(QFont('NanumBarunpen',170))
    
        self.button2 = QtWidgets.QPushButton("미안해..", self)
        self.button2.setStyleSheet("color : white;""background : #ce9945;" "border:1px solid;" "border-width :5px;" "border-radius : 20px;" "border-color:#a9711a")
        self.button2.setGeometry(1050,400,750,450)
        self.button2.setFont(QFont('NanumBarunpen',170))


        self.button.clicked.connect(self.change_stack)
        self.button2.clicked.connect(self.stack_reset1)

        self.text = QtWidgets.QTextEdit
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.button2) 
        self.showFullScreen()

    # ros 메세지 받는 부분
    def callback(self, data):
        if(data.data == "p"):
            self.stack_reset1()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

    def listener(self):
       
        rospy.Subscriber('/panda/ui/contrl', String, self.callback)

    def change_stack(self):
        self.parent().stack.setCurrentIndex(3)
        msg = "2"
        self.pub.publish(msg)
        rospy.loginfo('I published 2')



    def stack_reset1(self):
        self.parent().stack.setCurrentIndex(10)
        msg="lastvideo2"
        self.pub.publish(msg)
        rospy.loginfo("I published 7")

    

class FirstWidget2(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(1920,1080)
        # self.setStyleSheet(MAIN_COLOR)
        self.listener()
        # layout = QtWidgets.QVBoxLayout(self)
       
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)
        
        
       
        layout = QtWidgets.QVBoxLayout(self)
        self.label=QtWidgets.QLabel(self)
        self.label.resize(1920,1080)  
        pixmap=QPixmap("/home/panda/panda/src/panda_video/Screen/Select_cup.png")
        self.label.setPixmap(QPixmap(pixmap))

        self.label.setPixmap(QPixmap(pixmap))
        self.label.resize(pixmap.width(),pixmap.height())  
        

        
        self.button = QtWidgets.QPushButton("응 있어!", self)

        self.button.setStyleSheet("color : white;""background : #ce9945;" "border:1px solid;" "border-width :5px;" "border-radius : 20px;" "border-color:#a9711a")
        self.button.setGeometry(120,400,750,450)
        self.button.setFont(QFont('NanumBarunpen',170))
        self.button.clicked.connect(self.change_stack)
    
        self.button2 = QtWidgets.QPushButton("아니 없어!", self)
        self.button2.setStyleSheet("color : white;""background : #ce9945;" "border:1px solid;" "border-width :5px;" "border-radius : 20px;" "border-color:#a9711a")
        self.button2.setGeometry(1050,400,750,450)
        self.button2.setFont(QFont('NanumBarunpen',150))
        self.button2.clicked.connect(self.stack_reset)



        self.text = QtWidgets.QTextEdit
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        self.showFullScreen()

    # ros 메세지 받는 부분
    def callback(self, data):
        if(data.data == "p"):
            self.stack_reset1()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

    def listener(self):
       
        rospy.Subscriber('/panda/ui/contrl', String, self.callback)

    def change_stack(self):
       self.parent().stack.setCurrentIndex(5)
       msg="displaycam"
       self.pub.publish(msg)
       rospy.loginfo('I published displaycam')



    def stack_reset(self):
        self.parent().stack.setCurrentIndex(8)
        msg = "nocup"
        self.pub.publish(msg)
        rospy.loginfo('I published nocup')

class Donation1(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(1920,1080)
        # self.setStyleSheet(MAIN_COLOR)
        self.listener()
        # rospy.spin()
        layout = QtWidgets.QVBoxLayout(self)
        # layout = QtWidgets.QHBoxLayout(self)
        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)
        
        
        
        self.label=QtWidgets.QLabel(self)
        self.label.resize(1920,1080)  
        pixmap=QPixmap("/home/panda/panda/src/panda_video/Screen/QR_screen.png")
        self.label.setPixmap(QPixmap(pixmap))

        self.button = QtWidgets.QPushButton("완료!", self)
        self.button.setGeometry(1500,150,300,150)
        self.button.setFont(QFont('NanumBarunpen',70))
        self.button.setStyleSheet("color : white;""background : #ce9945;" "border:1px solid;" "border-width :5px;" "border-radius : 20px;" "border-color:#a9711a")
        self.button.clicked.connect(self.change_stack)

        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.showFullScreen()
    
    # ros 메세지 받는 부분
    def callback(self, data):
        if(data.data == "p"):
            self.stack_reset1()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

    def listener(self):
       
        rospy.Subscriber('TerminalToPyqt', String, self.callback)

    def change_stack(self):
        self.parent().stack.setCurrentIndex(8)
        msg = "4"
        self.pub.publish(msg)
        rospy.loginfo('I published 4')


class FirstWidget3(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.resize(1920,1080)
        # self.setStyleSheet(MAIN_COLOR)
        self.listener()
        # rospy.spin()
        layout = QtWidgets.QVBoxLayout(self)

        self.pub = rospy.Publisher('TerminalToPyqt1', String, queue_size=10)
        
    
  
        self.label=QtWidgets.QLabel(self)
        self.label.resize(1920,1080)  
        pixmap=QPixmap("/home/panda/panda/src/panda_video/Screen/Select_donation.png")
        self.label.setPixmap(QPixmap(pixmap))

        self.label.setPixmap(QPixmap(pixmap))
        self.label.resize(pixmap.width(),pixmap.height())  
        

        
        self.button = QtWidgets.QPushButton("응 좋아!", self)
        self.button.setStyleSheet("color : white;""background : #ce9945;" "border:1px solid;" "border-width :5px;" "border-radius : 20px;" "border-color:#a9711a")
        self.button.setGeometry(120,550,750,400)
        self.button.setFont(QFont('NanumBarunpen',170))
        self.button.clicked.connect(self.change_stack)
    
                

        self.button2 = QtWidgets.QPushButton("미안해..", self)
        self.button2.setStyleSheet("color : white;""background : #ce9945;" "border:1px solid;" "border-width :5px;" "border-radius : 20px;" "border-color:#a9711a")
        self.button2.setGeometry(1050,550,750,400)
        self.button2.setFont(QFont('NanumBarunpen',170))
        self.button2.clicked.connect(self.stack_reset)


        self.text = QtWidgets.QTextEdit
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        layout.addWidget(self.button2)
        self.resize(1920,1080)

    # ros 메세지 받는 부분
    def callback(self, data):
        if(data.data == "p"):
            self.stack_reset()
            rospy.loginfo(rospy.get_caller_id() + 'I heard %s', data.data)

    def listener(self):
       
        rospy.Subscriber('TerminalToPyqt', String, self.callback)

    def change_stack(self):
        self.parent().stack.setCurrentIndex(9)

    def stack_reset(self):
        self.parent().stack.setCurrentIndex(10)
        msg = "donation"
        self.pub.publish(msg)
        rospy.loginfo('I published donation')


   


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

        # self.stack0 = MyWindow2(self)
        # self.stack1 = FirstWidget(self)
        # self.stack2 = videowindow(self)
        # self.stack3 = Thankyou(self)
        # self.stack4 = Donation(self)
        # print(self.stack2)

        self.stack0 = videowindow(self)
        self.stack1 = videowindow2(self)
        self.stack2 = FirstWidget(self)
        self.stack3 = videowindow3(self)
        self.stack4 = FirstWidget2(self)
        self.stack5 = MyWindow2(self)
        self.stack6 = videowindow4(self)
        self.stack7 = FirstWidget3(self)
        self.stack8 = videowindow5(self)
        self.stack9 = Donation1(self)
        self.stack10 = videowindow6(self)
        self.stack11 = videowindow7(self)
        self.stack12 = videowindow8(self)
        self.stack13 = videowindow9(self)


        
        
        self.stack.addWidget(self.stack0)
        self.stack.addWidget(self.stack1)
        self.stack.addWidget(self.stack2)
        self.stack.addWidget(self.stack3)
        self.stack.addWidget(self.stack4)
        self.stack.addWidget(self.stack5)
        self.stack.addWidget(self.stack6)
        self.stack.addWidget(self.stack7)
        self.stack.addWidget(self.stack8)
        self.stack.addWidget(self.stack9)
        self.stack.addWidget(self.stack10)
        self.stack.addWidget(self.stack11)
        self.stack.addWidget(self.stack12)
        self.stack.addWidget(self.stack13)


        self.show()

# app = QApplication(sys.argv)
# player = videowindow()
# player.resize(1240, 980)
# # player.showFullScreen()
# player.show()
rospy.init_node('pyqt', anonymous=True)
app = QtWidgets.QApplication([])
main = MainWindow()
main.resize(1280, 880)
#main.showFullScreen()
app.exec()