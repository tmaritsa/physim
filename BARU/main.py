import sys
import pygame
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt


from login_screen import Login

if __name__ == "__main__":
    pygame.init() 
    pygame.font.init()  

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    login_window = Login()
    login_window.show()
    sys.exit(app.exec_())
