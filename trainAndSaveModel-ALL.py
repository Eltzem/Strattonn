from CreateAggregateInputOutputFiles import load_all_training_and_testing_data
from DNN import DNN
from Chromosome import Chromosome
from Paths import get_path_slash

'''
    trainAndSaveModel.py modified to use the alldata.py input and output generating
    functions. It uses stock data from multiple symbols combined into one input
    series. Hopefully it will tell us if there are hidden relationships between
    some stock symbols.
'''

def create_model (_chromosome):
    dnn = DNN(_chromosome=_chromosome)
    print(dnn.get_model().summary())
    return dnn

def create_train_test_save_model (_chromosome):
    dnn = create_model(_chromosome)

    trainInputs, trainOutputs, testInputs, testOutputs = \
        load_all_training_and_testing_data(0.2, 'PM', 'data/1min/3910')

    dnn.compile(_chromosome.optimizer(), 'mean_squared_error')

    dnn.train(trainInputs, trainOutputs, 8, 10)

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
    print(create_train_test_save_model(Chromosome(_genome=[115, 5, 'adam', 0.01, 400, 'tanh', 0, 500, 'tanh', 0, 500, 'tanh', 0, 300, 'tanh', 0, 200, 'tanh', 0, 1, 'linear'], _maxHL=5)))
