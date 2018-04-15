from GeneticSearchDNN import GeneticSearchDNN
from Chromosome import Chromosome

gen = GeneticSearchDNN(40, 10, 15, 5, 5, _testPercentage = 0.2)


gen.searchVerbose('AAPL', 'TIME_SERIES_INTRADAY', '1min','searches_after-change/search-dnn-stock-40-10-15-5-5-5epochs-5hl-AAPL', _numberToSave=5, _generations=100, _epochs=5, _batchSize=100, _maxHL=5, _initialPopulation=None, _goodLoss = 0, _goodDA = 0.9)

