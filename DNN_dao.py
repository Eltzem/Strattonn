from keras.models import load_model, save_model

from Chromosome import Chromosome

import pickle

import os
import os.path

#TODO: add save functionality

'''
    Data access object to saving and loading DNN classes. Loads keras models and Chromosome (s).
'''
class DNN_dao:

    def __init__ (self):
        self.CHROMOSOME_FILENAME = 'chromosome'
        self.MODEL_FILENAME = 'model.hdf5'
        self.LAYERS_FILENAME = 'layers'

        self.model = None
        self.chromosome = None
        self.layers = None

    def load (self, _directoryPath):
        print('loading model from', _directoryPath)

        # save current working directory
        oldPath = os.getcwd()

        # go into save folder
        if os.path.exists(_directoryPath):
            os.chdir(_directoryPath)
        else:
            raise Exception ('DNN save directory path does not exist:', _directoryPath)

        print('\n', os.path.exists(self.CHROMOSOME_FILENAME), '\n')
        # load chromosome if it exists
        if os.path.exists(self.CHROMOSOME_FILENAME):
            print('\nloading chromosome\n')
            self.chromosome = Chromosome.load(self.CHROMOSOME_FILENAME)

        # load model if it exists
        if os.path.exists(self.MODEL_FILENAME):
            print('\nloading model\n')
            self.model = load_model(self.MODEL_FILENAME)
        else:
            raise Exception ('DNN model save file not present:', self.MODEL_FILENAME)

        # restore current working directory
        os.chdir(oldPath)
   
    def save (self, _directoryPath, _dnn):
        print('saving DNN to', _directoryPath, '/', self.MODEL_FILENAME)

        # save current working directory
        oldPath = os.getcwd()

        # check if path exists. if not, create it and go in
        if not os.path.exists(_directoryPath):
            os.mkdir(_directoryPath)
        os.chdir(_directoryPath)

        # save Chromosome if it exists
        if _dnn.get_chromosome() != None:
            print('\nsaving chromosome\n')

            try:
                _dnn.get_chromosome().save(self.CHROMOSOME_FILENAME)
            except Exception as e:
                raise e

        # save DNN model
        try:
            _dnn.get_model().save(self.MODEL_FILENAME)
        except Exception as e:
            raise e

        # restore current working directory
        os.chdir(oldPath)

    # gets the loaded model
    def get_model (self):
        if self.model == None:
            raise Exception ('No model to return')
        return self.model

    # gets the loaded chromosome
    def get_chromosome (self):
        if self.chromosome == None:
            raise Exception ('No chromosome to return')
        return self.chromosome

