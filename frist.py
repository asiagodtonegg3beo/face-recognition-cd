# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'test.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import pyqtSlot
import os
import imp
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(448, 435)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.namebuilder = QtWidgets.QPushButton(self.centralwidget)
        self.namebuilder.setGeometry(QtCore.QRect(11, 40, 421, 28))
        self.namebuilder.setObjectName("namebuilder")
        
        self.dataset = QtWidgets.QPushButton(self.centralwidget)
        self.dataset.setGeometry(QtCore.QRect(11, 100, 421, 28))
        self.dataset.setObjectName("dataset")
        
        self.embeddings = QtWidgets.QPushButton(self.centralwidget)
        self.embeddings.setGeometry(QtCore.QRect(11, 160, 421, 28))
        self.embeddings.setObjectName("embeddings")
        
        
        self.training = QtWidgets.QPushButton(self.centralwidget)
        self.training.setGeometry(QtCore.QRect(11, 220, 421, 28))
        self.training.setObjectName("training")
        
        self.recognition = QtWidgets.QPushButton(self.centralwidget)
        self.recognition.setGeometry(QtCore.QRect(11,280, 421, 28))
        self.recognition.setObjectName("recognition")
        
        self.toolButton = QtWidgets.QToolButton(self.centralwidget)
        self.toolButton.setGeometry(QtCore.QRect(400, 320, 27, 21))
        self.toolButton.setObjectName("toolButton")
        
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 448, 25))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        
        self.namebuilder.clicked.connect(lambda :self.fn(1))
        
        self.dataset.clicked.connect(lambda :self.fn(2))
        
        self.embeddings.clicked.connect(lambda :self.fn(3))

        self.training.clicked.connect(lambda :self.fn(4))

        self.recognition.clicked.connect(lambda :self.fn(5))
        
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
    @pyqtSlot()
    def fn(self,flag):
        if flag==1:
            imp.load_source('a','namebuilder.py')
            flag==0
        if flag==2:
            imp.load_source('b','dataset.py')
            flag==0
        if flag==3:
            imp.load_source('c','extract_embeddings.py')
            flag==0
        if flag==4:
            imp.load_source('d','train_model.py')
            flag==0
        if flag==5:
            imp.load_source('e','recognize_video.py')
            flag==0
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "人臉辨識系統"))
        self.namebuilder.setText(_translate("MainWindow", "名稱建立"))
        self.embeddings.setText(_translate("MainWindow", "描繪特徵點"))
        self.dataset.setText(_translate("MainWindow", "拍照收集資料"))
        self.training.setText(_translate("MainWindow", "訓練"))
        self.recognition.setText(_translate("MainWindow", "辨識"))
        self.toolButton.setText(_translate("MainWindow", "..."))

