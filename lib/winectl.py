import os
from subprocess import Popen, run, CalledProcessError

#### Wine controls should initiate an invisable dialog, to lock down the parent window while the control is running ####

class WineControl():
    def __init__(self, prefix="", arch="win32"):
        self.WINEPREFIX = prefix
        self.WINEARCH   = arch

    def setTargetPrefix(self, prefix, arch="win64"):
        self.WINEPREFIX = prefix
        self.WINEARCH   = arch

    def openWineDrive(self):
        proc = Popen(["xdg-open", "{}/drive_c".format(self.WINEPREFIX)])

    def runInTarget(self, exe, msi=False):
        # wine msiexec /i xyz.msi
        previous = os.getcwd()
        if msi:
            proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    "wine", "msiexec", "/i"]+exe)
        else:
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

        # return CompletedProcess object
        return proc

    def winetricks(self):
        proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    "winetricks"])
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

