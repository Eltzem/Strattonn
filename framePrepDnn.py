import csv


class framePrepDnn:

    def __init__(self,_filesymbol):
        # Start Stop @ framelength
        self.frames = []

        filename = _filesymbol + "_data.csv"
        print("starting read of file: " + filename)

        with open(filename) as in_file:
            filelength = sum(1 for _ in in_file)


            with open(filename) as csvr:
                frame = []
                for row in csvr:
                    row = row.rstrip()
                    if(len(frame)>4):
                        frame.pop(0)
                    frame.append(row)

                    self.frames.append(frame)
