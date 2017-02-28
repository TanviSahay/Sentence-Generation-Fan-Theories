# This is the master code that generates sentences for the top 10 most famous named entities and stores them in text files. One text file each is generated for the first four methods as described in the report. The first 10 characters contain names which are not character titles and are hence ignored(For example: snow and stark occur in top 10 but are not considered for top 5).

import bigram_sentence as bigram
import word_pos_coreNLP as popularity
import HMM_generate as HMMG

pos_tags = popularity.word_ner()
nouns, sorted_nouns = popularity.word_nouns(pos_tags)

most_popular = sorted_nouns[0:10]
no_chars = ['\xe2\x80\x94','\xe2\x80\x9d','\xe2\x80\x9c','\xe2\x80\xa6','\xe2\x80\x93','\xe2\x80\x99','\xe2\x80\x98',',\xe2\x80\x9d','\xe2\x80\x9a']
f1 = open('sampletext_case1.txt','w')
f2 = open('sampletext_case2.txt','w')
f3 = open('sampletext_case3.txt','w')
f4 = open('sampletext_case4.txt','w')

word_to_word, word_to_pos, pos_to_word, pos_to_pos, start_to_pos, pos_count, word_count = HMMG.initiate()

for name in most_popular:
    print name
    sentences1 = bigram.print_sentences(name,bigram.sentence1())
    sentences2 = bigram.print_sentences(name,bigram.sentence2())
    sentences3 = bigram.print_sentences(name,bigram.sentence3())
    sentences4 = HMMG.print_sentences(name, word_to_word, word_to_pos, pos_to_word, pos_to_pos, start_to_pos, pos_count, word_count)

    f1.write('sentences for the character: %s' % (name))
    f1.write('\n')
    for sentence in sentences1:
        for word in sentence:
            if word not in no_chars:
                f1.write(word)
                f1.write(' ')
        f1.write('\n')
    f1.write('\n')
    
    f2.write('sentences for the character: %s' % (name))
    f2.write('\n')
    for sentence in sentences2:
        for word in sentence:
            if word not in no_chars:
                f2.write(word)
                f2.write(' ')
        f2.write('\n')
    f2.write('\n')
    
    f3.write('sentences for the character: %s' % (name))
    f3.write('\n')
    for sentence in sentences3:
        for word in sentence:
            if word not in no_chars:
                f3.write(word)
                f3.write(' ')
        f3.write('\n')
    f3.write('\n')

    f4.write('sentences for the character: %s' % (name))
    f4.write('\n')
    for sentence in sentences4:
        for word in sentence:
            if word not in no_chars:
                f4.write(word)
                f4.write(' ')
        f4.write('\n')
    f4.write('\n')

f1.close()
f2.close()
f3.close()
f4.close()
