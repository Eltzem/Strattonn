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


# test _format_genome()

chr3 = Chromosome(_genome=[1, 5, 'adam', 0.8463234663668969, 0, 'hard_sigmoid', 0.5953261906218358, 9772, 'tanh', 0.6109872522186298, 8232, 'linear', 0.376185909443878, 0, 'hard_sigmoid', 0.943356815341254, 0, 'relu', 0.1744068805742236, 3201, 'softmax', 0.4488322860702444, 8408, 'linear', 0.9168959638316913, 1, 'sigmoid'])

sizes, activations, dropouts = chr3.hidden_layers()
if len(sizes) == 4 and len(activations) == 4 and len(dropouts) == 4:
    print('Chromosome._format_genome() hidden layer size test passed')
else:
    print('Chromosome._format_genome() hidden layer size test failed')

print('Original genome:', [1, 5, 'adam', 0.8463234663668969, 0, 'hard_sigmoid', 0.5953261906218358, 9772, 'tanh', 0.6109872522186298, 8232, 'linear', 0.376185909443878, 0, 'hard_sigmoid', 0.943356815341254, 0, 'relu', 0.1744068805742236, 3201, 'softmax', 0.4488322860702444, 8408, 'linear', 0.9168959638316913, 1, 'sigmoid'])
print('Formatted genome:', str(chr3))


# mutation test
chr4 = Chromosome()
print(str(chr4))
print('mutating')
chr4.mutate()
print(str(chr4))
