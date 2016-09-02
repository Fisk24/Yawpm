import os
from subprocess import Popen

class WineControl():
    def __init__(self, prefix="", arch="win32"):
        self.WINEPREFIX = prefix
        self.WINEARCH   = arch

    def setTargetPrefix(self, prefix, arch="win32"):
        self.WINEPREFIX = prefix
        self.WINEARCH   = arch

    def runInTarget(self, exe):
        previous = os.getcwd()
        os.chdir(os.path.dirname(exe[0]))
        proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    "wine"]+exe)
        os.chdir(previous)

    def createWinePrefix(self):
        pass

    def wineBoot(self):
        proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    "wineboot"])
        proc.wait()

    def wineCfg(self):
        proc = Popen(["env", "WINEPREFIX={}".format(self.WINEPREFIX), "WINEARCH={}".format(self.WINEARCH), "winecfg"])
        proc.wait()

    def wineControlPanel(self):
        proc = Popen(["env", "WINEPREFIX={}".format(self.WINEPREFIX), "WINEARCH={}".format(self.WINEARCH), "wine", "control"])
        proc.wait()

    def wineJoyStick(self):
        proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    "wine", "control", "joy.cpl"])
        proc.wait()

    def wineAppWiz(self):
        proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    "wine", "control", "appwiz.cpl"])
        proc.wait()

    def wineInet(self):
        proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    "wine", "control", "inetcpl.cpl"])
        proc.wait()

