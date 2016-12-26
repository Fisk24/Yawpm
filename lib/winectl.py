import os
from subprocess import Popen, run, CalledProcessError

#### Wine controls should initiate an invisable dialog, to lock down the parent window while the control is running ####

class WineControl():
    def __init__(self, prefix="", wine="wine", arch="win32"):
        self.WINEPREFIX = prefix
        self.WINEARCH   = arch
        self.WINEEXEC   = wine

    def setTargetPrefix(self, prefix, wine, arch="win64"):
        self.WINEPREFIX = prefix
        self.WINEARCH   = arch
        self.WINEEXEC   = wine

    def openWineDrive(self):
        proc = Popen(["xdg-open", "{}/drive_c".format(self.WINEPREFIX)])

    def runInTarget(self, exe, msi=False):
        # wine msiexec /i xyz.msi
        previous = os.getcwd()
        os.chdir(os.path.dirname(exe[0]))
        if msi:
            proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    self.WINEEXEC, "msiexec", "/i"]+exe)
        else:
            proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    self.WINEEXEC]+exe)
        os.chdir(previous)

    def createWinePrefix(self):
        pass

    def wineBoot(self):
        proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    self.WINEEXEC,
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
        proc = Popen(["env", "WINEPREFIX={}".format(self.WINEPREFIX), "WINEARCH={}".format(self.WINEARCH), self.WINEEXEC, "winecfg"])
        proc.wait()

    def wineControlPanel(self):
        proc = Popen(["env", "WINEPREFIX={}".format(self.WINEPREFIX), "WINEARCH={}".format(self.WINEARCH), self.WINEEXEC, "control"])
        proc.wait()

    def wineJoyStick(self):
        proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    self.WINEEXEC, 
                    "control", "joy.cpl"])
        proc.wait()

    def wineAppWiz(self):
        proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    self.WINEEXEC, "control", "appwiz.cpl"])
        proc.wait()

    def wineInet(self):
        proc = Popen(["env", 
                    "WINEPREFIX={}".format(self.WINEPREFIX), 
                    "WINEARCH={}".format(self.WINEARCH), 
                    self.WINEEXEC, "control", "inetcpl.cpl"])
        proc.wait()

