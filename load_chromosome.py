from Chromosome import Chromosome

path = input('enter chromosome path:')

print(Chromosome.load('searches_after-change/' + path + '/chromosome').get_genome())
