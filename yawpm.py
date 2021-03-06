#! /usr/bin/python3

import sys, os, re, argparse

from PyQt5           import uic
from PyQt5.QtGui     import *
from PyQt5.QtCore    import *
from PyQt5.QtWidgets import *

from lib.config   import Config
from lib.winectl  import WineControl, WineError
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
    def __init__(self, args=None):
        super(Yawpm, self).__init__()
        # load ui files
        self.ui = uic.loadUi("lib/ui/main.ui", self)

        # initialize configuration settings
        if (args.reconfig == True):
            Config().doDetectFirstTimeSetup(force=True)
        else:
            Config().doDetectFirstTimeSetup()

        Config().load()

        # initialize prefix programs info list
        # Keys = prefixNickName
        self.prefixInfo = {}

        # initialize wine controls
        self.wine = WineControl()

        # initialize Prefix list manager
        self.manager  = PrefixManager(_file=Config.PREFIXFILE)
        self.manager.loadPrefixList()

        self.printList(self.manager.prefixes)

        # initialize Shortcut Manager
        self.shortcut = ShortcutManager(self, Config.USER)
        self.shortcut.scanShortcuts()

        # Launcher behavior
        if (args.launcher != None):
            print("Yawpm has been run in launcher mode. Will start wine program and then exit.")
            print(args.launcher)
            sys.exit()

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
        # when the user wants to make changes to the program settings
        #self.ui.wineBottlesLineEdit.textChanged.connect(self.updateWineBottles)
        # when the Kill all button is pressed
        self.ui.wkaPushButton.clicked.connect(self.doKillAllWineProcesses)
        # when the basic debugging level is changed
        self.ui.llComboBox.currentIndexChanged.connect(self.doChangeDebuggingLevelSimple)

    def closeEvent(self, event):
        Config().save()
        event.accept()

    def updateWineBottles(self):
        configData    = Config().data
        newBottlesDir = self.ui.wineBottlesLineEdit.text()

        configData["bottles"] = newBottlesDir
        Config.apply(configData)

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
        self.shortcut.shortcuts[index].execute()

    def doAddShortcut(self):
        dialog = AddShortcutDialog.getDialog(self)

    def doDelShortcut(self):
        question = QMessageBox.question(self, "Delete shortcut?", "This action will delete this shortcut from your system", buttons = QMessageBox.No | QMessageBox.Yes)
        # QMessagebox returns 0 for yes so the conditional needs to be inverted
        if question == QMessageBox.Yes:
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
    	# WINEPREFIX can be applied to "wineserver -k"
        self.wine.wineKillAll()

    def doChangeDebuggingLevelSimple(self):
        self.wine.setDebugLevelSimple(level=self.ui.llComboBox.currentIndex())
        # debug
        print(self.wine.WINEDEBUG)

    def updatePrefixInfo(self):
        # change currentIndex in the manager
        currentRow = self.ui.prefixListWidget.currentRow()
        self.manager.currentIndex = currentRow

        # new prefix values
        try:
            dire  = self.manager.getDir()
            arch  = self.manager.getArch()
            exec_ = self.manager.getExec()
        except IndexError:
            # If the requested prefix index would be
            # outside the bounds of the prefix list
            # default to the first one instead and
            # try again
            self.ui.prefixListWidget.setCurrentRow(0)
            return


        # change the targeted wine prefix
        self.wine.setTargetPrefix(dire, exec_, arch)

        # change UI info
        self.ui.prefixDirectoryLabel.setText(dire)
        self.ui.prefixArchitectureLabel.setText(arch)
        if exec_ == "wine":
            self.ui.prefixExecutableLabel.setText("{ver}: System Default".format(ver=self.wine.WINEVER))
        else:
            self.ui.prefixExecutableLabel.setText("{ver}: {exe}".format(ver=self.wine.WINEVER, exe=exec_))

        # If the wine executable dose not exist due to it being moved of deleted
        # Disable any controles that would make use of it
        try:
            self.wine.getWineVersion(exec_)
            self.ui.configureTabWidget.setEnabled(True)
        except WineError:
            self.ui.configureTabWidget.setEnabled(False)

        # If the currently selected prefix is the default prefix
        # Disable the remove button, as users should not be able
        # to remove it
        if currentRow == 0:
            self.ui.removePrefixToolButton.setEnabled(False)
            self.ui.editPrefixPushButton.setEnabled(False)
        else:
            self.ui.removePrefixToolButton.setEnabled(True)
            self.ui.editPrefixPushButton.setEnabled(True)

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
            if os.path.isfile(shortcut.data["Icon"]):
                icon = QIcon(shortcut.data["Icon"])
            else:
                icon = QIcon().fromTheme(shortcut.data["Icon"])
            item = QListWidgetItem(
                    icon,
                    shortcut.data["Name"],
                    self.ui.shortcutListWidget
                    )
        self.ui.shortcutListWidget.setCurrentRow(0)

    def printList(self, _list):
        for i in _list:
            print(i)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--launcher")
    parser.add_argument("--reconfig", action='store_true')
    args = parser.parse_args()
    if (args.launcher == True):
        print("I would launch something instead of showing a gui.")
        sys.exit()
    else:
        app = QApplication(sys.argv)
        main = Yawpm(args)
        sys.exit(app.exec_())
