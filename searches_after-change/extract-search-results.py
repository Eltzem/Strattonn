import os
import csv

if __name__ == '__main__':

    # for each search
    searchFolders = os.listdir()
    searchFolders.remove('extract-search-results.py')
    for searchFolder in searchFolders:
        os.chdir(searchFolder)

        # holds results of search
        resultsCSV = csv.writer(open('results.csv', 'w'))
        
        resultsCSV.writerow(['epoch', 'best', 'second best', 'third best', \
                                'fourth best', 'fifth best'])

        epochCount = 0
        # for each epoch
        epochFolders = os.listdir()
        epochFolders.remove('results.csv')

        # sort epoch folders
        for x in range(len(epochFolders)):
            epochFolders[x] = int(epochFolders[x])
        epochFolders = sorted(epochFolders)

        for x in range(len(epochFolders)):
            #print(epochFolders)
            os.chdir(str(epochFolders[x]))

            newRow = [epochCount]
            
            da = [] # hold directional accuracies
            for modelFolder in os.listdir():
                da.append(float(modelFolder[modelFolder.index('_', 10) + 1 : ]))
            
            da = sorted(da, reverse=True) # sort directional accuracies
            newRow += da # add to new row that will be appended to csv

            resultsCSV.writerow(newRow)

            epochCount += 1

        # back out of search and epoch directories
            os.chdir('..')
        os.chdir('..')


