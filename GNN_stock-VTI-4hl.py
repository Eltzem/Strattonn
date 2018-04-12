from GeneticSearchDNN import GeneticSearchDNN
from Chromosome import Chromosome
'''
for x in range(5, 6):
    try:
        gen = GeneticSearchDNN(100, 30, 15, 15, 20)
        gen.searchVerbose('VTI', 'TIME_SERIES_INTRADAY', '1min','search-dnn-stock-100-30-15-15-20-' + str(x) + 'hl', _numberToSave=5, _generations=25, _epochs=3, _batchSize=100, _initialPopulation=None, _maxHL=x, _goodLoss = 0.004, _goodDA = 0.53)
    except Exception as e:
        print('Exception found in hlsize = ', x)
        print(e)

for x in range(2, 10):
    try:
        gen = GeneticSearchDNN(100, 30, 15, 15, 20)
        gen.searchVerbose('VTI', 'TIME_SERIES_INTRADAY', '1min','/media/will/data-160/search-dnn-stock-100-30-15-15-20-' + str(x) + 'hl', _numberToSave=5, _generations=25, _epochs=3, _batchSize=100, _initialPopulation=None, _maxHL=x, _goodLoss = 0.01, _goodDA = 0.53)
    except Exception as e:
        print('Exception found in hlsize = ', x)
        print(e)
'''

'''
    Chromosome from the high requency trading article:
    startingPopulation.append(Chromosome(_genome=[5, 5, 'adam', 0.01, 13, 'tanh', 0, 10, 'tanh', 0, 6, 'tanh', 0, 3, 'tanh', 0, 1, 'linear'], _maxHL=4))
'''

#gen = GeneticSearchDNN(1, 1, 0, 0, 0, _testPercentage = 0.2)
#gen = GeneticSearchDNN(10, 2, 2, 2, 2, _testPercentage = 0.2)
#gen = GeneticSearchDNN(40, 4, 12, 12, 6, _testPercentage = 0.2)
gen = GeneticSearchDNN(40, 8, 8, 4, 10, _testPercentage = 0.2)

#startingPopulation = []
#for x in range(1):
#    startingPopulation.append(Chromosome(_genome=[5, 5, 'adam', 0.01, 20, 'relu', 0, 20, 'relu', 0, 20, 'relu', 0, 20, 'relu', 0, 1, 'relu'], _maxHL=4))


#gen.searchVerbose('VTI', 'TIME_SERIES_INTRADAY', '1min', 'search-dnn-VTI-short', _numberToSave=1, _generations=1, _epochs=100, _batchSize=10, _maxHL=4, _initialPopulation=startingPopulation)

#gen.searchVerbose('VTI', 'TIME_SERIES_INTRADAY', '1min', 'search-dnn-VTI-short', _numberToSave=5, _generations=5, _epochs=2, _batchSize=100, _maxHL=4, _initialPopulation=startingPopulation, _goodLoss = 0.005, _goodDA = 0.53)

#gen.searchVerbose('VTI', 'TIME_SERIES_INTRADAY', '1min','search-dnn-stock-40-4-12-12-6-5hl', _numberToSave=5, _generations=100, _epochs=3, _batchSize=100, _maxHL=5, _initialPopulation=None, _goodLoss = 0.01, _goodDA = 0.53)

gen.searchVerbose('VTI', 'TIME_SERIES_INTRADAY', '1min','searches_after-change/search-dnn-stock-40-8-8-4-10-5epochs-4hl-VTI', _numberToSave=5, _generations=100, _epochs=5, _batchSize=100, _maxHL=4, _initialPopulation=None, _goodLoss = 0, _goodDA = 0.9)
