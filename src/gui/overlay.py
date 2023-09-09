from logging import getLogger, info, FileHandler
from keyboard import add_hotkey
from threading import Thread, Lock
from time import sleep
from sys import exit
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import (QApplication, QComboBox, QPlainTextEdit, QGridLayout, QGroupBox,
                             QPushButton, QHBoxLayout, QStyleFactory, QWidget, QCheckBox)

from lib import config_helper, logging_helper, process_helper
from gui import toolbox, hud
from bot import combat


class Overlay(QWidget):
    def __init__(self, parent=None):
        super(Overlay, self).__init__(parent)
        self.running = False
        self.pause = False
        self._lock = Lock()
        self.pause_req = False
        self.cfg = config_helper.read_config()
        self.appName = self.cfg['appName']
        self.proc = process_helper.ProcessHelper()
        self.app_hud = hud.HUD()

        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('.\\assets\\layout\\mmorpg_helper.ico'))
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle(self.appName)
        self.setGeometry(1475, 625, 400, 170)
        self.setFixedSize(400, 170)
        
        add_hotkey('end', lambda: self.on_press('exit'))
        add_hotkey('del', lambda: self.on_press('pause'))
        add_hotkey('capslock', lambda: self.on_press('pause'))
        add_hotkey('capslock+w', lambda: self.on_press('pause'))
        add_hotkey('capslock+a', lambda: self.on_press('pause'))
        add_hotkey('capslock+s', lambda: self.on_press('pause'))
        add_hotkey('capslock+d', lambda: self.on_press('pause'))
        add_hotkey('capslock+w+a', lambda: self.on_press('pause'))
        add_hotkey('capslock+w+d', lambda: self.on_press('pause'))
        add_hotkey('capslock+s+a', lambda: self.on_press('pause'))
        add_hotkey('capslock+s+d', lambda: self.on_press('pause'))
        
        self.createDropdownBox()
        self.createStartBox()
        self.createToolBox()
        self.createLoggerConsole()
        self.loggerConsole.setDisabled(False)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.dropdownBox, 0, 0)
        mainLayout.addWidget(self.startBox, 0, 1)
        mainLayout.addWidget(self.toolBox, 0, 2)
        mainLayout.addWidget(self.loggerConsole, 1, 0, 1, 3)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)
        
        if self.cfg['showHUD'] == '1':
            self.show_hud()


    # prepare dropdownBox
    def update_config(self, item, value=None):
        info('Config item "' + item + '" set to new value: ' + value)
        config_helper.save_config(item, value)


    def passCurrentText(self):
        self.update_config('playerClass', self.ComboBox.currentText())
            

    def get_class(self):
        result = []
        class_array = ['Soulbeast PvP', 'Soulbeast PvE']
        for playerClass in class_array:
            result = QStandardItem(playerClass)
            self.model.appendRow(result)
        self.ComboBox.setCurrentIndex(0)


    # loggerConsole
    def createLoggerConsole(self):
        self.loggerConsole = QWidget()
        layout = QHBoxLayout()

        log_text_box = QPlainTextEdit(self)
        log_text_box.setStyleSheet('background-color: rgba(255,255,255, 0); color: rgb(0,0,255);')
        log_text_box.setReadOnly(True)
        handler = FileHandler('.\\log\\mmorpgHelper.log')
        getLogger().addHandler(handler)
        handler = logging_helper.Handler(self)
        getLogger().addHandler(handler)
        #getLogger().setLevel(DEBUG)
        handler.new_record.connect(log_text_box.appendPlainText)
        
        layout.addWidget(log_text_box)
        self.loggerConsole.setLayout(layout)
        
    
    def closeEvent(self):
        root_logger = getLogger()
        handler = logging_helper.Handler(self)
        root_logger.removeHandler(handler)
        exit(0)


    # dropdownBox
    def createDropdownBox(self):
        self.dropdownBox = QGroupBox()
        layout = QHBoxLayout()

        self.model = QStandardItemModel()
        self.ComboBox = QComboBox()
        self.ComboBox.setModel(self.model)
        
        self.get_class()
        self.ComboBox.activated.connect(self.passCurrentText)

        layout.addWidget(self.ComboBox)
        layout.addStretch(1)
        self.dropdownBox.setLayout(layout)


    # startBox
    def createStartBox(self):
        self.startBox = QGroupBox()
        layout = QHBoxLayout()
        
        toggleHUD = QCheckBox("HUD")
        toggleHUD.setStyleSheet('color: rgb(0,0,255);')
        if self.cfg['showHUD'] == '1':
            toggleHUD.setChecked(True)
        else:
            toggleHUD.setChecked(False)
        toggleHUD.stateChanged.connect(lambda: self.set_hud())

        toggleAssistButton = QPushButton("ASSISTANT")
        toggleAssistButton.setCheckable(False)
        toggleAssistButton.setChecked(False)
        toggleAssistButton.clicked.connect(lambda: self.get_rotation_thread())

        layout.addStretch(1)
        layout.addWidget(toggleHUD)
        layout.addStretch(1)
        layout.addWidget(toggleAssistButton)
        layout.addStretch(1)
        self.startBox.setLayout(layout)


    # toolBox
    def createToolBox(self):
        self.toolBox = QGroupBox()
        layout = QHBoxLayout()

        toggleToolButton = QPushButton("TOOLBOX")
        toggleToolButton.setCheckable(False)
        toggleToolButton.setChecked(False)
        toggleToolButton.clicked.connect(self.show_toolbox)

        layout.addStretch(1)
        layout.addWidget(toggleToolButton)
        layout.addStretch(1)
        self.toolBox.setLayout(layout)


    def on_press(self, key):
        if key == 'exit':
            info('*** EXIT ***')
            if self.running:
                self.running = False
                self.rotation_thread.join()
                #self.closeEvent()
        elif key == 'pause':
            self.set_pause(not self.should_pause())
            if self.pause == False:
                self.pause = True
                info('*** PAUSE ***')
            else:
                self.pause = False
                info('*** RUN ***')
            

    def should_pause(self):
        self._lock.acquire()
        pause_req = self.pause_req
        self._lock.release()
        return pause_req


    def set_pause(self, pause):
        self._lock.acquire()
        self.pause_req = pause
        self._lock.release()


    def set_hud(self):
        cfg = config_helper.read_config()
        if cfg['showHUD'] == '1':
            self.update_config('showHUD', '0')
            self.hide_hud()
        else:
            self.update_config('showHUD', '1')
            self.show_hud()


    def get_rotation_thread(self):
        self.rotation_thread = Thread(target=lambda: self.get_rotation())

        if not self.rotation_thread.is_alive():
            self.rotation_thread = None
            self.rotation_thread = Thread(target=lambda: self.get_rotation())
            self.rotation_thread.start()


    def get_rotation(self):
        info('Starting up combat')
        #self.proc.set_window_pos()
        self.proc.set_foreground_window()
        self.running = True

        while self.running:
            while self.should_pause():
                sleep(0.25)
            combat.rotation()

        info("Closing combat")


    def show_toolbox(self):
        app_toolbox = toolbox.Toolbox()
        app_toolbox.show()
        
        info('Starting up toolbox')


    def show_hud(self):
        self.app_hud.show()
        
        info('Starting up hud')


    def hide_hud(self):
        self.app_hud.close()
        
        info('Closing hud')

