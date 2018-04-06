from GeneticSearchDNN import GeneticSearchDNN as GSD
from DNN import DNN
from Chromosome import Chromosome
from Paths import get_path_slash

def create_model (_chromosome):
    dnn = DNN(_chromosome=_chromosome)
    print(dnn.get_model().summary())
    return dnn

def create_train_test_save_model (_chromosome):
    dnn = create_model(_chromosome)

    trainInputs, trainOutputs, testInputs, testOutputs = \
            GSD.load_training_and_testing_data(0.2, 'MASTER', 'TIME_SERIES_INTRADAY', '1min')

    dnn.compile(_chromosome.optimizer(), 'mean_squared_error')

    dnn.train(trainInputs, trainOutputs, 10, 1000)

    error = dnn.evaluate(testInputs, testOutputs)
    da = dnn.evaluate_directional_accuracy(testInputs, testOutputs)

    dnn.save('dnn' + get_path_slash() + str(da) + '_' + str(error))

    dnn.close()

    print()
    print('mean squared error:', error)
    print('directional accuracy:', da)
    print()

    return error, da



if __name__ == '__main__':

    print((create_train_test_save_model(Chromosome(_genome=[5, 5, 'nadam', 0.01, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 1, 'linear'], _maxHL=5)))
    '''
    NOTE: this code was used to find the best hidden layer count. Results were mixed.
    results = []
    results.append(create_train_test_save_model(Chromosome(_genome=[5, 5, 'nadam', 0.01, 20, 'tanh', 0, 20, 'tanh', 0, 1, 'linear'], _maxHL=2)))
    results.append(create_train_test_save_model(Chromosome(_genome=[5, 5, 'nadam', 0.01, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 1, 'linear'], _maxHL=3)))
    results.append(create_train_test_save_model(Chromosome(_genome=[5, 5, 'nadam', 0.01, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 1, 'linear'], _maxHL=4)))
    results.append(create_train_test_save_model(Chromosome(_genome=[5, 5, 'nadam', 0.01, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 1, 'linear'], _maxHL=5)))
    results.append(create_train_test_save_model(Chromosome(_genome=[5, 5, 'nadam', 0.01, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 1, 'linear'], _maxHL=6)))
    results.append(create_train_test_save_model(Chromosome(_genome=[5, 5, 'nadam', 0.01, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 1, 'linear'], _maxHL=7)))
    results.append(create_train_test_save_model(Chromosome(_genome=[5, 5, 'nadam', 0.01, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 1, 'linear'], _maxHL=8)))
    results.append(create_train_test_save_model(Chromosome(_genome=[5, 5, 'nadam', 0.01, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 1, 'linear'], _maxHL=9)))
    results.append(create_train_test_save_model(Chromosome(_genome=[5, 5, 'nadam', 0.01, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 20, 'tanh', 0, 1, 'linear'], _maxHL=10)))
    
    print(results)
    '''

    '''
    NOTE: This code was used to find the best optimizer. Results were mixed.

    d = Chromosome()
    results = {}
    for optimizer in d.possibleOptimizers:
        c = Chromosome(_genome=[5, 5, optimizer, 0.01, 20, 'softplus', 0, 20, 'softplus', 0, 20, 'softplus', 0, 20, 'softplus', 0, 20, 'softplus', 0, 1, 'linear'], _maxHL=5)
        
        # uses high frequency trading paper config
        #c = Chromosome(_genome=[5, 5, optimizer, 0.01, 25, 'softplus', 0, 20, 'softplus', 0, 15, 'softplus', 0, 10, 'softplus', 0, 5, 'softplus', 0, 1, 'linear'], _maxHL=5)
        
        error, da = create_train_test_save_model(c)
        results[optimizer] = [error, da]

    for optimizerKey in results:
        print('\n\nTrained model with optimizer:', optimizerKey, 'with mean' \
                'squared error:', error, 'and directional accuracy:', da, '\n')
    '''
