import os
from PyQt5           import uic
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *

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
        self.flags  = ""
        self.data   = {}
        self.environmentVars = []

        self.didExec = 0

        ### CONNECTIONS ###
        self.ui.acceptPushButton.clicked.connect(self.validate)
        #self.ui.cdPushButton.clicked.connect(self.findStartPoint)
        self.ui.executablePushButton.clicked.connect(self.findExecutable)
        self.ui.browseIconToolButton.clicked.connect(self.findIcon)
        self.ui.iconLineEdit.textChanged.connect(self.updateIcon)
        self.ui.flagsLineEdit.textChanged.connect(self.updateFlags)
        self.ui.prefixComboBox.currentIndexChanged.connect(self.updatePrefixIndex)
        self.ui.newVarToolButton.clicked.connect(self.addEnvironmentVariable)

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

    def updateFlags(self):
    	self.flags = self.ui.flagsLineEdit.text().strip()

    def addEnvironmentVariable(self):
        enviro = self.newVarLineEdit.text()
        components = enviro.split("=")
        varName = components[0].upper().strip()
        varValue = components[1].strip()
        varString = varName+"="+varValue
        if (varName == "LD_PRELOAD"):
            if not os.path.isfile(varValue):
                QMessageBox.critical(self, "File Not Found", components[1] + " is not a file or dosen't exist!")
                return 1
        self.ui.newVarLineEdit.setText("")
        self.ui.envListWidget.addItem(varString)
        self.environmentVars.append(varString)

    def findIcon(self):
        selected = QFileDialog.getOpenFileName(self, "Open Icon", "/home", "Images (*.png *.ico *.svg)")
        icon = selected[0]
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
        selected = QFileDialog.getOpenFileName(self, "Open Executable", "/home", "Executables (*.exe)")
        exec_ = selected[0]
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
        self.data["flags"]      = self.flags
        self.data["environment"]= self.environmentVars
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
