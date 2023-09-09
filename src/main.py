#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from logging import getLogger, info, error, INFO
from sys import exit, argv
from PyQt5.QtWidgets import QApplication

from lib import config_helper
from gui import overlay


APPNAME = 'mmorpgHelper'
APPVERSION = 'v1.0.4.0012-gw2'


def main():
    cfg = config_helper.read_config()
    getLogger().setLevel(INFO)

    app = QApplication(argv)
    app_gui = overlay.Overlay()
    app_gui.show()

    info(('### %s ### %s ###') % (APPNAME, APPVERSION))
    info('Starting up gui')
    info('Config item "playerClass" set to: ' + cfg['playerClass'])
    
    exit(app.exec_())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        error("Unexpected exception! %s", e)

