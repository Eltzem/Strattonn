import csv
import os
import os.path

if __name__ == '__main__':
    masterFile = csv.writer(open('data/1min/MASTER.csv', 'w'))

    for filename in os.listdir():
        first = False

        if 'csv' in filename and filename != 'MASTER.csv' and not '_' in filename:
            fromFile = csv.reader(open('data/1min/' + filename))
        
            firstLine = next(fromFile)

            if first:
                masterFile.writerow(firstLine)
                first = True
            
            for line in fromFile:
                masterFile.writerow(line)

