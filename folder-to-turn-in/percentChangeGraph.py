import PreprocessCsv
import csv
import numpy as np
import matplotlib.pyplot as plt


# Generates a histogram of the percent change of a stock
# Call with Stock Symbol
def graph(_filesymbol):
    # [Volume, PercentChange , Linear Regression, Hour, Minute]
    PreprocessCsv.PreprocessCsv(_filesymbol + ".csv")

    filename = _filesymbol + "_data.csv"
    print("starting read of file: " + filename)
    percentChanges = []
    with open(filename) as in_file:
        with open(filename) as csvr:
            csvReader = csv.reader(csvr)
            next(csvReader)
            for row in csvReader:
                print(row)
                print(type(row))
                print(row[1])
                percentChanges.append(row[1])
    print(percentChanges)
    percentChanges = rejectOutliers(list(map(float, percentChanges)))
    a = np.histogram(percentChanges)
    plt.hist(a, bins='auto')
    plt.title(_filesymbol)
    plt.show()

# INX / MSI index
# AAPL
def rejectOutliers(data):
    m = 2
    x = np.mean(data)
    s = np.std(data)
    filtered = [e for e in data if (x-2*s < e < x+2*s)]
    return filtered
