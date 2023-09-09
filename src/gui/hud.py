from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import (QApplication, QGridLayout, QGroupBox,
                             QHBoxLayout, QLabel, QStyleFactory, QWidget)

from lib import config_helper


class HUD(QWidget):
    def __init__(self, parent=None):
        super(HUD, self).__init__(parent)
        self.cfg = config_helper.read_config()
        self.appName = self.cfg['appName']

        self.setAttribute(Qt.WA_TransparentForMouseEvents)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.setWindowIcon(QIcon('.\\assets\\layout\\mmorpg_helper.ico'))
        QApplication.setStyle(QStyleFactory.create('Fusion'))
        self.setWindowTitle(self.appName)
        self.setGeometry(0, 100, 1700, 900)
        self.setFixedSize(1700, 900)
        
        self.hud_map()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.hudMap, 0, 0)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)


    # circular map
    def hud_map(self):
        self.hudMap = QGroupBox()
        layout = QHBoxLayout()

        self.imageLabel = QLabel(self)
        pixmap = QPixmap('.\\assets\\layout\\mmorpg_helper_hud')
        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.resize(pixmap.width(), pixmap.height())
        
        layout.addWidget(self.imageLabel)
        self.hudMap.setLayout(layout)

