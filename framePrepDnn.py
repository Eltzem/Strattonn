import copy

class framePrepDnn:

    def framePrepDnn(_filesymbol):
        # [Volume, Trendline , Linear Regression, Hour, Minute]
        frames = []
        skipcounter = 0

        filename = _filesymbol + "_data.csv"
        print("starting read of file: " + filename)

        with open(filename) as in_file:
            with open(filename) as csvr:
                frame = []
                for row in csvr:
                    row = row.rstrip()
                    row = row.split(",")
                    map(float, row)

                    if(len(frame)>4):
                        frame.pop(0)
                    frame.append(row)
                    flatframe = [item for sublist in frame for item in sublist]
                    if skipcounter > 4:
                        frames.append(copy.copy(flatframe))
                    else:
                        skipcounter+=1
        return frames