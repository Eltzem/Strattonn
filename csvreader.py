import timestep
# Converts a cvs file to a list
class csvreader():

    def __init__(self,_filename):
        self.aList = []
        i = 0
        for line in _filename:
            aline = line.split(",")
            self.aList.append(timestep.timestep(aline))
            i += 1

    def __str__(self):
        for item in self.aList:
                return str(item)