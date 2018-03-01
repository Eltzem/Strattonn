from keras.models import load_model

from Chromosome import Chromosome

import os
import os.path

#TODO: add save functionality

'''
    Data access object to saving and loading DNN classes. Loads keras models and Chromosome (s).
'''
class DNN_dao:

    def __init__ (self):
        self.CHROMOSOME_FILENAME = 'chromosome'
        self.MODEL_FILENAME = 'model.h5'

        self.model = None
        self.chromosome = None

    def load (self, _directoryPath):
        # save current working directory
        oldPath = os.getcwd()

        # go into save folder
        if os.path.exists(_directoryPath):
            os.chdir(_directoryPath)
        else:
            raise Exception ('DNN save directory path does not exist:', _directoryPath)

        # load chromosome if it exists
        if os.path.exists(self.CHROMOSOME_FILENAME):
            self.chromosome = Chromosome(_filepath=_self.CHROMOSOME_FILENAME)

        # load model if it exists
        if os.path.exists(self.MODEL_FILENAME):
            self.model = load_model(self.MODEL_FILENAME)
        else:
            raise Exception ('DNN model save file not present:', self.MODEL_FILENAME)

        # restore current working directory
        os.chdir(oldPath)
   
    def save (self, _directoryPath, _dnn, _chromosome=None):
        # save current working directory
        oldPath = os.getcwd()

        # check if path exists. if not, create it and go in
        if not os.path.exists(_directoryPath):
            os.mkdir(_directoryPath)
        os.chdir(_directoryPath)

        # save Chromosome if it exists
        if _chromosome != None:
            try:
                

        # restore current working directory
        os.chdir(oldPath)

    # gets the loaded model
    def model (self):
        if self.model == None:
            raise Exception ('No model to return')
        return self.model

    # gets the loaded chromosome
    def chromosome (self):
        if self.chromosome == None:
            raise Exception ('No chromosome to return')
        return self.chromosome
