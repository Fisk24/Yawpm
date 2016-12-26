import os, re

class ShortcutManager():
    def __init__(self, user):
        self.systemDir = "/home/{user}/.local/share/applications/".format(user=user)
        self.localDir = "/home/{user}/.config/Yawpm/shortcuts/".format(user=user)
        self.shortcuts = []

    def addShortcut(self):
        pass

    def delShortcut(self):
        pass

    def scanShortcuts(self):
        # parse the desktop files located in the given directory, into a list of dictionaries
        sclist = []
        for short in os.listdir(self.localDir):
            print(os.path.abspath(short))
            print(short)
            sclist.append(self.parseShort(self.localDir+"/"+short))

        self.shortcuts = sclist

    def parseShort(self, short):
        # Translate desktop files into a dictionary then return the dictionary
        with open(short, "r") as sc:
            scinfo = {}
            for line in sc.readlines():
                if "[Desktop Entry]" not in line:
                    x = line.split("=")
                    key   = x[0]
                    value = re.sub("("+x[0]+"=|\\n)", "", line)
                    scinfo[key] = value

        print(scinfo)
        return scinfo 
