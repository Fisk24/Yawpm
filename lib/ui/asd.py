import os
from PyQt4       import uic
from PyQt4.QtGui import *

class AddShortcutDialog(QDialog):
    def __init__(self, parent):
        super(AddShortcutDialog, self).__init__(parent)

        self.parent = parent
        self.ui = uic.loadUi("lib/ui/newshortcut.ui", self)
        
        ### VARS ###
        self.name = ""
        self.comm = ""
        self.exe  = ""
        self.icon = ""
        self.term = "false"
        self.type = "Application"
        self.cate = ""

        self.start  = "./"
        self.prefix = 0
        self.data   = {}

        self.didExec = 0

        ### CONNECTIONS ###
        self.ui.acceptPushButton.clicked.connect(self.validate)
        self.ui.cdPushButton.clicked.connect(self.findStartPoint)
        self.ui.executablePushButton.clicked.connect(self.findExecutable)
        self.ui.browseIconToolButton.clicked.connect(self.findIcon)
        self.ui.iconLineEdit.textChanged.connect(self.updateIcon)
        self.ui.prefixComboBox.currentIndexChanged.connect(self.updatePrefixIndex)

        self.populate()

    def populate(self):
        self.populatePrefixComboBox()

    def populatePrefixComboBox(self):
        prefixes = self.parent.manager.prefixes
        for i in prefixes:
            self.ui.prefixComboBox.addItem(i[0])

    def updatePrefixIndex(self, index):
        # This function is called whenever the index of prefixComboBox is changed.
        # the index should match the index of the prefix in the list provided py the
        # prefix manager. Therefore this index will refrence the correct information
        # when this data in this dialog is passed to the shortcut manager
        self.prefix = index

    def updateIcon(self):
        #print("Text Changed")
        icon = self.ui.iconLineEdit.text()
        if os.path.isfile(icon):
            self.ui.browseIconToolButton.setIcon(QIcon(icon))
        else:
            self.ui.browseIconToolButton.setIcon(QIcon().fromTheme(icon))

    def findIcon(self):
        icon = QFileDialog.getOpenFileName(self, "Open Icon", "/home", "Images (*.png *.ico *.svg)")
        if icon != "":
            self.ui.iconLineEdit.setText(icon)
            self.ui.browseIconToolButton.setIcon(QIcon(icon))
            #self.ui.iconLabel.setPixmap(QPixmap(icon).scaled(24, 24))

    def findStartPoint(self):
        start = QFileDialog.getExistingDirectory(self, "Starting Directory", options = QFileDialog.ReadOnly | QFileDialog.ShowDirsOnly)
        if start != "":
            self.ui.cdPushButton.setText(start)
            self.start = start

    def findExecutable(self):
        exec_ = QFileDialog.getOpenFileName(self, "Open Executable", "/home", "Executables (*.exe)")
        if exec_ != "":
            self.ui.executablePushButton.setText(exec_)
            self.exe = exec_
            self.didExec = 1
        else:
            self.didExec = 0

    def generateSCData(self):
        self.data["Name"]       = self.name
        self.data["Comment"]    = self.comm
        self.data["Exec"]       = self.exe
        self.data["Icon"]       = self.icon
        self.data["Terminal"]   = self.term
        self.data["Type"]       = self.type
        self.data["Categories"] = self.cate
        self.data["start"]      = self.start
        self.data["prefix"]     = self.prefix
        #self.data[""] = self.
        #self.data[""] = self.

    def validateName(self, name):
        # Shortcut names must consist of atleast one non-whiespace character
        if len(name.strip()) > 0:
            self.name = name.strip()
            return 1
        else:
            QMessageBox.critical(self, "Name error!", "A shortcut name must consist of atleast one non-whitespace character")
            return 0

    def validateExec(self):
        # The user either has or hasent picked an executable
        # The user must have picked an executable to continue
        if self.didExec:
            return 1
        else:
            QMessageBox.critical(self, "No Executable Selected", "You must select a file to execute.")
            return 0

    def validate(self):
        if not self.validateName(self.ui.nickLineEdit.text()): return 0
        if not self.validateExec(): return 0
        self.comm = self.ui.commentLineEdit.text()
        self.icon = self.ui.iconLineEdit.text()
        self.cate = self.ui.categoryLineEdit.text()

        self.generateSCData()

        self.parent.shortcut.addShortcut(self.data)
        self.parent.updateShortcutList()
        self.accept()

    @staticmethod
    def getDialog(parent=None):
        dialog = AddShortcutDialog(parent)
        result = dialog.exec_()
        return (result == QDialog.Accepted)
