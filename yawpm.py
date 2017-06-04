#! /usr/bin/python3

import sys, os, re

from PyQt5           import uic
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

from lib          import setup
from lib.winectl  import WineControl
from lib.prefix   import PrefixManager
from lib.shortcut import ShortcutManager
from lib.ui.apd   import AddPrefixDialog
from lib.ui.rpd   import RemovePrefixDialog
from lib.ui.asd   import AddShortcutDialog
from lib.ui.epd   import EditPrefixDialog

# Setup
# Config
# Logger

## prefixes.csv should be created if it does not exist and the prefered location for this file is in $USER/.config/yawpm/prefixes.csv

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
        self.manager  = PrefixManager(_file=setup.PREFIXCSV)
        self.manager.loadPrefixList()

        self.printList(self.manager.prefixes)

        # initialize Shortcut Manager
        self.shortcut = ShortcutManager(self, setup.USER)
        self.shortcut.scanShortcuts()

        # Show ui
        self.show()

        # populate ui
        self.populate()

        ### connect buttons and others
        # When prefixListWidget changes selected item
        self.ui.prefixListWidget.itemSelectionChanged.connect(self.updatePrefixInfo)
        # When the user wants to interact with the current wine prefix
        self.ui.runInPushButton.clicked.connect(self.doRunInCurrentPrefix)
        self.ui.cfgToolButton.clicked.connect(self.wine.wineCfg)
        self.ui.gameToolButton.clicked.connect(self.wine.wineJoyStick)
        self.ui.installedToolButton.clicked.connect(self.wine.wineAppWiz)
        self.ui.driveToolButton.clicked.connect(self.wine.openWineDrive)
        self.ui.winetricksToolButton.clicked.connect(self.wine.winetricks)
        # When the user wants to make changes to the prefix list
        self.ui.editPrefixPushButton.clicked.connect(self.doEditPrefix)
        self.ui.addPrefixPushButton.clicked.connect(self.doAddPrefix)
        self.ui.removePrefixToolButton.clicked.connect(self.doRemovePrefix)
        # when the user wants to make changes to the shortcut list
        self.ui.shortcutListWidget.itemDoubleClicked.connect(self.doLaunchShortcut)
        self.ui.addShortcutPushButton.clicked.connect(self.doAddShortcut)
        self.ui.delShortcutPushButton.clicked.connect(self.doDelShortcut)
        # when the Kill all button is pressed
        self.ui.wkaPushButton.clicked.connect(self.doKillAllWineProcesses)
        # when the basic debugging level is changed
        self.ui.llComboBox.currentIndexChanged.connect(self.doChangeDebuggingLevelSimple)

    def listWidgetChanged(self):
        # store prefix data from target index
        # pop prefix from target index
        # insert stored data at new index
        print("CHANGE!!!!")

    def populate(self):
        self.populatePrefixList()
        self.populateShortcutList()
        self.updatePrefixInfo()

    def doLaunchShortcut(self):
        # Launches a shortcut from a specified index location
        index = self.ui.shortcutListWidget.currentRow()
        self.shortcut.launchShortcut(index)

    def doAddShortcut(self):
        dialog = AddShortcutDialog.getDialog(self)           

    def doDelShortcut(self):
        question = QMessageBox.question(self, "Delete shortcut?", "This action will delete this shortcut from your system", "Ok", "No Don't!")
        # QMessagebox returns 0 for yes so the conditional needs to be inverted
        if not question:
            index = self.ui.shortcutListWidget.currentRow()
            self.shortcut.delShortcut(index)
            self.shortcut.scanShortcuts()
            self.populateShortcutList()

    def doRemovePrefix(self):
        dialog = RemovePrefixDialog.getDialog(self)

    def doAddPrefix(self):
        dialog = AddPrefixDialog.getDialog(self)

    def doEditPrefix(self):
        dialog = EditPrefixDialog.getDialog(self)

    def doRunInCurrentPrefix(self):
        # pick exe file to run, start in the prefix drive_c, and only show executable files.
        selected = QFileDialog.getOpenFileName(self, 
                                        caption="Select program to run.", 
                                        directory=self.manager.getDir()+"/drive_c", 
                                        filter="Executable files (*.exe *.msi *.cpl *.bat *.cmd)",
                                        options=QFileDialog.ReadOnly)
        exe = selected[0]
        if exe != "":
            if ".msi" in exe:
                self.wine.runInTarget([exe], msi=True)
            else:
                self.wine.runInTarget([exe])

    def doKillAllWineProcesses(self):
        self.wine.wineKillAll()

    def doChangeDebuggingLevelSimple(self):
        self.wine.setDebugLevelSimple(level=self.ui.llComboBox.currentIndex())
        # debug
        print(self.wine.WINEDEBUG)

    def updatePrefixInfo(self):
        # change currentIndex in the manager
        #self.manager.currentIndex = self.ui.prefixListWidget.currentRow()
        self.manager.currentIndex = 0

        # new prefix values
        dire  = self.manager.getDir()
        arch  = self.manager.getArch()
        exec_ = self.manager.getExec()

        # change the targeted wine prefix
        self.wine.setTargetPrefix(dire, exec_, arch)

        # change UI info
        self.ui.prefixDirectoryLabel.setText(dire)
        self.ui.prefixArchitectureLabel.setText(arch)
        if exec_ == "wine":
            self.ui.prefixExecutableLabel.setText("{ver}: System Default".format(ver=self.wine.WINEVER))
        else:
            self.ui.prefixExecutableLabel.setText("{ver}: {exe}".format(ver=self.wine.WINEVER, exe=exec_))

    def populatePrefixList(self):
        self.ui.prefixListWidget.clear()
        for prefix in self.manager.prefixes:
            # Create listWidgetItem Object with the nickname text
            item = QListWidgetItem(prefix[0], self.ui.prefixListWidget)
        self.ui.prefixListWidget.setCurrentRow(0)

    def updateShortcutList(self):
        self.shortcut.scanShortcuts()
        self.populateShortcutList()

    def populateShortcutList(self):
        # Clear the list widget, then fill it with shortcuts
        self.ui.shortcutListWidget.clear()
        for shortcut in self.shortcut.shortcuts:
            # create the listWidgetItem using the information in the shortcut manager
            #
            # Decide how to create the icon object for the shortcut in the listWidget
            if os.path.isfile(shortcut["Icon"]):
                icon = QIcon(shortcut["Icon"])
            else:
                icon = QIcon().fromTheme(shortcut["Icon"])
            item = QListWidgetItem(
                    icon,
                    shortcut["Name"],
                    self.ui.shortcutListWidget
                    )
        self.ui.shortcutListWidget.setCurrentRow(0)

    def printList(self, _list):
        for i in _list:
            print(i)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Yawpm()
    sys.exit(app.exec_())
