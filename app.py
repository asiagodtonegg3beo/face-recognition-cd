from PyQt5 import QtCore, QtGui, QtWidgets
import sys
from frist import Ui_MainWindow
if __name__ == '__main__':  
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow) 
    MainWindow.show()
    exit(app.exec_()) 
