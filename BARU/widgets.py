# widgets.py

import pygame
from PyQt5.QtWidgets import QLabel, QWidget, QVBoxLayout, QApplication, QSizePolicy # FIX: Added QSizePolicy
from PyQt5.QtGui import QPixmap, QImage, QFont, QFontMetrics
from PyQt5.QtCore import Qt, QSize

class PygameEmbedWidget(QLabel):
    """
    A QLabel subclass that embeds a Pygame surface.
    The size of this widget will be controlled by its parent layout.
    """
    def __init__(self, simulation, parent=None):
        super().__init__(parent)
        self.simulation = simulation
        # Initial size will be set by the parent GL class based on window size
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding) # Allow it to expand

    def update_display(self):
        """
        Updates the QLabel's pixmap with the current Pygame surface.
        """
        surface = self.simulation.surface
        if surface: # Ensure surface exists before trying to convert
            raw_str = pygame.image.tostring(surface, "RGBA")
            qimage = QImage(raw_str, surface.get_width(), surface.get_height(), QImage.Format_RGBA8888)
            # Scale pixmap to fit the current QLabel size
            self.setPixmap(QPixmap.fromImage(qimage).scaled(self.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))

class ShadowedTitle(QWidget):
    """
    A custom widget to display a title with a shadowed effect.
    The size and font will now attempt to scale dynamically.
    """
    def __init__(self, title, parent=None):
        super().__init__(parent)
        self._title = title
        self._font_size = 48 # Base font size
        self._padding = 12 # Base padding

        self.shadow1 = QLabel(title, self)
        self.shadow1.setStyleSheet("color: #93c5fd;")
        self.shadow1.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.shadow2 = QLabel(title, self)
        self.shadow2.setStyleSheet("color: #1e40af;")
        self.shadow2.setAttribute(Qt.WA_TransparentForMouseEvents)

        self.main_text = QLabel(title, self)
        self.main_text.setStyleSheet("color: white;")
        self.main_text.setAttribute(Qt.WA_TransparentForMouseEvents)

        # Initially set font and size, will be updated on resize
        self._update_sizes()

    def _update_sizes(self):
        """Updates font and widget size based on current font metrics."""
        # Get font size relative to parent (or a reasonable default if no parent)
        # If no parent, use QApplication's default font size.
        base_font_size = QApplication.font().pointSize()
        if self.parent():
            # Attempt to scale based on parent's initial height for more consistent scaling
            # This is a heuristic and might need fine-tuning
            parent_height = self.parent().height()
            if parent_height > 0:
                base_font_size = int(base_font_size * (parent_height / 600)) # Assuming 600 is a base height
        
        current_font_size = int(self._font_size * (base_font_size / 12)) # Scale font size relative to a 12pt base
        current_font_size = max(24, current_font_size) # Ensure minimum readable font size

        font = QFont("Sans Serif", current_font_size, QFont.ExtraBold)
        fm = QFontMetrics(font)
        text_width = fm.horizontalAdvance(self._title)
        text_height = fm.height()

        scaled_padding = int(self._padding * (base_font_size / 12)) # Scale padding
        scaled_padding = max(6, scaled_padding) # Ensure minimum padding

        # Adjust font for all labels
        self.shadow1.setFont(font)
        self.shadow2.setFont(font)
        self.main_text.setFont(font)

        # Adjust position
        self.shadow1.move(scaled_padding + 6, scaled_padding + 6)
        self.shadow2.move(scaled_padding + 3, scaled_padding + 3)
        self.main_text.move(scaled_padding, scaled_padding)

        # Set fixed size for the container based on scaled text size + padding
        self.setFixedSize(text_width + scaled_padding * 2 + 6, text_height + scaled_padding * 2 + 6)

    def resizeEvent(self, event):
        """Handle resize events to update sizes."""
        super().resizeEvent(event)
        self._update_sizes() # Recalculate and apply sizes
