#Constructs an object from one line in a csv file
class timestep():

    def __init__(self, _inputlist):
        self.year = _inputlist[0]
        self.month = _inputlist[1]
        self.day = _inputlist[2]
        self.hour = _inputlist[3]
        self.minute = _inputlist[4]
        self.open = _inputlist[5]
        self.close = _inputlist[6]
        self.low = _inputlist[7]
        self.high = _inputlist[8]
        self.volume = _inputlist[9]

    def __str__(self):
        part1 = self.month + "/" + self.day + "/" + self.year + " " + self.hour + ":" + self.minute
        part2 = " " + self.open + " " + self.close + " " + self.low + " " + self.high + " " + self.volume
        return str(part1+part2)
