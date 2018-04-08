from GeneticSearchDNN import GeneticSearchDNN
from Chromosome import Chromosome

'''
    Conducts a genetic search using aggregated input data. Which symbols are used in the
    aggregated input data is defined in CreateAggregateInputOutputFiles.py.

    It uses aggregated data to try and predict stock price changes based on the price info
    of many companies, instead of one.
'''

numChromosomes = 40

gen = GeneticSearchDNNAll(numChromosomes, 8, 8, 8, 8, _testPercentage = 0.2)

chromosomes = []
for x in range(numChromosomes):
    c = Chromosome(_maxHL=5)
    c.get_genome()[0] = 115 # modify window size to 115, instead of 5
    chromosomes.append(c)

gen.searchVerbose('BBT', 'data/1min/3910', 'TIME_SERIES_INTRADAY', '1min','searches/search-dnn-stock-ALL3910-40-8-8-8-8-5hl', _numberToSave=5, _generations=100, _epochs=3, _batchSize=100, _maxHL=5, _initialPopulation=chromosomes, _goodLoss = 0.00007, _goodDA = 0.53)
