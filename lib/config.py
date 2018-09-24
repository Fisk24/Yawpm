import os, json, getpass


class Config():

    USER = getpass.getuser()

    BASE_USER_DIR    = "/home/"+USER+"/"
    BASE_YAWPM_EXTRA = BASE_USER_DIR+".local/Yawpm/"

    CONFIGBASE = BASE_USER_DIR+".config/Yawpm/"
    CONFIGFILE = CONFIGBASE+"Settings.json"
    PREFIXFILE = CONFIGBASE+"prefixes.csv"

    DATA = {
        "PATHS": {
            "DEFAULTPREFIX" : BASE_USER_DIR+".wine/",
            "WINEBOTTLES"   : BASE_USER_DIR+"WineBottles/",
            "EXTRAFILES"    : BASE_YAWPM_EXTRA+"Libraries/",
            "WINEVERSIONS"  : BASE_YAWPM_EXTRA+"WineVersions/",
            "SCDATADIR"     : BASE_YAWPM_EXTRA+"SCData/",
            "SHORTCUTDIR"   : BASE_USER_DIR+".local/share/applications/Yawpm/"
        }
    }

    def doDetectFirstTimeSetup(self, force=False):
        self.createReqFiles()

        if force == True:
            self.save() # Save current configuration. Because this function is called before load(), The default values are writen out.
            self.genDefaultPrefixesCsv() # Reinitialize the prefix file, any existing prefixes will be forgotten but not removed from the system.
        else:
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
        os.makedirs(Config.DATA['PATHS']['SCDATADIR'], exist_ok=True)
        os.makedirs(Config.DATA['PATHS']['EXTRAFILES'], exist_ok=True)
        os.makedirs(Config.DATA['PATHS']['WINEVERSIONS'], exist_ok=True)
        os.makedirs(Config.DATA['PATHS']['WINEBOTTLES'], exist_ok=True)


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
