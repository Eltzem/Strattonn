import copy
import PreprocessCsv
import csv

class framePrepDnn:

    # Call with Stock Symbol
    def framePrepDnn(_filesymbol):
        # call PreprocessCsv.py
        # [Volume, PercentChange , Linear Regression, Hour, Minute]
        frames = []
        outputs = []
        skipcounter = 0
        PreprocessCsv.PreprocessCsv(_filesymbol + ".csv")

        filename = _filesymbol + "_data.csv"
        print("starting read of file: " + filename)

        with open(filename) as in_file:
            with open(filename) as csvr:
                frame = []
                for row in csvr:
                    row = row.rstrip()
                    row = row.split(",")
                    
                    row = list(map(float, row))

                    if(len(frame)>4):
                        frame.pop(0)
                    frame.append(row)
                    #print(row)
                    #frame.append(a)
                    #print(a)
                    flatframe = [item for sublist in frame for item in sublist]
                    if skipcounter > 4:
                        frames.append(copy.copy(flatframe))
                    else:
                        skipcounter+=1


        # Adding just the % change to an extra list: outputs
        for row in frames:
            outputs.append([float(copy.copy(row[1]))])

        return frames, outputs
