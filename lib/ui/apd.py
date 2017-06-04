import os

from PyQt5           import uic
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *

class AddPrefixDialog(QDialog):
    def __init__(self, parent=None):
        super(AddPrefixDialog, self).__init__(parent)
        
        self.parent = parent
        self.ui = uic.loadUi("lib/ui/newprefix.ui", self)

        self.prefixLocation = None
        self.executableLocation = "wine"

        ### Connect UI Elements ###
        self.ui.selectPrefixPushButton.clicked.connect(self.selectPrefixLocation)
        self.ui.browseNewWineToolButton.clicked.connect(self.selectWineLocation)
        self.ui.addPushButton.clicked.connect(self.validate)
        self.ui.cancelPushButton.clicked.connect(self.reject)

    def validate(self):
        # Check to see if the prefix nickname is a valid string
        if self.checkValidNick(self.ui.nickNameLineEdit.text()):
            nick = self.ui.nickNameLineEdit.text().strip()
        else:
            QMessageBox.critical(None, "Invalid Nickname!", "Nicknames must consist of atleast one non-whitespace character")
            return
        # Check to see if the prefix location has been set
        if self.prefixLocation:
            pref = self.prefixLocation
        else:
            QMessageBox.critical(None, "Invalid Prefix!", "Please select the location of the prefix before you continue.")
            return
        # Check to ensure that the selected wine executable exists and that it executable
        if self.ui.doNewWineCheckBox.isChecked():
            if self.validateWine() == 1:
                # in the event of a successful validation set the variable accordingly
                wine = self.executableLocation
            elif self.validateWine() == 2:
                # one possible error...
                QMessageBox.critical(self, "Wine executable error!", "The choosen wine executable does not exist! Please choose a different one...")
                return
            elif self.validateWine() == 3:
                # another possible error...
                QMessageBox.critical(self, "Wine executable error!", "This file is not executable. Check to ensure that you have selected the correct file...")
                return
        else:
            wine = "wine"

        arch = self.ui.archComboBox.currentText()

        self.acceptValues(nick, pref, arch, wine)

    def acceptValues(self, nick, pref, arch, wine):
        ## Target the prefix and attempt wineboot
        # this will generate a new prefix of the desired arch, or
        # it will warn user that an existing prefix would be added with 
        # the incorrect arch
        
        if self.doWineBoot(pref, arch, wine):
            try:
                self.parent.manager.addPrefix([nick, pref, arch, wine])
                self.parent.manager.savePrefixList()
                self.parent.populatePrefixList()
                self.parent.updatePrefixInfo()
                self.accept()
            except ValueError as e:
                QMessageBox.critical(self, "Value Error", str(e))

    def validateWine(self):
        ## Return a value based on the outcome of these tests
        #  if the file exists and is executable the wine executable is valid
        if not os.path.isfile(self.executableLocation):
            return 2
        if not os.access(self.executableLocation, os.X_OK):
            return 3
        return 1

    def doWineBoot(self, target, arch, wine):
        # if a folder does not exist, create prefix
        # if a folder exists but is empty, create prefix
        # if the folder exists but is not empty and is not a wine prefix do not create wine prefix
        if os.path.isdir(target):
            try:
                os.rmdir(target)
                self.parent.wine.setTargetPrefix(target, wine, arch)
                result = self.parent.wine.wineBoot()
                if result.returncode == 1:
                    QMessageBox.critical(None, "Wine Error!", result)
                return not result.returncode
            except OSError as e:
                print("########### {} ##########".format(e))
                # if the non-empty directory is a preexisting wine prefix
                if self.testIsPrefix(target):
                    self.parent.wine.setTargetPrefix(target, wine, arch)
                    result = self.parent.wine.wineBoot()
                    if result.returncode == 1:
                        QMessageBox.critical(None, "Wine Error!", "An unspecified error has occured. Is the architecture wrong?")
                    return not result.returncode
                else:
                    QMessageBox .critical(None, "Prefix Error!", "Supplied directory is not empty, and is not a preexisting wine prefix.")
                    return 0

            except FileNotFoundError:
                pass

    def testIsPrefix(self, target):
        # take give dir "target" and determin whether or not it is a wine prefix

        # files required to qualify as a wineprefix
        require = ["drive_c"]
        testdir = os.listdir(target)
        for requirement in require:
            if requirement in testdir:
                pass
            else:
                return 0
        return 1

    def selectPrefixLocation(self):
        # folder should start in the users home folder, but should not allow the users home folder to be 
        # classified as a wine prefix. This is because wine would create all of its prefix files in the 
        # users home folder instead of some subdirectory therein.
        folder = QFileDialog.getExistingDirectory(self, 
                    caption = "Select wine prefix location.",
                    options = QFileDialog.ShowDirsOnly)

        if len(folder) >= 1:
            self.ui.selectPrefixPushButton.setText("Prefix location: "+folder)
            self.prefixLocation = folder

    def cleanNick(self, nick):
        return nick.strip()
        # strip spaces from the beginning and end of nicknames automaticaly

    def checkValidNick(self, nick):
        ## Ensure that the user has input a nickname
        # nicknames must be atleast one character
        # nicknames cannot consist only of spaces
        if len(nick.strip()) >= 1:
            return True
        else:
            return False

    def selectWineLocation(self):
        # Inform add prefix dialog as to the location of the wine executable that should be envoked
        # when a program is launched from this prefix
        selected = QFileDialog.getOpenFileName(self,
                    "Select wine executable location.")

        executable = selected[0]

        if len(executable) > 1:
            self.ui.newWineLineEdit.setText(executable)
            self.executableLocation = executable

    @staticmethod
    def getDialog(parent=None):
        dialog = AddPrefixDialog(parent)
        result = dialog.exec_()
        return (result == QDialog.Accepted)
