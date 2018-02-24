import timestep


# Converts a cvs file to a list
class csvreader():

    def __init__(self, _filename):
        source = open(_filename, "r")
        self.aList = []
        global aList;
        i = 0
        for line in source:
            aline = line.split(",")
            self.aList.append(timestep.timestep(aline))
            i += 1
        self.aList.append("\n")

        temp = 'trendlines_' + _filename + '.txt'
        target = open('temp', 'w')

    def str_print(self):
        for item in self.aList:
            print(str(self.aList[item]))

    def data_calculator(self, target, filename):
        for line in target:
            self.aList[i]

# linear trendline 5 timesteps
# ln trendline
