#! /usr/bin/python3

import sys, os

from PyQt4        import uic
from PyQt4.QtGui  import *
from PyQt4.QtCore import *

from lib.winectl import WineControl
from lib.prefix  import PrefixManager 

# Setup
# Config
# Logger

class Yawpm(QMainWindow):
    def __init__(self):
        super(Yawpm, self).__init__()
        # load ui files
        self.ui = uic.loadUi("lib/ui/main.ui", self)
        
        # initialize wine controls
        self.wine = WineControl()
        
        # initialize Prefix list manager
        self.manager  = PrefixManager()
        self.manager.loadPrefixList()

        self.printList(self.manager.prefixes)

        # populate ui
        self.populate()

        # connect buttons and others
        # When prefixListWidget changes selected item
        self.ui.prefixListWidget.itemSelectionChanged.connect(self.updatePrefixInfo)
        # When runInPushButton is clicked
        self.ui.runInPushButton.clicked.connect(self.doRunInCurrentPrefix)

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

    def populate(self):
        self.populatePrefixList()

    def populatePrefixList(self):
        for prefix in self.manager.prefixes:
            # Create listWidgetItem Object with the nickname text
            item = QListWidgetItem(prefix[0], self.ui.prefixListWidget)


    def printList(self, _list):
        for i in _list:
            print(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Yawpm()
    main.show()
    sys.exit(app.exec_())
