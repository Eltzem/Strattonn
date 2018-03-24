from Chromosome import Chromosome

genome = [1, 5, 'adam', 0.01, 0, 'hard_sigmoid', 0.5, 9772, 'tanh', 0.6, 8232, 'linear', 0.3, 0, 'hard_sigmoid', 0.9, 0, 'relu', 0.1, 3201, 'softmax', 0.4, 8408, 'linear', 0.9, 1, 'sigmoid']

chr1 = Chromosome(_genome=genome)
chr2 = None

try:
    chr1.save('/home/will/Documents/Intelligent Systems/Strattonn/chromosomes/chr1')
    chr2 = Chromosome.load('/home/will/Documents/Intelligent Systems/Strattonn/chromosomes/chr1')
except Exception as e:
    print(str(e))

success = True
for x in range(len(genome)):
    print('comaring:', chr1.get_genome()[x], 'to:', chr2.get_genome()[x])

    if chr1.get_genome()[x] != chr2.get_genome()[x]:
        print('FAILED to load correct genome. Index:', x, 'does not match')
        success = False

if success:
    print('Passed loading genome')

