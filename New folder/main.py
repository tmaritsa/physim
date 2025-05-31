import sys
from PyQt5.uic import loadUi
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog,QApplication,QMainWindow,QLineEdit,QMessageBox

class MainWindow(QDialog) :
    def __init__(self):
        super(MainWindow,self).__init__()
        loadUi("login.ui",self)
        self.btn1.clicked.connect(self.gomenu)
    def gomenu(self): 
        if self.nim.text() == "H1A024xxx" and self.pw.text() == "kel20": 
            screen2 = Menu()
            widget.addWidget(screen2)
            widget.setCurrentWidget(screen2)
        else:
            QMessageBox.warning(self, "Login Failed", "NIM atau password salah.")

class Menu(QMainWindow) :
    def __init__(self):
        super(Menu,self).__init__()
        loadUi("screen2.ui",self)
        self.btn1.clicked.connect(self.go3)
        self.btn2.clicked.connect(self.go4)
    def go3(self): 
            screen3=sim1()
            widget.addWidget(screen3)
            widget.setCurrentWidget(screen3)
    def go4(self): 
            screen4=sim2()
            widget.addWidget(screen4)
            widget.setCurrentWidget(screen4)
class sim1(QMainWindow) :
    def __init__(self):
        super(sim1,self).__init__()
        loadUi("screen3.ui",self)
class sim2(QMainWindow) :
    def __init__(self):
        super(sim2,self).__init__()
        loadUi("screen4.ui",self)

app = QApplication(sys.argv)
widget=QtWidgets.QStackedWidget()
screen1=MainWindow()
widget.addWidget(screen1)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exit")