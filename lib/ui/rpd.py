from PyQt5           import uic
from PyQt5.QtGui     import *
from PyQt5.QtWidgets import *

class RemovePrefixDialog(QDialog):
    def __init__(self, parent=None):
        super(RemovePrefixDialog, self).__init__(parent)

        self.parent = parent
        self.ui = uic.loadUi("lib/ui/removeprefix.ui", self)

        ## index of prefix to be deleted ##
        self.index = self.parent.ui.prefixListWidget.currentRow()

        ### CONNECT UI ELEMENTS ###
        self.ui.removePushButton.clicked.connect(self.doRemovePrefix)

        ### POPULATE UI ELEMENTS ###
        self.populate()

    def populate(self):
        self.populatePrefixInfoLabel()

    def populatePrefixInfoLabel(self):
        nick = self.parent.manager.prefixes[self.index][0]
        path = self.parent.manager.prefixes[self.index][1] 
        arch = self.parent.manager.prefixes[self.index][2]
        self.ui.prefixInfoLabel.setText("[{nick}:{arch}] @ {path}".format(nick=nick, path=path, arch=arch))

    def doRemovePrefix(self):
        # remove the prefix that matches the one currently selected in prefixListWidget 
        self.parent.manager.prefixes.pop(self.index)
        self.parent.manager.savePrefixList()
        self.parent.populate()
        self.accept()
        
    @staticmethod
    def getDialog(parent=None):
        dialog = RemovePrefixDialog(parent)
        result = dialog.exec_()
        return (result == QDialog.Accepted)
