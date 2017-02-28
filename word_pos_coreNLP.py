# This code prepares dictionaries with word as the key and their named entity as the value.

import os, re
from collections import defaultdict

def word_ner():
    direc = './Sentence-Generation-Fan-Theories/Database/coreNLP output'

    files = os.listdir(direc)
    ner_tags = []

    for elem in files:
        path = os.path.join(direc, elem)
        f = open(path, 'r')
        text = f.read()
    #print text
        word_names_pair = re.findall('Text=(.*) CharacterOffsetBegin.* NamedEntityTag=(\w+)',text)
    #print word_tag_pair
        for pair in word_names_pair: ner_tags.append(pair)

    #print len(ner_tags)
    return ner_tags


def word_nouns(pos_tags):
    nouns = defaultdict(float)

    for elem in pos_tags:
        if elem[1] == 'PERSON': nouns[elem[0].lower()] += 1

    sorted_nouns = sorted(nouns, key = nouns.__getitem__, reverse=True)

    return nouns, sorted_nouns


'''
pos_tags = word_pos()
nouns, sorted_nouns = word_nouns(pos_tags)
for noun in sorted_nouns[0:20]:
    print noun
    print nouns[noun]
'''
