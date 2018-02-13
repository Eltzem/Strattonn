''' This file is here to handle creation of paths for files. It can help us manage operating
    system path differences.
'''

import platform

def create_data_dir_path ():
    if 'Windows' in platform.platform():
        return '..\data'
    else:
        return '../data'

def get_path_slash ():
    if 'Windows' in platform.platform():
        return '\\'
    else:
        return '/'
