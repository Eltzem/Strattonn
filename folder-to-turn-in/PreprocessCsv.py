import csv
import numpy as np
import math
from scipy import stats
# Converts a cvs file to a list
class PreprocessCsv():

    def __init__(self,_filename):
        filepathNew = _filename[:-4] + "_data.csv"
        with open(_filename) as fOld:
            csvOld = csv.reader(fOld)
            with open(filepathNew, 'w', newline='') as fNew:
                csvNew = csv.writer(fNew)

                next(csvOld)
                pastFive = []
                previousClose = 1
                currentClose = 0

                for row in csvOld:

                    # Approximates a readable queue for calculating the trend lines
                    # If we don't have 5 items yet, we don't need to shift
                    if(pastFive.__len__()>4):
                        for i in range(4, 0, -1):
                            pastFive[i] = pastFive[i-1]
                        pastFive[0]=(row[6]) #7?
                    else:
                        pastFive.append((row[6])) #7?

                    # adding volume
                    outrow = []
                    outrow.append(row[9])

                    # Percent Change
                    pastFive = list(map(float, pastFive))
                    if len(pastFive)>1:
                        logReturns = 1000000 * (math.log(pastFive[0], 2) - math.log(pastFive[1], 2))
                        outrow.append(logReturns)
                        #percentIncrease = (pastFive[0] - pastFive[1]) / math.fabs(pastFive[0])*100
                        #outrow.append(percentIncrease)


                    # From list of stings to np array of ints
                    linearInput = np.array(pastFive)

                    # generating "time" for regression
                    np.set_printoptions(precision=5)
                    x = np.array(range(1,pastFive.__len__()+1))
                    slope, intercept, r_value, p_value, std_err = stats.linregress(x, linearInput)
                    outrow.append(slope)

                    # adding hour/minute
                    outrow.append(row[3])
                    outrow.append(row[4])

                    # add header with date
                    csvNew.writerow(outrow)

        fOld.close()
        fNew.close()
