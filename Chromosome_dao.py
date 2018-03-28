import sys

if not 'Chromosome' in sys.modules:
    from Chromosome import Chromosome

import os
import os.path

import pickle


class Chromosome_dao:

    def __init__ (self):
        self.chromosome = None

    '''
        Loads a Chromosome object from a file. Sets self.chromosome as the loaded Chromosome.

        Args:   string _filepath = path to file to load from
    '''

    def load (self, _filepath):

        print('loading chromosome from:', _filepath)

        if os.path.exists(_filepath):
            try:
                with open(_filepath, 'rb') as input:
                    self.chromosome = pickle.load(input)
            except Exception as e:
                raise e
        else:
            raise Exception ('Chromosome save file not present:', _filepath)


    '''
        Saves a Chromosome object to a file.

        Args:   Chromosome _chromosome = Chromosome object to save.
                string _filepath = path to save file to

    '''

    def save (self, _chromosome, _filepath):

        print('saving chromosome to:', _filepath)

        try:
            with open(_filepath, 'wb') as output:  # Overwrites any existing file.
                pickle.dump(_chromosome, output, pickle.HIGHEST_PROTOCOL)
        except Exception as e:
            print(str(e))
            raise e

    '''
        Gets the loaded Chromosome object.

        Returns:Chromosome = self.chromosome
    '''

    def get_chromosome (self):
        if self.chromosome == None:
            raise Exception ('No Chromosome genome to return')
        return self.chromosome
