from PyQt5.QtCore import *
import sys
from PyQt5.QtWidgets import *   # 使用此模塊中的QWidget，QTextBrowser、QLineEdit
 # 通過QDialog子類化的方法創建一個頂級窗口
 # PyQt中的所有控件都是繼承自QWidget, 如：QDialog,QLineEdit
fp = open("present.txt", "w")
name = ""
class Form(QDialog):
     def __init__(self):
         super().__init__()   # 初始化窗口
 
         # 創建兩個窗口控件
         self.setGeometry(0, 0, 250, 75)
         self.center()
         self.setWindowTitle('名稱建立工具')
         self.label = QLabel('請輸入您的大名',self)
         self.label.setAlignment(Qt.AlignCenter)
         self.lineedit = QLineEdit()
         self.lineedit.selectAll()
         # 創建一個垂直布局管理器QVBoxLayout
         # PyQt提供了三種布局管理器：垂直布局／水平布局／網格布局，它們可以彼此嵌套。
         # 使用了布局管理器後，各種控件會隨著窗口的大小改變自動調整。
         
         layout = QVBoxLayout()
         layout.addWidget(self.label)
         layout.addWidget(self.lineedit)
         self.lineedit.setPlaceholderText("請輸入英文名或數字")
         self.setLayout(layout)
         self.lineedit.setFocus()
         # 信號（returnPressed）連接到槽（updateUi)
         # 當用戶在lineedit上按下回車鍵時，retrunPressed信號就會發射出來，
         # 因有connect , 此時會調用updateUi().
         self.show()
         self.lineedit.returnPressed.connect(self.input)
         self.lineedit.returnPressed.connect(self.close)
     def input(self):
         try:
             global name
             name = self.lineedit.text()
             fp.write(name)
             fp.close()
             print("[INFO] "+ name +" has been created!")
         except:
             print("[INFO] wrong!")       
    
     def center(self):
         qr = self.frameGeometry()
         cp = QDesktopWidget().availableGeometry().center()
         qr.moveCenter(cp)
         self.move(qr.topLeft())


             
app = QApplication(sys.argv)
form = Form()  # 創建Form實例     # 調用了show()後，事件循環開始，顯示出窗口
exit(app.exec_())
