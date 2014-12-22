#BrownAndTreebankTagsList.py - by Tarek Kanan, 9/15/2014, for VT CS4984, CL
from __future__ import division
import nltk
from nltk.corpus import brown
from nltk.corpus import treebank

# Building a large tagging corpus(BrownAndTreebankTag) by combining
#  the Brown and Treebank POS tagging corpora.
BrownAndTbankTag = nltk.corpus.brown.tagged_words() + nltk.corpus.treebank.tagged_words()

#To print the number of POS tags in the new big tags corpus

print 'the number of tags in the corpus: ', len(BrownAndTbankTag)

#To print the new corpus tags list
print '\n the corpus tags list', BrownAndTbankTag
