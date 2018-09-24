import os, re, shutil, json

from lib.config import Config
from subprocess import run, Popen, CalledProcessError

class Shortcut():
    def __init__(self, scData=None):
        self.data = scData

    def assembleExecLine(self, info):
        print(info['prefix'][1])
        target    = info['prefix'] # Target wine prefix directory
        exec_line = "env "
        # append any environment extra variables to the exec line
        for i in info["environment"]:
            exec_line += i+" "
        # then append the standard command string, keeping in mind that the "env" is already a part of the string
        exec_line += "WINEDEBUG=-all WINEPREFIX=\"{pfx}\" {wine} \"{exe}\" {flags}".format(pfx=target[1], exe=info["Exec"], wine=target[3], flags=info["flags"])
        print(exec_line)
        return exec_line

    def execute(self):
        # Assemble command
        command = self.assembleExecLine(self.data)
        Popen(command, shell=True, cwd=os.path.dirname(self.data["Exec"]))

    @staticmethod
    def fromFile(filename):
        # Return a shortcut object based on a JSON File
        with open(filename, 'r') as sc:
            scData = sc.read()
            return Shortcut(json.loads(scData))

class ShortcutManager():
    def __init__(self, parent, user):

        self.parent = parent

        #self.systemDir = Config.DATA['PATHS']['SHORTCUTDIR']
        #self.localDir  = Config.DATA['PATHS']['SCDATADIR']
        self.shortcuts = [] # The master list of all scanned shortcuts
        self.scDataTemplate = {
            'Name': 'Name',
            'Comment': 'Shortcut Created by Yawpm (Yet Another Wine Prefix Manager)',
            'Exec': '/home/fisk/WineBottles/bnet64/drive_c/windows/explorer.exe',
            'Icon': 'icon file name',
            'Terminal': 'false',
            'Type': 'Application',
            'Categories': 'Games;Wine;',
            'start': './',
            'prefix': 0,
            'flags': '--derp',
            'environment': []
        }

    def addShortcut(self, info):
        # Create .desktop file and copy it into the appropriate directories
        # Shortcut Data is passed in the form of a dictionary: {}
        newShortcut = Shortcut(info)
        self.shortcuts.append(newShortcut)

        fileBaseName = self.legalize(info["Name"])
        fullPathJson = Config.DATA["PATHS"]["SCDATADIR"]+fileBaseName+".json"
        print("Added shortcut data:", fullPathJson)
        self.writeJsonFile(info, fullPathJson)

    def distributeDesktopFiles(self, filename):
        shutil.copyfile(self.localDir+filename, self.systemDir+filename)

    def writeJsonFile(self, data, filename):
        with open(filename, 'w') as shortcut:
            shortcut.write(json.dumps(data))

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

    def delShortcut(self, index):
        filename = self.shortcuts[index]["filename"]
        print("Deleted shortcut: {}".format(filename))
        try:
            os.remove(self.systemDir+filename)
        except FileNotFoundError as e:
            print("The system shortcut does not appear to exist in the file system...")

    def scanShortcuts(self):
        # parse the desktop files located in the given directory, into a list of dictionaries
        sclist = []
        localDir = Config.DATA["PATHS"]["SCDATADIR"]
        for short in os.listdir(localDir):
            if short.endswith(".json"):
                #print(os.path.abspath(short))
                #print(short)

                sclist.append(Shortcut.fromFile(localDir+short))

        self.shortcuts = sclist

    '''
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

    '''

    def legalize(self, x):
        # *NEW* Easy How To Install Brutal Doom V19 With Extras 11/05/13
        ILLEGAL= [['\u2665', ""], [" ","_"], [":", ""], ["/", "_"], ["\\", "_"], ["\"", "_"], ["?", ""], ["*", ""], ["|", "_"],[",", ""]]
        for i in ILLEGAL:
            x = x.replace(i[0], i[1])
        return x
