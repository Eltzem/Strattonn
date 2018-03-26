from GeneticSearchDNN import GeneticSearchDNN
from Chromosome import Chromosome

gen = GeneticSearchDNN(10, 2, 2, 2, 2)
#gen = GeneticSearchDNN(3, 3, 0, 0, 0)
startingPopulation = []


'''
startingPopulation.append(Chromosome(_genome=[28, 28, 'adam', 0, 500, 'sigmoid', 0, 500, 'sigmoid', 0, 500, 'sigmoid', 0, 0, 'hard_sigmoid', 0.4397462817710124, 0, 'hard_sigmoid', 0.3138025771867151, 0, 'softplus', 0.5779566775052997, 0, 'linear', 0.8054541031099068, 10, 'sigmoid']))
startingPopulation.append(Chromosome(_genome=[28, 28, 'rmsprop', 0, 500, 'sigmoid', 0, 500, 'sigmoid', 0, 500, 'sigmoid', 0, 0, 'hard_sigmoid', 0.4397462817710124, 0, 'hard_sigmoid', 0.3138025771867151, 0, 'softplus', 0.5779566775052997, 0, 'linear', 0.8054541031099068, 10, 'sigmoid']))
startingPopulation.append(Chromosome(_genome=[28, 28, 'adam', 0, 200, 'sigmoid', 0, 500, 'sigmoid', 0, 800, 'sigmoid', 0, 0, 'hard_sigmoid', 0.4397462817710124, 0, 'hard_sigmoid', 0.3138025771867151, 0, 'softplus', 0.5779566775052997, 0, 'linear', 0.8054541031099068, 10, 'sigmoid']))
startingPopulation.append(Chromosome(_genome=[28, 28, 'adam', 0, 500, 'sigmoid', 0, 500, 'elu', 0, 500, 'relu', 0, 0, 'hard_sigmoid', 0.4397462817710124, 0, 'hard_sigmoid', 0.3138025771867151, 0, 'softplus', 0.5779566775052997, 0, 'linear', 0.8054541031099068, 10, 'sigmoid']))
startingPopulation.append(Chromosome(_genome=[28, 28, 'adam', 0, 500, 'softmax', 0, 500, 'sigmoid', 0, 500, 'softplus', 0, 0, 'hard_sigmoid', 0.4397462817710124, 0, 'hard_sigmoid', 0.3138025771867151, 0, 'softplus', 0.5779566775052997, 0, 'linear', 0.8054541031099068, 10, 'sigmoid']))
'''

for x in range(3):
    startingPopulation.append(Chromosome())

gen.searchVerbose('search-dnn-mnist-1', 5, 5, 2, 1000, _initialPopulation=None, _maxHL=4)
#gen.searchVerbose('search-dnn-mnist-1', 3, 2, 2, 1000, _initialPopulation=None, _maxHL=4)
