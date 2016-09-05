import os

from PyQt4       import uic
from PyQt4.QtGui import *

class AddPrefixDialog(QDialog):
    def __init__(self, parent=None):
        super(AddPrefixDialog, self).__init__(parent)
        
        self.parent = parent
        self.ui = uic.loadUi("lib/ui/newprefix.ui", self)

        self.prefixLocation = None

        ### Connect UI Elements ###
        self.ui.selectPrefixPushButton.clicked.connect(self.selectPrefixLocation)
        self.ui.addPushButton.clicked.connect(self.validate)
        self.ui.cancelPushButton.clicked.connect(self.reject)

    def validate(self):
        if self.checkValidNick(self.ui.nickNameLineEdit.text()):
            nick = self.ui.nickNameLineEdit.text().strip()
        else:
            QMessageBox.critical(None, "Invalid Nickname!", "Nicknames must consist of atleast one non-whitespace character")
            return
        if self.prefixLocation:
            pref = self.prefixLocation
        else:
            QMessageBox.critical(None, "Invalid Prefix!", "Please select the location of the prefix before you continue.")
            return

        arch = self.ui.archComboBox.currentText()

        ## Target the prefix and attempt wineboot
        # this will generate a new prefix of the desired arch, or
        # it will warn user that an existing prefix would be added with 
        # the incorrect arch
        
        if self.doWineBoot(pref, arch):
            self.parent.manager.addPrefix([nick, pref, arch])
            self.parent.manager.savePrefixList()
            self.parent.populatePrefixList()
            self.parent.updatePrefixInfo()
            self.accept()

    def doWineBoot(self, target, arch):
        # if a folder does not exist, create prefix
        # if a folder exists but is empty, create prefix
        # if the folder exists but is not empty do not create wine prefix
        if os.path.isdir(target):
            try:
                os.rmdir(target)
                self.parent.wine.setTargetPrefix(target, arch)
                result = self.parent.wine.wineBoot()
                return not result.returncode
            except OSError as e:
                print("########### {} ##########".format(e))
                # if the non-empty directory is a preexisting wine prefix
                if self.testIsPrefix(target):
                    self.parent.wine.setTargetPrefix(target, arch)
                    result = self.parent.wine.wineBoot()
                    return not result.returncode
                else:
                    QMessageBox.critical(None, "Prefix Error!", "Supplied directory is not empty, and is not a preexisting wine prefix.")
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
        folder = QFileDialog.getExistingDirectory(self, "Select wine prefix location.", options = QFileDialog.ShowDirsOnly | QFileDialog.ReadOnly)
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

    @staticmethod
    def getDialog(parent=None):
        dialog = AddPrefixDialog(parent)
        result = dialog.exec_()
        return (result == QDialog.Accepted)
