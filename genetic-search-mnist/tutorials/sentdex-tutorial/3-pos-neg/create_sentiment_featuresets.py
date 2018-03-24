import nltk # natural language processing toolkit
from nltk.tokenize import word_tokenize # converts sentence to array of words in sentence
from nltk.stem import WordNetLemmatizer # removes versions of same word

import numpy as np
import random
import pickle
from collections import Counter

lemmatizer = WordNetLemmatizer()
n_lines = 100000 # test data is about 5000 lines

# create lexicon from all words in datasets
def create_lexicon (pos, neg):
    lexicon = []

    # Get all words in files
    # loop through both files
    for fi in [pos, neg]:
        # open file
        with open(fi, 'r') as fi_current:
            # read lines into a list
            contents = fi_current.readlines()
            # loop through lines
            for line in contents[:n_lines]:
                # creates list of words in line
                all_words = word_tokenize(line.lower())
                
                #print(all_words)
                #input()

                # adds list elements to master lexicon of all words
                lexicon += list(all_words)
    #print(lexicon)
    
    # lemmatize (take out weird parts, simplify) of each word
        # add word to new lexicon
    lexicon = [lemmatizer.lemmatize(word) for word in lexicon]

    # get count of each word now that they are all simplified
    word_counts = Counter(lexicon)
    #word_counts = {'the':5345, 'house':301} <= example of word_counts

    # throw away common words and uncommon words
    lexicon_limited = []
    for word in word_counts:
        if 1000 > word_counts[word] > 50:
            lexicon_limited += [word]
    
    print('Lexicon length:', len(lexicon_limited))

    return lexicon_limited


def sample_handling (sample, lexicon, classification):
    featureset = []

    '''
    examples of featureset at end. Containts hot arrays for word counts + array to hold sentiment.
    [
    [[1 3 0 0 2], [1 0]], # positive
    [[0 1 2 2 0], [0 1]] # negative
    ]
    '''

    # opens sample file
    with open(sample, 'r') as fi:
        # reads file lines
        contents = fi.readlines()

        # loops through lines up to limit
        for line in contents[:n_lines]:
            # extract all words into list
            current_words = word_tokenize(line.lower())
            # lemmatize (simplify) words into new list
            current_words = [lemmatizer.lemmatize(word) for word in current_words]

            # init 0'ed array to hold word counts of sample
            features = np.zeros(len(lexicon))

            # loop through words in current_words
            for word in current_words:
                # increment each word features index by 1 if it exists in current_words
                if word.lower() in lexicon:
                    index = lexicon.index(word.lower())
                    features[index] += 1

            # add this line's hot array and pos/neg classification to featureset
            features = list(features)
            featureset.append([features, classification])

    #print('len featureset:', len(featureset))
    #print(featureset[3])
    return featureset

def create_feature_sets_and_labels (pos, neg, train_size = 0.9):
    # create word lexicon for all data
    lexicon = create_lexicon(pos, neg)

    # get word counts for each sentence in data, and classify that sentence as pos/neg
    features_pos = sample_handling('pos.txt', lexicon, [1, 0])
    features_neg = sample_handling('neg.txt', lexicon, [0, 1])

    #print('len pos:', len(features_pos))
    #print('len neg:', len(features_neg))

    # adds each sentence data to features[]
    features = []
    for feature in features_pos:
        features.append(feature)
    for feature in features_neg:
        features.append(feature)

    # randomize sentences
    random.shuffle(features)

    '''
    Why Shuffle?
    Final question, does prediction == actual output?
    does tf.argmax([output]) == tf.argmax([expectations])
    tf.argmax([32423, 1234]) == tf.argmax([1, 0]) == true, argmax returns index of largest value
    
    Must shuffle data so you don't train network to output [99999999, -999999999]
    '''

    # need it to be an np array
    features = np.array(features)

    training_size = int(train_size * len(features))
    # creates training inputs (lexicons) and outputs (classifications) up to testing_size limit
    train_x = []
    train_y = []
    for sentence_classification in range(training_size):
        # 0'th element in each sentence classification array is the lexicon, 1 is classification
        train_x.append(features[sentence_classification][0])
        train_y.append(features[sentence_classification][1])
    
    # creates testing inputs (lexicons) and outputs (classifications) after testing_size limit
    test_x = []
    test_y = []
    for sentence_classification in range(training_size, len(features)):
        # 0'th element in each sentence classification array is the lexicon, 1 is classification
        test_x.append(features[sentence_classification][0])
        test_y.append(features[sentence_classification][1])

    #return training and testing datasets
    return train_x, train_y, test_x, test_y
    

if __name__ == '__main__':
    train_x, train_y, test_x, test_y = create_feature_sets_and_labels('pos.txt', 'neg.txt')

    # pickle (serialize) datasets and save them
    with open('sentiment.set.pickle', 'wb') as fi:
        pickle.dump([train_x, train_y, test_x, test_y], fi)
