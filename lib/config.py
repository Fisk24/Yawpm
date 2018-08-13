import os, json, getpass


class Config():

    USER = getpass.getuser()
    CONFIGBASE = "/home/{USER}/.config/Yawpm/".format(USER=USER)
    CONFIGFILE = CONFIGBASE+"Settings.json"
    PREFIXFILE = CONFIGBASE+"prefixes.csv"

    DATA = {
        "PATHS": {
            "DEFAULTPREFIX" : "/home/{USER}/.wine/".format(USER=USER),
            "WINEBOTTLES"   : "/home/{USER}/WineBottles/".format(USER=USER),
            "EXTRAFILES"    : "/home/{USER}/.local/Yawpm/Libraries/".format(USER=USER),
            "WINEVERSIONS"  : "/home/{USER}/.local/Yawpm/WineVersions/".format(USER=USER),
            "SHORTCUTDIR"   : "/home/{USER}/.local/applications/Yawpm/".format(USER=USER)
        }
    }

    def doDetectFirstTimeSetup(self):
        self.createReqFiles()

        if not os.path.isfile(Config.CONFIGFILE):
            self.save()
        if not os.path.isfile(Config.PREFIXFILE):
            self.genDefaultPrefixesCsv()

    def genDefaultPrefixesCsv(self):
        with open(Config.PREFIXFILE,"w") as prefix:
            prefix.write("Default,"+Config.DATA['PATHS']['DEFAULTPREFIX']+",win64,wine")

    def createReqFiles(self):
        os.makedirs(Config.CONFIGBASE, exist_ok=True)
        os.makedirs(Config.DATA['PATHS']['SHORTCUTDIR'], exist_ok=True)


    # Class methods receive the class name as their first argument
    # This is good for makeing changes to static variables which need their values
    # to be consistant across all instances of a class.
    # EXTRA SPICY GOOD FOR CONFIG CLASSES!!!!!!!!!!!!!!!!!!
    @classmethod
    def apply(cls, newdata):
        cls.data = newdata
        print(Config.DATA)

    def save(self):
        with open(Config.CONFIGFILE, "w") as settings:
            settings.write(json.dumps(Config.DATA))


    def load(self):
        with open(Config.CONFIGFILE, "r") as settings:
            configRaw = settings.read()
            Config.DATA = json.loads(configRaw)
