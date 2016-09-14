#! /usr/bin/python3

import sys, os, re

from PyQt4        import uic
from PyQt4.QtGui  import *
from PyQt4.QtCore import *

from lib.winectl import WineControl
from lib.prefix  import PrefixManager
from lib.ui.apd  import AddPrefixDialog
from lib.ui.rpd  import RemovePrefixDialog

# Setup
# Config
# Logger

class Yawpm(QMainWindow):
    def __init__(self):
        super(Yawpm, self).__init__()
        # load ui files
        self.ui = uic.loadUi("lib/ui/main.ui", self)

        # initialize prefix programs info list
        # Keys = prefixNickName
        self.prefixInfo = {}
        
        # initialize wine controls
        self.wine = WineControl()
        
        # initialize Prefix list manager
        self.manager  = PrefixManager()
        self.manager.loadPrefixList()

        self.printList(self.manager.prefixes)

        # Show ui
        self.show()

        # populate ui
        self.populate()

        # connect buttons and others
        # When prefixListWidget changes selected item
        self.ui.prefixListWidget.itemSelectionChanged.connect(self.updatePrefixInfo)
        # When runInPushButton is clicked
        self.ui.runInPushButton.clicked.connect(self.doRunInCurrentPrefix)
        self.ui.cfgToolButton.clicked.connect(self.wine.wineCfg)
        self.ui.gameToolButton.clicked.connect(self.wine.wineJoyStick)
        self.ui.installedToolButton.clicked.connect(self.wine.wineAppWiz)
        self.ui.driveToolButton.clicked.connect(self.wine.openWineDrive)
        self.ui.winetricksToolButton.clicked.connect(self.wine.winetricks)
        self.ui.addPrefixPushButton.clicked.connect(self.doAddPrefix)
        self.ui.removePrefixPushButton.clicked.connect(self.doRemovePrefix)

    def populate(self):
        self.populatePrefixList()
        self.updatePrefixInfo()

    def doRemovePrefix(self):
        dialog = RemovePrefixDialog.getDialog(self)

    def doAddPrefix(self):
        dialog = AddPrefixDialog.getDialog(self)

    def doRunInCurrentPrefix(self):
        # pick exe file to run, start in the prefix drive_c, and only show executable files.
        exe = QFileDialog.getOpenFileName(self, 
                                        "Select program to run.", 
                                        self.manager.getDir()+"/drive_c", 
                                        "Executable files (*.exe *.msi *.cpl *.bat *.cmd)")
        self.wine.runInTarget([exe])

    def updatePrefixInfo(self):
        # change currentIndex in the manager
        self.manager.currentIndex = self.ui.prefixListWidget.currentRow()

        # new prefix values
        dire = self.manager.getDir()
        arch = self.manager.getArch()

        # change the targeted wine prefix
        self.wine.setTargetPrefix(dire, arch)

        # change UI info
        self.ui.prefixDirectoryLabel.setText(dire)
        self.ui.prefixArchitectureLabel.setText(arch)

    def populatePrefixList(self):
        self.ui.prefixListWidget.clear()
        for prefix in self.manager.prefixes:
            # Create listWidgetItem Object with the nickname text
            item = QListWidgetItem(prefix[0], self.ui.prefixListWidget)
        self.ui.prefixListWidget.setCurrentRow(0)

    def printList(self, _list):
        for i in _list:
            print(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Yawpm()
    sys.exit(app.exec_())
