from GeneticSearchDNN import GeneticSearchDNN
from Chromosome import Chromosome

gen = GeneticSearchDNN(20, 4, 2, 4, 5, _testPercentage = 0.05)


gen.searchVerbose('MASTER', 'TIME_SERIES_INTRADAY', '1min','searches/search-dnn-stock-MASTER-20-4-2-4-5-5hl', _numberToSave=5, _generations=100, _epochs=10, _batchSize=10000, _maxHL=5, _initialPopulation=None, _goodLoss = 0.00007, _goodDA = 0.53)
