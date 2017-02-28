#This code presents the first order hidden markov model used in method 4, as presented in the report.

import os, re, numpy, sys, random
from collections import defaultdict

#The initiate function finds the counts of part of speech tags, word counts, PoS pair counts as well as counts of word to PoS tag pairs, to be used for prediction by the HMM

def initiate():
    direc = './Sentence-Generation-Fan-Theories/Database/coreNLP output'

    files = os.listdir(direc)
    content = {}

    for elem in files:
            path = os.path.join(direc, elem)
            f = open(path, 'r')
            content[elem] = f.readlines()

    print '\nnumber of documents loaded: ', len(content)
#print content['001.out']

    newfile = open('word_pos.txt','w')
    k = 1
    for passage in content.values():
    #print k  
        for sentence in passage:
        #print sentence
            pos_tuple = re.findall('Text=(.*) CharacterOffsetBegin.* PartOfSpeech=(.*) L.*',sentence)
        #print pos_tuple
            if pos_tuple != []:
                newfile.write(pos_tuple[0][0].lower())
                newfile.write('\t')
                newfile.write(pos_tuple[0][1])
                newfile.write('\n')
    #newfile.write('\n')
        k += 1

    newfile.close()

    newfile = open('word_pos.txt','r')

    word_to_pos = defaultdict(float) 				
    word_to_word = defaultdict(lambda: defaultdict(float))
    pos_to_word = defaultdict(lambda: defaultdict(float))
    pos_to_pos = defaultdict(lambda: defaultdict(float))
    start_to_pos = defaultdict(float)
    pos_count = defaultdict(float)
    word_count = defaultdict(float)

    lines = newfile.readlines()
    lines = ['%s %s' % ('START', line) for line in lines]
#print lines[0]
    split_lines = [line.split() for line in lines]
    #print split_lines
    #for line in range(len(split_lines)):
    #    for elem in range(line): 
    #        split_lines[line][elem] = split_lines[line][elem].lower()
    
    start_count = 0

    for start, word, tag in split_lines:
    #print word, tag
        pos_to_word[tag][word] += 1
        pos_count[tag] += 1 
        word_count[word] += 1
        start_count += 1
        if word not in word_to_pos.keys(): word_to_pos[word] = tag

    #print word_to_pos
    for k in range(len(split_lines)-1):
    #print split_lines[k][2], split_lines[k+1][2]    
        pos_to_pos[split_lines[k][2]][split_lines[k+1][2]] += 1
        word_to_word[split_lines[k][1]][split_lines[k+1][1]] += 1

    for start, word, tag in split_lines:
        start_to_pos[tag] += 1

    return word_to_word, word_to_pos, pos_to_word, pos_to_pos, start_to_pos, pos_count, word_count

def weighted_draw(words_dict):
    choice_items = words_dict.items()
    total = sum(w for c, w in choice_items)
    #print total
    r = random.uniform(0, total)
    upto = 0
    for c, w in choice_items:
       if upto + w > r:
          return c
       upto += w
    assert False, "Shouldn't get here"

def get_next_tag(pos_to_pos, pos_count, pos):
    next_pos = defaultdict(float)
    for tag in pos_count.keys():
        next_pos[tag] = float(pos_to_pos[pos][tag]) / pos_count[pos]
    #print next_pos
    tag = weighted_draw(next_pos)
    return tag

def get_word(pos_to_word, pos_count, pos):
    next_word_pos = defaultdict(float)
    #next_word_word = defaultdict(float)
    #print pos
    word_probs = pos_to_word[pos]
    for word in word_probs.keys():
        next_word_pos[word] = float(word_probs[word]) / pos_count[pos]
    
    #print next_word_pos
    word = weighted_draw(next_word_pos)
    return word

def get_next_word(word, pos, word_to_word, pos_to_word, pos_count, word_count):
    next_word_pos = defaultdict(float)
    next_word_word = defaultdict(float)
    word_pros = pos_to_word[pos]
    word_word = word_to_word[word]
    values = []
    for key in word_pros.keys():
        next_word_pos[key] = float(word_pros[key]) / pos_count[pos]
        next_word_word[key] = float(word_word[key]) / word_count[word]
    sorted_pos = sorted(next_word_pos, key=next_word_pos.__getitem__, reverse=True)
    sorted_word = sorted(next_word_word, key=next_word_word.__getitem__, reverse=True)
    for value in sorted_pos:
        if value in sorted_word:
            values.append(value)
    return values[0]

def get_first_tag(start_to_pos, start_count):
    tag_prob = {}
    for tag in start_to_pos.keys():
        tag_prob[tag] = float(start_to_pos[tag]) / start_count
    first_tag = weighted_draw(tag_prob)
    return first_tag


def generate_sentence(pos_to_word, pos_to_pos, pos_count, start_to_pos, word_count, start, word_to_pos, word_to_word):
    sample_sentence = [start]

    if start == 'START':
        pos = get_first_tag(start_to_pos, word_count)
    else:
        pos = word_to_pos[start]  
        #print pos
    while pos != '.':
            word = get_word(pos_to_word, pos_count, pos)
            #print word
            sample_sentence.append(word)
            pos = get_next_tag(pos_to_pos, pos_count, pos)

    return sample_sentence

def print_sentences(start, word_to_word, word_to_pos, pos_to_word, pos_to_pos, start_to_pos, pos_count, word_count):
    #print start
    #print word_to_pos
    all_sentences = []
    for k in range(10):
        sentence = generate_sentence(pos_to_word, pos_to_pos, pos_count, start_to_pos, word_count, start, word_to_pos, word_to_word)
        
        #print word_to_pos[start]
        all_sentences.append(sentence)

    return all_sentences
