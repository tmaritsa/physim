# coba_final_v2.py

import sys
import pygame
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit, QPushButton,
    QMainWindow, QMessageBox, QHBoxLayout, QGridLayout, QAction, QSizePolicy,
    QSlider, QStackedWidget
)
from PyQt5.QtGui import (
    QFont, QPalette, QLinearGradient, QColor, QBrush, QIcon, QPixmap, QImage
)
from PyQt5.QtCore import Qt, QSize, QTimer, pyqtSignal

# Impor kelas simulasi dari file yang telah direvisi
from glbb import GLBBSimulation

class PygameEmbedWidget(QLabel):
    """Widget ini tidak berubah."""
    def __init__(self, simulation, width, height, parent=None):
        super().__init__(parent)
        self.setFixedSize(width, height)
        self.simulation = simulation

    def update_display(self):
        surface = self.simulation.surface
        raw_str = pygame.image.tostring(surface, "RGBA")
        qimage = QImage(raw_str, surface.get_width(), surface.get_height(), QImage.Format_RGBA8888)
        self.setPixmap(QPixmap.fromImage(qimage))


class GLBBSimulationPage(QWidget):
    """Halaman simulasi dengan slider dua arah dan fungsi reset."""
    back_to_menu_requested = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.simulation = GLBBSimulation(width=800, height=400)
        self.pygame_widget = PygameEmbedWidget(self.simulation, 800, 400)
        
        self.slider_label = QLabel(f"Akselerasi: {0.00:.2f} m/s²")
        self.slider_label.setAlignment(Qt.AlignCenter)
        self.slider_label.setFont(QFont("Arial", 12))
        
        self.slider = QSlider(Qt.Horizontal)
        # PERUBAHAN: Range slider sekarang dari -5000 hingga 5000, dengan 0 di tengah
        self.slider.setRange(-5000, 5000)
        self.slider.setValue(0)
        self.slider.valueChanged.connect(self.update_acceleration)
        
        self.back_button = QPushButton("Kembali ke Menu")
        self.back_button.clicked.connect(self.request_back_to_menu)
        
        layout = QVBoxLayout()
        layout.addWidget(self.pygame_widget)
        layout.addWidget(self.slider_label)
        layout.addWidget(self.slider)
        layout.addWidget(self.back_button, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.game_tick)

    def game_tick(self):
        self.simulation.step()
        self.simulation.draw()
        self.pygame_widget.update_display()

    def update_acceleration(self, value):
        # Konversi nilai -5000..5000 menjadi -50.00..50.00
        accel_value = value / 100.0
        self.simulation.set_acceleration(accel_value)
        self.slider_label.setText(f"Akselerasi: {accel_value:.2f} m/s²")

    def request_back_to_menu(self):
        self.back_to_menu_requested.emit()

    def start_simulation(self):
        self.timer.start(1000 // 60)

    def stop_simulation(self):
        self.timer.stop()
        
    def reset(self):
        """
        FUNGSI BARU: Mereset simulasi DAN UI (slider) ke kondisi awal.
        """
        self.simulation.reset()
        self.slider.setValue(0)


class LoginScreen(QWidget):
    # Tidak ada perubahan di kelas ini
    def __init__(self):
        super(LoginScreen, self).__init__()
        self.setWindowTitle("Login")
        self.setMinimumSize(400, 300)
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0.0, QColor("#a2d4f5"))
        gradient.setColorAt(1.0, QColor("#ffffff"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)
        layout = QVBoxLayout()
        logo = QLabel("PhySim")
        logo.setAlignment(Qt.AlignCenter)
        logo_font = QFont("Arial", 48, QFont.Bold)
        logo.setFont(logo_font)
        logo.setMinimumHeight(70)
        logo.setStyleSheet("color: black;")
        layout.addWidget(logo)
        self.nim = QLineEdit()
        self.nim.setPlaceholderText("NIM")
        layout.addWidget(self.nim)
        self.password = QLineEdit()
        self.password.setPlaceholderText("PASSWORD")
        self.password.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password)
        login_btn = QPushButton("LOGIN")
        login_btn.setStyleSheet("background-color: #00aaff; color: white; padding: 6px 12px; border-radius: 6px;")
        login_btn.clicked.connect(self.check_login)
        layout.addWidget(login_btn, alignment=Qt.AlignCenter)
        self.setLayout(layout)
        self.menu_window = None

    def check_login(self):
        if self.nim.text() == "H1A024xxx" and self.password.text() == "kel20":
            self.menu_window = Menu(self)
            self.menu_window.show()
            self.hide()
        else:
            QMessageBox.warning(self, "Login Failed", "NIM atau password salah.")


class Menu(QMainWindow):
    """Jendela utama yang sekarang juga memanggil fungsi reset."""
    def __init__(self, login_window):
        super(Menu, self).__init__()
        self.login_window = login_window
        self.setWindowTitle("PhySim")
        self.resize(820, 700)

        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        self.menu_page = self.create_menu_page()
        self.simulation_page = GLBBSimulationPage()
        
        self.stacked_widget.addWidget(self.menu_page)
        self.stacked_widget.addWidget(self.simulation_page)
        
        self.simulation_page.back_to_menu_requested.connect(self.show_menu_page)

        menubar = self.menuBar()
        account_menu = menubar.addMenu("Account")
        logout_action = QAction("← Logout", self)
        logout_action.triggered.connect(self.handle_logout)
        account_menu.addAction(logout_action)
        
        self.show_menu_page()

    def create_menu_page(self):
        page = QWidget()
        palette = QPalette()
        gradient = QLinearGradient(0, 0, 800, 600)
        gradient.setColorAt(0.0, QColor("#a2d4f5"))
        gradient.setColorAt(1.0, QColor("#ffffff"))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        page.setAutoFillBackground(True)
        main_layout = QVBoxLayout(page)
        
        title_label = QLabel("PILIH MATERI")
        title_font = QFont("Arial", 32, QFont.Bold)
        title_label.setFont(title_font)
        title_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title_label)

        button_grid = QGridLayout()
        simulasi_labels = ["Gerak Lurus", "Hukum Newton", "Hukum Hooke", "Rangkaian Resistor", "Gerak Harmonik", "Hukum Archimedes"]
        for i in range(6):
            btn = QPushButton()
            btn.setMinimumSize(100, 100)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            if i == 0:
                btn.clicked.connect(self.show_simulation_page)
            
            label = QLabel(simulasi_labels[i])
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("color: black; font-weight: bold;")
            
            vbox = QVBoxLayout()
            vbox.addWidget(btn)
            vbox.addWidget(label)
            container = QWidget()
            container.setLayout(vbox)
            button_grid.addWidget(container, i // 3, i % 3)
        main_layout.addLayout(button_grid)
        return page

    def show_menu_page(self):
        """Pindah ke halaman menu, hentikan, dan reset simulasi."""
        self.simulation_page.stop_simulation()
        # PERUBAHAN: Panggil fungsi reset sebelum pindah halaman
        self.simulation_page.reset()
        self.stacked_widget.setCurrentWidget(self.menu_page)

    def show_simulation_page(self):
        """Pindah ke halaman simulasi dan mulai simulasi."""
        self.simulation_page.start_simulation()
        self.stacked_widget.setCurrentWidget(self.simulation_page)

    def handle_logout(self):
        self.login_window.show()
        self.close()

if __name__ == "__main__":
    pygame.init()
    pygame.font.init()

    app = QApplication(sys.argv)
    app.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    app.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    login_window = LoginScreen()
    login_window.show()
    
    sys.exit(app.exec_())