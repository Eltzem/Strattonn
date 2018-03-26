from Chromosome import Chromosome
from DNN import DNN

from keras.models import load_model, save_model

genome = [1, 5, 'adam', 0.01, 0, 'hard_sigmoid', 0.5, 97, 'tanh', 0.6, 82, 'linear', 0.3, 0, 'hard_sigmoid', 0.9, 0, 'relu', 0.1, 32, 'softmax', 0.4, 84, 'linear', 0.9, 1, 'sigmoid']

chr1 = Chromosome(_genome=genome)

dnn1 = DNN(_chromosome=chr1)

try:
    print(dnn1.get_model().summary())
    print(str(dnn1.get_chromosome()))

    dnn1.compile('adam', 'mean_squared_error', ['accuracy'])
    dnn1.save('/home/will/Documents/Intelligent Systems/Strattonn/dnn/dnn1')
    
    dnn2 = DNN()
    dnn2.load('/home/will/Documents/Intelligent Systems/Strattonn/dnn/dnn1')
    print(dnn2.get_model().summary())
    print(str(dnn2.get_chromosome()))


    dnn1.close()
    dnn2.close()
except Exception as e:
    print(str(e))
    raise e
