import os, re, shutil
from subprocess import run, Popen, CalledProcessError

class ShortcutManager():
    def __init__(self, parent, user):

        self.parent = parent

        self.systemDir = "/home/{user}/.local/share/applications/".format(user=user)
        self.localDir = "/home/{user}/.config/Yawpm/shortcuts/".format(user=user)
        self.shortcuts = [] # The master list of all scanned shortcuts

    def addShortcut(self, info):
        # Create .desktop file and copy it into the appropriate directories
        # Note: consider seperating the shortcut file writing code to its own method
        print("Conpiling keys for shortcut")

        filename = self.legalize(info["Name"])+".desktop"

        print("File name is {}".format(filename))

        # breifly before we overwrite the Exec line with the final information
        # we utilize the supplied executable file location to derive the
        # starting directory
        starts_in = os.path.dirname(info["Exec"])
        info["Exec"] = self.assembleExecLine(info)

        self.initializeDesktopFile(self.localDir+filename)
        self.writeDesktopFile(info, starts_in, self.localDir+filename)
        self.distributeDesktopFiles(filename)

    def distributeDesktopFiles(self, filename):
        shutil.copyfile(self.localDir+filename, self.systemDir+filename)

    def writeDesktopFile(self, info, start, filename):
    	with open(filename, "a") as shortcut:
    		for key in info:
    			# excluding metadata tags, write all shortcut tags into the file
    			if (key != "start") and (key != "prefix") and (key != "flags") and (key != "environment"):
    				shortcut.write("{k}={v}\n".format(k=key, v=info[key]))
    			elif key == "start":
    				shortcut.write("Path={v}".format(v=start))

    def initializeDesktopFile(self, filename):
        with open(filename, "w") as desktop:
            desktop.write("[Desktop Entry]\n")

    def assembleExecLine(self, info):
        prefixes  = self.parent.manager.prefixes # list of all wine prefixes
        target    = prefixes[info["prefix"]] # Target wine prefix
        exec_line = "env "
        # append any environment extra variables to the exec line
        for i in info["environment"]:
            exec_line += i+" "
        # then append the standard command string, keeping in mind that the "env" is already a part of the string
        exec_line += "WINEDEBUG=fixme-all WINEPREFIX=\"{pfx}\" {wine} \"{exe}\" {flags}".format(pfx=target[1], exe=info["Exec"], wine=target[3], flags=info["flags"])
        print(exec_line)
        return exec_line

    def delShortcut(self, index):
        filename = self.shortcuts[index]["filename"]
        print("Deleted shortcut: {}".format(filename))
        try:
            os.remove(self.systemDir+filename)
        except FileNotFoundError as e:
            print("The system shortcut does not appear to exist in the file system...")
        try:
            os.remove(self.localDir+filename)
        except FileNotFoundError as e:
            print("The local shortcut does not appear to exist in the file system...")

    def launchShortcut(self, index):
        print(index)
        # env WINEPREFIX="/home/fisk/Wine Prefixes/League_of_Legends/" wine "/home/fisk/Wine Prefixes/League_of_Legends/drive_c/Riot Games/League of Legends/lol.launcher.exe"
        #os.system(self.shortcuts[index]["Exec"])
        # Its difficult to parse a string into a list of arguments. (Directories could contain spaces and would be split into diffrent list entries)
        # Insted try to pass the whole Exec line of the shortcut as an argument to bash
        os.chdir(self.shortcuts[index]["Path"])
        Popen(self.shortcuts[index]["Exec"], shell=True)

    def scanShortcuts(self):
        # parse the desktop files located in the given directory, into a list of dictionaries
        sclist = []
        for short in os.listdir(self.localDir):
            if short.endswith(".desktop"):
                #print(os.path.abspath(short))
                #print(short)
                sclist.append(self.parseShort(self.localDir, short))

        self.shortcuts = sclist

    def parseShort(self, directory, filename):
        # Translate desktop files into a dictionary then return the dictionary
        short = directory+filename
        scinfo = {}
        scinfo["filename"] = filename
        with open(short, "r") as sc:
            for line in sc.readlines():
                if "[Desktop Entry]" not in line:
                    x = line.split("=")
                    key   = x[0]
                    value = re.sub("("+x[0]+"=|\\n)", "", line)
                    scinfo[key] = value

        #print(scinfo)
        return scinfo

    def legalize(self, x):
        # *NEW* Easy How To Install Brutal Doom V19 With Extras 11/05/13
        ILLEGAL= [['\u2665', ""], [" ","_"], [":", ""], ["/", "_"], ["\\", "_"], ["\"", "_"], ["?", ""], ["*", ""], ["|", "_"],[",", ""]]
        for i in ILLEGAL:
            x = x.replace(i[0], i[1])
        return x
