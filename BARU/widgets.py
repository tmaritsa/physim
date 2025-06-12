# widgets.py

import pygame
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QApplication, QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QSize

class PygameEmbedWidget(QLabel):
   
    def __init__(self, simulation, parent=None):
        super().__init__(parent)
        self.simulation = simulation
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def update_display(self):
       
        surface = self.simulation.surface
        if surface:
            raw_str = pygame.image.tostring(surface, "RGBA")
            qimage = QImage(raw_str, surface.get_width(), surface.get_height(), QImage.Format_RGBA8888)
            
            self.setPixmap(QPixmap.fromImage(qimage).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

class ShadowedTitle(QWidget):
    
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self._title = title
        self._font_size = 48 
        self._padding = 12 

        self.shadow1 = QLabel(title, self)
        self.shadow1.setStyleSheet("color: #93c5fd;")
        self.shadow1.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.shadow2 = QLabel(title, self)
        self.shadow2.setStyleSheet("color: #1e40af;")
        self.shadow2.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.main_text = QLabel(title, self)
        self.main_text.setStyleSheet("color: white;")
        self.main_text.setAttribute(Qt.WA_TransparentForMouseEvents)

        
        self._update_sizes()

    def _update_sizes(self):
        
        base_font_size = QApplication.font().pointSize()
        if self.parent():
            
            parent_height = self.parent().height()
            if parent_height > 0:
                base_font_size = int(base_font_size * (parent_height / 600)) 
        
        current_font_size = int(self._font_size * (base_font_size / 12))
        current_font_size = max(24, current_font_size) 

        font = QFont("Sans Serif", current_font_size, QFont.ExtraBold)
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(self._title)
        text_height = fm.height()

        scaled_padding = int(self._padding * (base_font_size / 12)) 
        scaled_padding = max(6, scaled_padding) 

        self.shadow1.setFont(font)
        self.shadow2.setFont(font)
        self.main_text.setFont(font)

    
        self.shadow1.move(scaled_padding + 6, scaled_padding + 6)
        self.shadow2.move(scaled_padding + 3, scaled_padding + 3)
        self.main_text.move(scaled_padding, scaled_padding)

        
        self.setFixedSize(text_width + scaled_padding * 2 + 6, text_height + scaled_padding * 2 + 6)

    def resizeEvent(self, event):
    
        super().resizeEvent(event)
        self._update_sizes() 
