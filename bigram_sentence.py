## This code will generate sentences using the bigram language model, for three cases. The three methods of text generation using bigram models have been defined in the report.

import os, re, random
from collections import defaultdict

'''THE FIRST CASE'''

#Get all sentences from the data set, tokenize them using function tokenize() and store them in a list -- sentence_1, generated using the function sentence1().

def tokenize(line):
    line_split = line.split()
    tokens = []
    final_tokens = []
    for token in line_split:
        string = re.findall('(\W*)(\w+)?(\W*\w*)', token)
        if string[0][0] != '': tokens.append(string[0][0]) 
        if string[0][1] != '': tokens.append(string[0][1])
        if string[0][2] != '': tokens.append(string[0][2])
    #print tokens
    '''Certain tokens that could not be read using the default encoding were manually mapped to their written english counterpart'''
    for token in range(len(tokens)):
        #print token
        tokens[token] = re.sub('\(', '-LRB-', tokens[token])
        tokens[token] = re.sub('\)', '-RRB-', tokens[token])
        tokens[token] = re.sub("\\xe2\\x80\\x99s","'s",tokens[token])
        tokens[token] = re.sub("\xe2\x80\x99ll", "'ll", tokens[token])
        tokens[token] = re.sub("\xe2\x80\x99t", "'t", tokens[token])
        tokens[token] = re.sub("\xe2\x80\x99m", "'m", tokens[token])
        tokens[token] = re.sub("\xe2\x80\x99ve","'ve",tokens[token])
        tokens[token] = re.sub("\xe2\x80\x99d","'d",tokens[token])
        tokens[token] = tokens[token].lower()
        #print tokens[token]
    #tokens.append('.')
    
    return tokens

#load data for case 1
def sentence1():
    directory = '../../Database/dataset'

    list_files = os.listdir(directory)

    sentences_1 = []
    for elem in list_files:
        filepath = os.path.join(directory, elem)
        f = open(filepath, 'r')
        f_text = f.read()
        f_text = f_text.split('.')
        for line in f_text:
            if line != []:
                f_text = tokenize(line)
                sentences_1.append(f_text)
            
    return sentences_1


'''THE SECOND CASE'''

#Get all sentences from the data set cleaned using OpenIE, tokenize them and store them in a list sentences_2, generated using the function sentences2().

def sentence2():
    directory = '../../../stanford-corenlp-full-2016-10-31 (2)'
    filename = 'output.txt'

    filepath = os.path.join(directory, filename)

    f = open(filepath, 'r')
    f_lines = f.readlines()

#print f_lines
    f_lines = [i.split() for i in f_lines]

    sentences_2 = []

    for line in f_lines:
        for elem in range(len(line)):line[elem] = line[elem].lower() 
        line.append('.')
        sentences_2.append(line[1:])
    
    #sentences_2 : a list of tokenized sentences with each element a list itself, for a single sentence from the dataset.
    return sentences_2


'''THE THIRD CASE'''

#Out of the sentences generated in case 2, only extract sentences with a named entity = PERSON at the beginning of the sentence. Store these in a list sentences_3 generated using the function sentence3().

def sentence3():
    directory = '../'
    filename = 'openie_nouns'

    filepath = os.path.join(directory, filename)
    f = open(filepath, 'r')
    f_lines = f.readlines()
   
    f_lines = [i.split() for i in f_lines]
    
    sentences_3 = []
    for line in f_lines:
        for elem in range(len(line)):line[elem] = line[elem].lower() 
        #print line
        line.append('.')
        sentences_3.append(line)
    
    return sentences_3


#Get unigram and bigram counts

def unigram_count(sentences):
    unigram_counts = defaultdict(int)
    for line in sentences:
        #print line
        for word in line: unigram_counts[word] += 1
    return unigram_counts

def bigram_count(sentences):
    bigram_counts = defaultdict(lambda: defaultdict(int))
    for line in sentences:
        #tokenize_elem = better_tokenize(content[elem])
        #print tokenize_elem
        for word in range(len(line)-1): 
            #print line[word], line[word+1]
            #print tokenize_elem[word], tokenize_elem[word+1]
            #print '\n'
            bigram_counts[line[word]][line[word+1]] += 1
    #print bigram_counts
    return bigram_counts


#The weighted draw function will choose a random word from a list of possible words given its probability is greater than a threshold.

def weighted_draw(words_dict):
    choice_items = words_dict.items()
    #print choice_items
    total = sum(w for c, w in choice_items)
    r = random.uniform(0, total)
    upto = 0
    for c, w in choice_items:
       if upto + w > r:
          return c
       upto += w
    assert False, "Shouldn't get here"


#A new word is drawn from the bigram model

def draw_from_bigram_model(unigram_counts, bigram_counts, word):
    possible_words = {}
    count_word = unigram_counts[word]
    bigram_count_word = bigram_counts[word]
    #print bigram_count_word
    for i in bigram_count_word.keys():
        #print i
        possible_words[i] = float(bigram_count_word[i]) / count_word
    #print possible_words
    next_word = weighted_draw(possible_words)
    return next_word


#This function outputs a sample sentence taking into account the seed word, unigram and bigram counts

def sample_sentence(unigram_counts, bigram_counts, start):
    sentence = [start]
    #print sentence
    word = draw_from_bigram_model(unigram_counts, bigram_counts, start)
    #print word
    while word != '.': 
        sentence.append(word)
        word = draw_from_bigram_model(unigram_counts, bigram_counts, word)
    sentence.append(word)
    return sentence


#For the seed word given by start, 10 sample sentences are generated and appended into the list all_sentences

def print_sentences(start, sentences):
    print 'For the character %s' % (start)
    print 'example sentences generated from case 1 are: '
   # sentences = {}
    all_sentences = []
    for i in range(10):
        unigrams = unigram_count(sentences)
        #print unigrams['villainous']
        bigrams = bigram_count(sentences)
        #print bigrams['jon']
        sentence = sample_sentence(unigrams, bigrams, start)
        print sentence
        all_sentences.append(sentence)
    return all_sentences


