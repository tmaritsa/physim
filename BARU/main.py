import sys
import pygame
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt

# Import modularized components
from login_screen import Login

if __name__ == "__main__":
    pygame.init()  # Initialize Pygame modules
    pygame.font.init()  # Initialize Pygame font module

    app = QApplication(sys.argv)
    # Enable high DPI scaling and pixmaps for better appearance on high-resolution screens
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)

    login_window = Login()
    login_window.show()
    sys.exit(app.exec_())
