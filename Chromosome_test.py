from Chromosome import Chromosome

chromosomes = []
for x in range(10):
    newChromosome = Chromosome()
    chromosomes.append(newChromosome)
    print(newChromosome)
    print()

chr1 = Chromosome([3, 3, 0, 4, 1])
sizes, activations, dropouts = chr1.hidden_layers()
if len(sizes) == 6 and len(activations) == 6 and len(dropouts) == 6:
    print('Chromosome.hidden_layer() size test passed')
    print(sizes)
    print(activations)
    print(dropouts)


chr1 = Chromosome([0], 1)
sizes, activations, dropouts = chr1.hidden_layers()
if len(sizes) == 1 and len(activations) == 1 and len(dropouts) == 1:
    print('Chromosome.hidden_layer() size test passed')
    print(sizes)
    print(activations)
    print(dropouts)
