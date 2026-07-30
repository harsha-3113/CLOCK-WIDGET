import sys
import datetime
import pygame
from PyQt5.QtWidgets import (
                            QApplication, QWidget, QLabel, QVBoxLayout, QHBoxLayout,
                            QTabWidget, QLineEdit, QPushButton)
from PyQt5.QtCore import QTimer, QTime, Qt
from PyQt5.QtGui import QFont, QFontDatabase
from PyQt5.QtGui import QIcon

class DigitalClock(QWidget):
    def __init__(self):
        super().__init__()
        
        self.time_label = QLabel(self)
        self.timer = QTimer(self)
        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()
        vbox.addWidget(self.time_label)
        self.setLayout(vbox)
        self.setWindowIcon(QIcon("assets/icon.jpg"))
        self.time_label.setAlignment(Qt.AlignCenter)
        self.time_label.setStyleSheet("font-size:150px;"
                                       "color:hsl(111, 100%, 50%);")
        self.setStyleSheet("background-color: black;")

        font_id = QFontDatabase.addApplicationFont("assets/DS-DIGIT.TTF")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        my_font = QFont(font_family, 150)
        self.time_label.setFont(my_font)

        self.timer.timeout.connect(self.update_time)
        self.timer.start(1000)
        self.update_time()


    def update_time(self):
        current_time = QTime.currentTime().toString("HH:mm:ss")
        self.time_label.setText(current_time)


class AlarmClock(QWidget):

    def __init__(self):
        super().__init__()
        self.sound_file = "assets/alarm_sound.mp3"
        self.alarm_time = None
        self.alarm_active = False
        self.check_timer = QTimer(self)
        self.check_timer.timeout.connect(self.check_alarm)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("background-color: black;")

        font_id = QFontDatabase.addApplicationFont("assets/DS-DIGIT.TTF")
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        green = "hsl(111, 100%, 50%);"
        input_color = "#05f5e9;"

        self.normal_button_style = (f"font-size:20px; padding:5px; color:{green} "
            "background-color:black; border: 1px solid hsl(111, 100%, 50%);")

        self.set_button_style = ("font-size:20px; padding:5px; color:black; "
            "background-color:hsl(111, 100%, 50%); border: 1px solid hsl(111, 100%, 50%);")


        vbox = QVBoxLayout()
        self.current_time_label = QLabel("")
        self.current_time_label.setAlignment(Qt.AlignCenter)
        self.current_time_label.setStyleSheet(f"font-size:60px; color:{green}")
        self.current_time_label.setFont(QFont(font_family, 40))
        vbox.addWidget(self.current_time_label)

        input_row = QHBoxLayout()
        self.time_input = QLineEdit()
        self.time_input.setPlaceholderText("HH:MM:SS")
        self.time_input.setAlignment(Qt.AlignCenter)
        self.time_input.setStyleSheet(f"font-size:30px; padding:5px; color:{input_color} "
            "background-color:black; border: 1px solid hsl(111, 100%, 50%);")
        self.time_input.setFont(QFont(font_family, 20))
        input_row.addWidget(self.time_input)
        vbox.addLayout(input_row)

        self.set_button = QPushButton("SET ALARM")
        self.set_button.setStyleSheet(self.normal_button_style)
        self.set_button.clicked.connect(self.set_alarm)
        vbox.addWidget(self.set_button)
        self.stop_button = QPushButton("STOP ALARM")
        self.stop_button.setStyleSheet(f"font-size:20px; padding:5px; color: black; background-color:hsl(0, 92%, 51%); border: 1px solid hsl(0, 92%, 51%);")
        self.stop_button.clicked.connect(self.stop_alarm)
        self.stop_button.hide()
        vbox.addWidget(self.stop_button)

        self.status_label = QLabel("YOU DONT HAVE AN ALARM SET!!")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size:20px; color:hsl(0, 80%, 41%);")
        vbox.addWidget(self.status_label)
        self.setLayout(vbox)

        display_timer = QTimer(self)
        display_timer.timeout.connect(self.update_display_time)
        display_timer.start(1000)
        self.update_display_time()

    def update_display_time(self):
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        self.current_time_label.setText(current_time)

    def set_alarm(self):
        print("set_alarm called")
        self.alarm_time = self.time_input.text().strip()
        if not self.alarm_time:
            self.status_label.setText("Please enter a valid time")
            return

#add funtion for date also :)
        self.status_label.setText(f"ALARM SET FOR {self.alarm_time}")
        self.alarm_active = True
        self.check_timer.start(1000)
        self.set_button.setText("ALARM HAS BEEN SET")
        self.set_button.setStyleSheet(self.set_button_style)
        self.set_button.setEnabled(False)

    def check_alarm(self):
        if not self.alarm_active:
            return

        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        print(current_time)

        if current_time == self.alarm_time:
            print("TIME's UP!!!!!!!")
            self.status_label.setText("TIME'S UP!!!!!!!")

            pygame.mixer.init()
            pygame.mixer.music.load(self.sound_file)
            pygame.mixer.music.play()
            self.stop_button.show()
            self.set_button.setText("STOP TO RESET")

            self.alarm_active = False
            self.check_timer.stop()
            self.playback_timer = QTimer(self)
            self.playback_timer.timeout.connect(self.check_playback_finished)
            self.playback_timer.start(1000)

    def stop_alarm(self):
        pygame.mixer.music.stop()
        if hasattr(self, 'playback_timer'):
            self.playback_timer.stop()
        self.stop_button.hide()
        self.status_label.setText("INTERRUPTED!! GET BACK TO WORK :)")
        self.set_button.setText("SET ALARM")
        self.set_button.setStyleSheet(self.normal_button_style)
        self.set_button.setEnabled(True)

    def check_playback_finished(self):
        if not pygame.mixer.music.get_busy():
            self.playback_timer.stop()
            self.stop_button.hide()
            self.status_label.setText("NO ALARM SET")
            self.set_button.setText("SET ALARM")
            self.set_button.setStyleSheet(self.normal_button_style)
            self.set_button.setEnabled(True)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Clock & Alarm")
        self.setGeometry(600, 400, 500, 500)

        tabs = QTabWidget()
        tabs.addTab(DigitalClock(), "Clock")
        tabs.addTab(AlarmClock(), "Alarm")
        tabs.setStyleSheet("""
                            QTabWidget::pane { background-color: black; border: 0px; }
                            QTabBar::tab {
                                background: black;
                                color: hsl(55, 92%, 48%);
                                padding: 8px 20px;
                                border: 1px solid hsl(299, 45%, 37%);
                            }
                            QTabBar::tab:selected {
                                background: hsl(283, 98%, 50%);
                            }
                        """)

        self.setStyleSheet("background-color: black;")
        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())