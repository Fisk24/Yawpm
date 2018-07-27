import os, getpass

USER = getpass.getuser()
CONFIGROOT = "/home/{user}/.config/Yawpm/".format(user=USER)
SHORTCUT   = CONFIGROOT+"shortcuts"
PREFIXCSV  = CONFIGROOT+"prefixes.csv"
CONFIGFILE = CONFIGROOT+"Settings.json"
DEFAULTPREFIX = "/home/{user}/.wine".format(user=USER)
