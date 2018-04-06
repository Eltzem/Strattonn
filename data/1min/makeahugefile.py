import csv
import os
import os.path

if __name__ == '__main__':
    masterFile = csv.writer(open('MASTER.csv', 'w'))

    for filename in os.listdir():
        first = False

        if 'csv' in filename and filename != 'MASTER.csv' and not '_' in filename:
            fromFile = csv.reader(open(filename))
        
            firstLine = next(fromFile)

            if first:
                masterFile.writerow(firstLine)
                first = True
            
            for line in fromFile:
                masterFile.writerow(line)

