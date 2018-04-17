import os
import os.path

def strings_are_in (_targetString, _strings):
    print(_targetString)
    print(_strings)
    for s in _strings:
        if not s in _targetString:
            return False

    return True

if __name__ == '__main__':

    # get input string to search for
    strings = []
    keepGoing = True
    while keepGoing:
        newString = input('enter a string to earch for: ')        
        
        if newString == '':
            keepGoing = False
        else:
            strings.append(newString)

    best = (0, 'None')

    # for each search
    for search in os.listdir():
        if os.path.isdir(search) and strings_are_in(search, strings):
            #print('entering search', search)
            os.chdir(search)

            for epoch in os.listdir():
                if os.path.isdir(epoch):
                    #print('entering epoch', epoch)
                    os.chdir(epoch)
           
                    # extract da of each model
                    for model in os.listdir():
                        da = float(model[model.index('_', 10) + 1 : ])
                        print(da)
                        
                        # if da is higher than best, we have a new best model
                        if da > best[0]:
                            name = search + '/' + epoch + '/' + model
                            best = (da, name)

                    # back out of search and epoch directories
                    os.chdir('..')
            
            os.chdir('..')

    print(best)
