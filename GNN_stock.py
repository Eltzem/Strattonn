from GeneticSearchDNN import GeneticSearchDNN
from Chromosome import Chromosome

for x in range(5, 6):
    try:
        gen = GeneticSearchDNN(100, 30, 15, 15, 20)
        gen.searchVerbose('VTI', 'TIME_SERIES_INTRADAY', '1min','search-dnn-stock-100-30-15-15-20-' + str(x) + 'hl', _numberToSave=5, _generations=25, _epochs=3, _batchSize=100, _initialPopulation=None, _maxHL=x, _goodLoss = 0.01, _goodDA = 0.53)
    except Exception as e:
        print('Exception found in hlsize = ', x)
        print(e)
'''
for x in range(2, 10):
    try:
        gen = GeneticSearchDNN(100, 30, 15, 15, 20)
        gen.searchVerbose('VTI', 'TIME_SERIES_INTRADAY', '1min','/media/will/data-160/search-dnn-stock-100-30-15-15-20-' + str(x) + 'hl', _numberToSave=5, _generations=25, _epochs=3, _batchSize=100, _initialPopulation=None, _maxHL=x, _goodLoss = 0.01, _goodDA = 0.53)
    except Exception as e:
        print('Exception found in hlsize = ', x)
        print(e)
'''
#gen = GeneticSearchDNN(10, 2, 2, 2, 2)
#gen = GeneticSearchDNN(100, 30, 15, 15, 20)

#startingPopulation = []


'''
startingPopulation.append(Chromosome(_genome=[28, 28, 'adam', 0, 500, 'sigmoid', 0, 500, 'sigmoid', 0, 500, 'sigmoid', 0, 0, 'hard_sigmoid', 0.4397462817710124, 0, 'hard_sigmoid', 0.3138025771867151, 0, 'softplus', 0.5779566775052997, 0, 'linear', 0.8054541031099068, 10, 'sigmoid']))
startingPopulation.append(Chromosome(_genome=[28, 28, 'rmsprop', 0, 500, 'sigmoid', 0, 500, 'sigmoid', 0, 500, 'sigmoid', 0, 0, 'hard_sigmoid', 0.4397462817710124, 0, 'hard_sigmoid', 0.3138025771867151, 0, 'softplus', 0.5779566775052997, 0, 'linear', 0.8054541031099068, 10, 'sigmoid']))
startingPopulation.append(Chromosome(_genome=[28, 28, 'adam', 0, 200, 'sigmoid', 0, 500, 'sigmoid', 0, 800, 'sigmoid', 0, 0, 'hard_sigmoid', 0.4397462817710124, 0, 'hard_sigmoid', 0.3138025771867151, 0, 'softplus', 0.5779566775052997, 0, 'linear', 0.8054541031099068, 10, 'sigmoid']))
startingPopulation.append(Chromosome(_genome=[28, 28, 'adam', 0, 500, 'sigmoid', 0, 500, 'elu', 0, 500, 'relu', 0, 0, 'hard_sigmoid', 0.4397462817710124, 0, 'hard_sigmoid', 0.3138025771867151, 0, 'softplus', 0.5779566775052997, 0, 'linear', 0.8054541031099068, 10, 'sigmoid']))
startingPopulation.append(Chromosome(_genome=[28, 28, 'adam', 0, 500, 'softmax', 0, 500, 'sigmoid', 0, 500, 'softplus', 0, 0, 'hard_sigmoid', 0.4397462817710124, 0, 'hard_sigmoid', 0.3138025771867151, 0, 'softplus', 0.5779566775052997, 0, 'linear', 0.8054541031099068, 10, 'sigmoid']))
'''

'''
for x in range(3):
    startingPopulation.append(Chromosome())
'''
#gen.searchVerbose('search-dnn-mnist-1', 5, 5, 2, 1000, _initialPopulation=None, _maxHL=4)
#gen.searchVerbose('VTI', 'TIME_SERIES_INTRADAY', '1min','/media/will/data-160/search-dnn-stock-100-30-15-15-20-3hl', _numberToSave=5, _generations=100, _epochs=3, _batchSize=100, _initialPopulation=None, _maxHL=3, _goodLoss = 0.01, _goodDA = 0.53)
