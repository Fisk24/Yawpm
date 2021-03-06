import csv, os

class PrefixManager():
    def __init__(self, _file="prefixes.csv"):
        self.file = _file
        self.currentIndex = 0
        self.prefixes = [] # [nick, dir, arch, exec]

    def getNick(self):
        return self.prefixes[self.currentIndex][0].strip()

    def getDir(self):
        return self.prefixes[self.currentIndex][1].strip()

    def getArch(self):
        return self.prefixes[self.currentIndex][2].strip()

    def getExec(self):
        return self.prefixes[self.currentIndex][3].strip()

    def getPrefix(self):
        return self.prefixes[self.currentIndex]

    def addPrefix(self, item):
        # [nick, dir, arch, exe]
        for prefix in self.prefixes:
            if (item[0] == prefix[0]) or (item[1] == prefix[1]):
                raise ValueError("Duplicate entries are not allowed!: {0} matches {1}".format(item, prefix))
        self.prefixes.append(item)

    def editPrefix(self, item):
        # edits a currently existing entry by replacing it entirely
        # by default this edits the currently selected prefix
        self.prefixes[self.currentIndex] = item

    def savePrefixList(self):
        with open(self.file, "w", newline='') as csvfile:
            csvwriter = csv.writer(csvfile, delimiter=",")
            for i in self.prefixes:
                csvwriter.writerow(i)

    def loadPrefixList(self):
        with open(self.file, "r", newline="\n") as prefixfile:
            csvreader = csv.reader(prefixfile, delimiter=",")
            for row in csvreader:
                self.prefixes.append(row)


