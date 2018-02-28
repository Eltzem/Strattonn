from Chromosome import Chromosome

chromosomes = []
for x in range(10):
    newChromosome = Chromosome()
    chromosomes.append(newChromosome)
    print(newChromosome)
    print()

chr1 = Chromosome(_hlSizes=[3, 3, 0, 4, 1], _hlActivations=['elu', 'softmax'], _hlDropouts=[0.5, 0.01])
sizes, activations, dropouts = chr1.hidden_layers()
if len(sizes) == 6 and len(activations) == 6 and len(dropouts) == 6:
    print('Chromosome.hidden_layer() size test passed')
else:
    print('size test failed')
print(sizes)

if activations[0] == 'elu' and activations[1] == 'softmax':
    print('Chromosome.hidden_layer() activation test passed')
else:
    print('activation test failed')
print(activations)

if dropouts[0] == 0.5 and dropouts[1] == 0.01:
    print('Chromosome.hidden_layer() dropout test passed')
else:
    print('dropout test failed')
print(dropouts)

chr1 = Chromosome(_hlSizes=[0], _maxHL=1)
sizes, activations, dropouts = chr1.hidden_layers()
if len(sizes) == 1 and len(activations) == 1 and len(dropouts) == 1:
    print('Chromosome.hidden_layer() size test passed')
    print(sizes)
    print(activations)
    print(dropouts)
else:
    print('size test failed')
