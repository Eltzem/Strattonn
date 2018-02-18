''' This file is here to handle creation of paths for files. It can help us manage operating
    system path differences.
'''

import platform

'''
    Returns relative path to the data directory from the program's file location.

    Returns:string = relative path to data directory
'''
#tested
def get_data_dir_path ():
    if 'Windows' in platform.platform():
        return 'data'
    else:
        return 'data'

'''
    Returns the proper directory seperator in a file path for the operating system being used.

    Returns:string = operating system path slash
'''
#tested
def get_path_slash ():
    if 'Windows' in platform.platform():
        return '\\'
    else:
        return '/'
