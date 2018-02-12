''' This file is here to handle creation of paths for files. It can help us manage operating
    system path differences.
'''

import platform.platform as pf

def create_data_dir_path ():
    if 'Windows' in pf():
        return '..\data'
    else:
        return '../data'


