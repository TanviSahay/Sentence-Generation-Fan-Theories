# Sentence-Generation-Fan-Theories
In the last 20 years, American entertainment, ranging from movies to television shows to comic books to
novels, has seen a colossal increase in its fan following, and with this increase, more and more people have
begun to keep a story going even when it is on hiatus, giving rise to fan-proposed theories of what the
future of a story might be. In this projcet, these fan theories have been used as the data set over which several models have been trained and their generative performance has been compared. 

Three generative models, N-grams, Hidden Markov Models(HMM) and Long-
Short Term Memory(LSTM) recurrent neural networks have been explored and their results compared to
analyze how they perform for the proposed task. The Stanford OpenIE package has been used to extract
relational tuples while the CoreNLP package has been used to tokenize the input text, perform part-of-
speech tagging and find the named entities in the text. This information has been utilized in combination
1 with the N-gram models to propose three different methods of sentence generation and assess how they
perform as compared to other baseline models. Frequency of occurrence of each character name from the
chosen show has been computed and sentence for the five most famous characters have been generated,
with each sentence generation task being seeded with the name of the character. Comparison has been
done on the basis of how understandable a sentence is and how much information it conveys. Human
subjects with both presence as well as absence of domain knowledge were asked to rate the sentences,
in order to obtain an understanding of how well each model maps domain knowledge in its generative methodology.
