from GeneticSearchDNN import GeneticSearchDNN
from Chromosome import Chromosome

# creates a GeneticSearchDNN object

# population = 40
# selection = 8
# mutation = 8
# newblood = 4
# crossover pairs = 10
# testing on 20% of the data
gen = GeneticSearchDNN(40, 8, 8, 4, 10, _testPercentage = 0.2)


# start the genetic search

# stock symbol = VTI
# time series = TIME_SERIES_INTRADAY
# time interval = 1min
# directory to save best models in = searches/search-dnn-stock-40-8-8-4-10-5epochs-5hl-VTI
# save the 5 best models of each generation
# run searcch for 100 generations
# batch size for data = 100
# maximum hidden layers for each network = 5
gen.searchVerbose('VTI', 'TIME_SERIES_INTRADAY', '1min','searches/search-dnn-stock-40-8-8-4-10-5epochs-5hl-VTI', _numberToSave=5, _generations=100, _epochs=5, _batchSize=100, _maxHL=5, _initialPopulation=None, _goodLoss = 0, _goodDA = 0.9)
