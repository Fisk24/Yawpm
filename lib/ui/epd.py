import os

from PyQt5           import uic
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *
from lib.ui.apd      import AddPrefixDialog

class EditPrefixDialog(AddPrefixDialog):
    def __init__(self, parent):
        super(EditPrefixDialog, self).__init__(parent) 
        # populate the gui
        self.populate()

    def populate(self):
        self.ui.setWindowTitle("Edit Prefix")
        self.addPushButton.setText("Accept")
        self.nickNameLineEdit.setText(self.parent.manager.getNick())
        self.newWineLineEdit.setText(self.parent.manager.getExec())
        self.selectPrefixPushButton.setText(self.parent.manager.getDir())
        self.prefixLocation = self.parent.manager.getDir()
        #self.archComboBox.setCurrentText(self.parent.manager.getArch())
        if self.parent.manager.getArch() == "win32":
            self.archComboBox.setCurrentIndex(0)
        else:
            self.archComboBox.setCurrentIndex(1)

        if self.parent.manager.getExec() != "wine":
            self.doNewWineCheckBox.setChecked(True)

    def acceptValues(self, nick, pref, arch, wine):
        newValues = [nick, pref, arch, wine]
        self.parent.manager.editPrefix(newValues)
        self.parent.manager.savePrefixList()
        self.parent.populatePrefixList()
        self.parent.updatePrefixInfo()
        self.accept()

    @staticmethod
    def getDialog(parent=None):
        dialog = EditPrefixDialog(parent)
        result = dialog.exec_()
        return (result == QDialog.Accepted)
