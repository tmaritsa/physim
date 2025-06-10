# quiz_screen.py

import csv
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QPushButton,
    QAction, QApplication, QSizePolicy, QFrame, QHBoxLayout, QTextEdit, QMessageBox
)
from PyQt5.QtGui import QPalette, QLinearGradient, QColor, QBrush, QFont
from PyQt5.QtCore import Qt

from config import COLOR_BACKGROUND_START, COLOR_BACKGROUND_END, COLOR_BUTTON_START, COLOR_BUTTON_END
from widgets import ShadowedTitle

class Kuis(QMainWindow):
    """
    Quiz screen for the application.
    Elements dynamically resize with the window.
    """
    def __init__(self, menu_window, simulation_type: str = "Umum"): # NEW: Added simulation_type parameter
        super().__init__()
        self.menu_window = menu_window
        self.simulation_type = simulation_type # Store the simulation type
        self.setWindowTitle(f"Kuis: {self.simulation_type}") # Set window title based on simulation type
        self.setWindowIcon(QIcon('atom.png'))

        # Get primary screen geometry for initial sizing
        screen_rect = QApplication.primaryScreen().geometry()
        initial_width = int(screen_rect.width() * 0.7) # 70% of screen width
        initial_height = int(screen_rect.height() * 0.7) # 70% of screen height
        self.resize(initial_width, initial_height)
        self.setMinimumSize(int(initial_width * 0.6), int(initial_height * 0.6)) # Set a flexible minimum size

        # Background gradient
        palette = QPalette()
        gradient = QLinearGradient(0, 0, screen_rect.width(), screen_rect.height())
        gradient.setColorAt(0.0, QColor(COLOR_BACKGROUND_START))
        gradient.setColorAt(1.0, QColor(COLOR_BACKGROUND_END))
        palette.setBrush(QPalette.Window, QBrush(gradient))
        self.setPalette(palette)
        self.setAutoFillBackground(True)

        # Menu bar with Akun and Logout action
        menubar = self.menuBar()
        # Adjust font sizes for menubar
        menubar.setStyleSheet(f"""
            QMenuBar {{
                background-color: #f9f9f9;
                font-weight: 600;
                font-size: {int(1.2 * QApplication.font().pointSize())}px;
                color: #111111;
            }}
            QMenuBar::item {{
                spacing: {int(0.5 * QApplication.font().pointSize())}px;
                padding: {int(0.5 * QApplication.font().pointSize())}px {int(1.0 * QApplication.font().pointSize())}px;
                background: transparent;
                border-radius: 4px;
            }}
            QMenuBar::item:selected {{
                background: #e2e8f0;
            }}
            QMenu {{
                background-color: #f9f9f9;
                border: 1px solid #ddd;
            }}
            QMenu::item:selected {{
                background-color: #cbd5e1;
                color: #111111;
            }}
        """)
        akun_menu = menubar.addMenu("Akun")
        logout_action = QAction("Logout", self)
        akun_menu.addAction(logout_action)
        logout_action.triggered.connect(self.handle_logout)

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        # Dynamic margins and spacing
        main_layout.setContentsMargins(int(initial_width * 0.03), int(initial_height * 0.03), int(initial_width * 0.03), int(initial_height * 0.03))
        main_layout.setSpacing(int(initial_height * 0.04))

        main_layout.addStretch(1) # Add flexible space at top

        container = QWidget()
        container_layout = QVBoxLayout()
        container_layout.setSpacing(int(initial_height * 0.04))
        container_layout.setContentsMargins(0, 0, 0, 0)
        container.setLayout(container_layout)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        try:
            self.title_widget = ShadowedTitle(f"Kuis: {self.simulation_type}", parent=container) # NEW: Update title
        except NameError:
            title_widget = QLabel(f"Kuis: {self.simulation_type}") # NEW: Update title
            title_widget.setFont(QFont("Inter", int(3 * QApplication.font().pointSize()), QFont.Bold))
            title_widget.setStyleSheet("color: #111827;")
            self.title_widget = title_widget # Assign to instance variable
        container_layout.addWidget(self.title_widget, alignment=Qt.AlignHCenter) # Use instance variable

        main_layout.addWidget(container, alignment=Qt.AlignCenter)

        # Text area container styled as a card with subtle rounded corners and background
        self.text_area_container = QFrame()
        self.text_area_container.setStyleSheet("""
            QFrame {
                border: 2px solid #374151;
                border-radius: 12px;
                background-color: #cbd5e1;
            }
        """)
        self.text_area_container.setLayout(QHBoxLayout())
        # Dynamic margins for text area
        self.text_area_container.layout().setContentsMargins(int(initial_width * 0.06), int(initial_height * 0.02), int(initial_width * 0.02), int(initial_height * 0.02))
        self.text_area_container.layout().setSpacing(0)
        self.text_area_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)


        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet(f"background-color: transparent; border: none; font-size: {int(1.5 * QApplication.font().pointSize())}px; color: black; padding-left: 0px; resize: none;")
        self.text_edit.setReadOnly(True)
        self.text_edit.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.text_area_container.layout().addWidget(self.text_edit)

        self.number_circle = QLabel("1", self.text_area_container)
        # Initial size of number circle, will be scaled in resizeEvent
        circle_size = int(min(initial_width, initial_height) * 0.05)
        self.number_circle.setFixedSize(circle_size, circle_size)
        self.number_circle.setStyleSheet(f"""
            background-color: #a9a9a9;
            border-radius: {int(circle_size / 2)}px;
            font-weight: bold;
            font-size: {int(1.3 * QApplication.font().pointSize())}px;
            color: black;
        """)

        # Corrected initial position for number_circle
        # We want it to be at the top-left corner of the QFrame's *visual border area*
        # This means slightly offset from (0,0) of the parent (text_area_container)
        # A small positive offset brings it slightly into the container's area,
        # preventing it from being fully cropped.
        # The exact values might need fine-tuning based on your QFrame's border width.
        # Let's try an offset based on a small percentage of the circle size.
        offset = circle_size * 0.1 # A 10% offset, adjust as needed
        self.number_circle.move(int(-offset), int(-offset)) # Move slightly inwards from the perfect corner
        self.number_circle.raise_()

        main_layout.addWidget(self.text_area_container, alignment=Qt.AlignHCenter)

        # Buttons for choices
        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setSpacing(int(initial_height * 0.025))
        self.buttons_layout.setContentsMargins(0, 0, 0, 0)

        # Dynamic font size and padding for choice buttons
        choice_button_font_size = int(1.4 * QApplication.font().pointSize())
        choice_button_padding_v = int(1.0 * QApplication.font().pointSize())
        min_choice_button_height = int(initial_height * 0.07) # Dynamic min height

        self.choice_buttons = []
        for i in range(1, 5):
            btn = QPushButton(f"Pilihan {i}")
            btn.setObjectName(f"ChoiceButton_{i}") # Set unique object name for each choice button
            btn.setFont(QFont("Sans Serif", choice_button_font_size, QFont.ExtraBold))
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #cbd5e1;
                    border: 2px solid #374151;
                    border-radius: 20px;
                    color: black;
                    padding: {choice_button_padding_v}px 0;
                    min-width: 80px;
                }}
                QPushButton:hover {{
                    background-color: #94a3b8;
                }}
            """)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
            btn.setMinimumHeight(min_choice_button_height)
            btn.clicked.connect(lambda checked, b=btn: self.check_answer(b))
            self.buttons_layout.addWidget(btn)
            self.choice_buttons.append(btn)

        buttons_container = QWidget()
        buttons_container.setLayout(self.buttons_layout)
        buttons_container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        main_layout.addWidget(buttons_container, alignment=Qt.AlignCenter)

        # Next button styled dynamically
        next_button_font_size = int(1.5 * QApplication.font().pointSize())
        next_button_padding_v = int(1.0 * QApplication.font().pointSize())
        next_button_padding_h = int(2.0 * QApplication.font().pointSize())
        min_next_button_width = int(initial_width * 0.2)
        min_next_button_height = int(initial_height * 0.07)

        self.next_button = QPushButton("Next", self)
        self.next_button.setObjectName("NextButton") # Set object name
        self.next_button.setFont(QFont("Sans Serif", next_button_font_size, QFont.ExtraBold))
        self.next_button.setStyleSheet(f"""
            QPushButton {{
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
                color: white;
                font-size: {next_button_font_size}px;
                border: none;
                border-radius: 20px;
                color: white;
                padding: {next_button_padding_v}px {next_button_padding_h}px;
                font-weight: bold;
                min-width: {min_next_button_width}px;
                min-height: {min_next_button_height}px;
                transition: background-color 0.3s ease;
            }}
            QPushButton:hover {{
                background-color: #2563eb;
            }}
        """)
        self.next_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.next_button.clicked.connect(self.next_question)
        main_layout.addWidget(self.next_button, alignment=Qt.AlignCenter)
        self.next_button.hide()

        # Menu button styled exactly like Next button
        self.menu_button = QPushButton("Menu", self)
        self.menu_button.setObjectName("QuizMenuButton") # Set object name
        self.menu_button.setFont(QFont("Sans Serif", next_button_font_size, QFont.ExtraBold))
        self.menu_button.setStyleSheet(self.next_button.styleSheet())
        self.menu_button.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.menu_button.clicked.connect(self.back_to_menu)
        main_layout.addWidget(self.menu_button, alignment=Qt.AlignCenter)
        self.menu_button.hide()

        main_layout.addStretch(1) # Add flexible space at bottom

        # Load questions from CSV based on simulation type
        self.questions = self.load_questions_for_type(self.simulation_type) # NEW: Call new loading function
        self.current_question_index = 0
        self.display_question()

    def load_questions_for_type(self, sim_type: str): # NEW: Function to load specific quiz files
        """
        Loads quiz questions from a CSV file based on the simulation type.
        Maps simulation_type string to a specific CSV file name.
        """
        file_map = {
            "Gerak Lurus": "soal_gl.csv",
            "Gerak Harmonik": "soal_shm.csv",
            # Add other simulation types and their corresponding quiz files here:
            # "Hukum Newton": "soal_newton.csv",
            # "Hukum Hooke": "soal_hooke.csv",
            # "Rangkaian Resistor": "soal_resistor.csv",
            # "Hukum Archimedes": "soal_archimedes.csv",
        }

        file_name = file_map.get(sim_type, "soal_default.csv") # Fallback to a default if type not found
        file_path = f'source/{file_name}'

        questions = []
        try:
            with open(file_path, mode='r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    questions.append(row)
            if not questions:
                QMessageBox.information(self, "Informasi", f"File soal untuk '{sim_type}' kosong atau tidak memiliki data yang valid. Silakan tambahkan soal ke '{file_name}'.")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"File soal '{file_name}' untuk '{sim_type}' tidak ditemukan di 'source/'. Pastikan file ada.")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Terjadi kesalahan saat membaca soal dari '{file_name}': {e}")
        return questions

    def display_question(self):
        """Displays the current quiz question and its choices."""
        if not self.questions:
            self.text_edit.setPlainText("Tidak ada soal yang tersedia untuk simulasi ini.") # NEW: More specific message
            for btn in self.choice_buttons:
                btn.hide() # Hide buttons if no questions
            self.next_button.hide()
            self.menu_button.show()
            return

        question = self.questions[self.current_question_index]
        self.text_edit.setPlainText(question['soal'])
        self.number_circle.setText(str(self.current_question_index + 1))
        self.choice_buttons[0].setText(question['a'])
        self.choice_buttons[1].setText(question['b'])
        self.choice_buttons[2].setText(question['c'])
        self.choice_buttons[3].setText(question['d'])

        # When displaying a question reset buttons
        current_width = self.width() # Get current width for dynamic padding
        current_height = self.height()
        choice_button_font_size = max(10, int(0.02 * current_height))
        choice_button_padding_v = max(5, int(choice_button_font_size * 0.7))

        for btn in self.choice_buttons:
            btn.setEnabled(True)
            # Reset stylesheet to default for current theme
            btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: #cbd5e1;
                    border: 2px solid #374151;
                    border-radius: 20px;
                    color: black;
                    padding: {choice_button_padding_v}px 0;
                    min-width: 80px;
                }}
                QPushButton:hover {{
                    background-color: #94a3b8;
                }}
            """)

        # Hide both navigation buttons until user answers
        self.next_button.hide()
        self.menu_button.hide()

    def check_answer(self, selected_button):
        """Checks the selected answer and highlights buttons accordingly."""
        # Disable buttons to lock answer
        for btn in self.choice_buttons:
            btn.setEnabled(False)

        question = self.questions[self.current_question_index]
        correct_answer_text = question.get('correct', '').strip()
        selected_text = selected_button.text()

        # Get current width/height for dynamic padding when applying styles
        current_width = self.width()
        current_height = self.height()
        choice_button_font_size = max(10, int(0.02 * current_height))
        choice_button_padding_v = max(5, int(choice_button_font_size * 0.7))

        # Highlight buttons according to correctness
        for btn in self.choice_buttons:
            if btn.text() == correct_answer_text:
                # Correct answer style - green
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #34d399;
                        border: 2px solid #059669;
                        border-radius: 20px;
                        color: white;
                        padding: {choice_button_padding_v}px 0;
                        min-width: 80px;
                    }}
                """)
            elif btn == selected_button:
                # Wrong answer style - red
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #f87171;
                        border: 2px solid #dc2626;
                        border-radius: 20px;
                        color: white;
                        padding: {choice_button_padding_v}px 0;
                        min-width: 80px;
                    }}
                """)
            else:
                # Other buttons dimmed
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #cbd5e1;
                        border: 2px solid #374151;
                        border-radius: 20px;
                        color: black;
                        padding: {choice_button_padding_v}px 0;
                        opacity: 0.6;
                        min-width: 80px;
                    }}
                """)

        # Show next or menu button after answer
        if self.current_question_index < len(self.questions) - 1:
            self.next_button.show()
            self.menu_button.hide()
        else:
            self.next_button.hide()
            self.menu_button.show()

    def next_question(self):
        """Moves to the next question in the quiz."""
        self.current_question_index += 1
        self.display_question()

    def resizeEvent(self, event):
        """
        Overrides resizeEvent to dynamically adjust element sizes and positions
        in the Kuis screen when the window size changes.
        """
        super().resizeEvent(event)
        current_width = self.width()
        current_height = self.height()

        # Update shadowed title size
        self.title_widget._update_sizes() # Use instance variable

        # Adjust text_area_container minimum height
        self.text_area_container.setMinimumHeight(int(current_height * 0.15))

        # Re-position and re-size number_circle dynamically
        circle_size = int(min(current_width, current_height) * 0.05)
        self.number_circle.setFixedSize(circle_size, circle_size)
        self.number_circle.setAlignment(Qt.AlignCenter)
        self.number_circle.setStyleSheet(f"""
            background-color: #a9a9a9;
            border-radius: {int(circle_size / 2)}px;
            font-weight: bold;
            font-size: {max(12, int(0.02 * circle_size))}px;
            color: black;
        """)
        # Corrected position for number_circle on resize
        offset = circle_size * 0.1 # Consistent offset
        self.number_circle.move(int(-offset), int(-offset))


        # Adjust button fonts and padding on resize for choice buttons
        choice_button_font_size = max(10, int(0.02 * current_height))
        choice_button_padding_v = max(5, int(choice_button_font_size * 0.7))
        min_choice_button_height = max(30, int(current_height * 0.07))

        for i in range(len(self.choice_buttons)):
            btn = self.findChild(QPushButton, f"ChoiceButton_{i+1}")
            if btn:
                btn.setFont(QFont("Sans Serif", choice_button_font_size, QFont.ExtraBold))
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background-color: #cbd5e1;
                        border: 2px solid #374151;
                        border-radius: 20px;
                        color: black;
                        padding: {choice_button_padding_v}px 0;
                        min-width: 80px;
                    }}
                    QPushButton:hover {{
                        background-color: #94a3b8;
                    }}
                """)
                btn.setMinimumHeight(min_choice_button_height)

        # Adjust Next/Menu button fonts and padding on resize
        next_button_font_size = max(12, int(0.025 * current_height))
        next_button_padding_v = max(8, int(next_button_font_size * 0.7))
        next_button_padding_h = max(15, int(next_button_font_size * 1.3))
        min_next_button_width = max(80, int(current_width * 0.2))
        min_next_button_height = max(40, int(current_height * 0.07))

        next_btn = self.findChild(QPushButton, "NextButton")
        menu_btn = self.findChild(QPushButton, "QuizMenuButton")

        if next_btn:
            next_btn.setFont(QFont("Sans Serif", next_button_font_size, QFont.ExtraBold))
            next_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
                    color: white;
                    font-size: {next_button_font_size}px;
                    border: none;
                    border-radius: 20px;
                    color: white;
                    padding: {next_button_padding_v}px {next_button_padding_h}px;
                    font-weight: bold;
                    min-width: {min_next_button_width}px;
                    min-height: {min_next_button_height}px;
                    transition: background-color 0.3s ease;
                }}
                QPushButton:hover {{
                    background-color: #2563eb;
                }}
            """)
        if menu_btn:
            menu_btn.setFont(QFont("Sans Serif", next_button_font_size, QFont.ExtraBold))
            menu_btn.setStyleSheet(f"""
                QPushButton {{
                    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {COLOR_BUTTON_START}, stop:1 {COLOR_BUTTON_END});
                    color: white;
                    font-size: {next_button_font_size}px;
                    border: none;
                    border-radius: 20px;
                    color: white;
                    padding: {next_button_padding_v}px {next_button_padding_h}px;
                    font-weight: bold;
                    min-width: {min_next_button_width}px;
                    min-height: {min_next_button_height}px;
                    transition: background-color 0.3s ease;
                }}
                QPushButton:hover {{
                    background-color: #2563eb;
                }}
            """)


    def back_to_menu(self):
        """Returns to the main menu from the quiz."""
        # self.menu_window here is a GL or Bandul instance
        # The GL/Bandul instance's menu_window is the actual Menu instance
        self.menu_window.menu_window.show() # Show the Menu window
        self.close() # Close the current Kuis window

    def handle_logout(self):
        """Handles logout action from the quiz."""
        # self.menu_window here is a GL or Bandul instance
        # self.menu_window.menu_window is the Menu instance
        # self.menu_window.menu_window.login_window is the Login instance
        self.menu_window.menu_window.login_window.show()
        self.menu_window.menu_window.close() # Close the Menu window
        self.close() # Close the current Kuis window