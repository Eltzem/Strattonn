from array import array

import timestep
import csv
import numpy as np
import math
from scipy import stats
# Converts a cvs file to a list
class csvreader():

    def __init__(self,_filename):
        filepathNew = _filename + "_data.csv"
        with open(_filename) as fOld:
            csvOld = csv.reader(fOld)
            with open(filepathNew, 'w') as fNew:
                csvNew = csv.writer(fNew)

                next(csvOld)
                pastFive = []

                for row in csvOld:

                    # Approximates a readable queue for calculating the trend lines
                    # If we don't have 5 items yet, we don't need to shift
                    if(pastFive.__len__()>4):
                        for i in range(4, 0, -1):
                            pastFive[i] = pastFive[i-1]
                        pastFive[0]=(row[7])
                    else:
                        pastFive.append((row[7]))

                    outrow = []

                    pastFive = list(map(float, pastFive))
                    if len(pastFive)>1:
                        percentIncrease = (pastFive[0] - pastFive[1]) / math.fabs(pastFive[0])*100
                        outrow.append(percentIncrease)


                    # From list of stings to np array of ints
                    linearInput = np.array(pastFive)

                    # generating "time" for regression
                    x = np.array(range(1,pastFive.__len__()+1))
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x, linearInput)
                    outrow.append(slope)

                    # add header with date
                    csvNew.writerow(outrow)

        fOld.close()
        fNew.close()