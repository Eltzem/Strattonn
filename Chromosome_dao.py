from Chromosome import Chromosome

import os
import os.path

import pickle

#TODO: add save functionality

class Chromosome_dao:

    def __init__ (self):
        self.chromosome = None

    def load (self, _filepath):

        if os.path.exists(_filepath):
            try:
                with open(_filepath, 'rb') as input:
                    self.chromosome = pickle.load(input)
            except Exception as e:
                print(str(e))

        else:
            raise Exception ('Chromosome save file not present:', _filepath)


    def save(self, _chromosome, _filepath):
        try:
            with open(_filepath, 'wb') as output:  # Overwrites any existing file.
                pickle.dump(_chromosome, output, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(str(e))

    def chromosome (self):
        if self.chromosome == None:
            raise Exception ('No model to return')
        return self.chromosome
