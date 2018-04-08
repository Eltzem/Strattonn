import csv
import os
import os.path

if __name__ == '__main__':
    masterFile = csv.writer(open('data/1min/MASTER.csv', 'w'))

    for filename in os.listdir('data/1min'):
        first = False

        if 'csv' in filename and not 'MASTER' in filename and not '_' in filename \
                and not 'back' in filename and not '3910' in filename:
            fromFile = csv.reader(open('data/1min/' + filename))
        
            firstLine = next(fromFile)

            if first:
                masterFile.writerow(firstLine)
                first = True
            
            for line in fromFile:
                masterFile.writerow(line)

