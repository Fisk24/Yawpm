import os, getpass

USER = getpass.getuser()
CONFIGROOT = "/home/{user}/.config/Yawpm/".format(user=USER)
SHORTCUT   = CONFIGROOT+"shortcuts"
PREFIXCSV  = CONFIGROOT+"prefixes.csv"
DEFAULTPREFIX = "/home/{user}/.wine".format(user=USER)

def genDefaultPrefixesCsv():
    if not os.path.isfile(PREFIXCSV):
        with open(PREFIXCSV,"w") as prefix:
            prefix.write("Default,"+DEFAULTPREFIX+",win64")

def createReqFiles():
    os.makedirs(CONFIGROOT, exist_ok=True)
    os.makedirs(SHORTCUT, exist_ok=True)

def doOnStart():
    createReqFiles()
    genDefaultPrefixesCsv()

doOnStart()
