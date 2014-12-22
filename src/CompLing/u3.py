'''
Created on Sep 20, 2014

@author: dlrl
'''
import nltk
from nltk import word_tokenize
#from nltk import sent_tokenize
#text = word_tokenize("And now for something completely different")
from nltk.corpus import PlaintextCorpusReader

def findtags(tag_prefix, tagged_text):
    cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text
                                   if tag.startswith(tag_prefix))
    #return dict((tag, cfd[tag].keys()[:5]) for tag in cfd.conditions())
    return dict((tag, cfd[tag].keys()[:5]) for tag in cfd.conditions())


corpusCE = PlaintextCorpusReader("Islip13Rain", ".*\.txt")

ceRow = corpusCE.raw()

sentsCE = nltk.sent_tokenize(ceRow)
#CEwords = []
BrownAndTbankTags = nltk.corpus.brown.tagged_sents() + nltk.corpus.treebank.tagged_sents()
t0 = nltk.DefaultTagger('NN')
t1 = nltk.UnigramTagger(BrownAndTbankTags, backoff=t0)
t2 = nltk.BigramTagger(BrownAndTbankTags, backoff=t1)
t3 = nltk.TrigramTagger(BrownAndTbankTags,backoff=t2)

sentsTokensCE = [nltk.word_tokenize(sent) for sent in sentsCE]

CEposTags = t3.batch_tag(sentsTokensCE)
'''
for sent in CEsents:
    words = nltk.word_tokenize(sent)
    #CEwords.append(words)
    #posTags = nltk.pos_tag(words)
    posTags = t3.tag(words)
    CEposTags.append(posTags)
'''

tagged_words = [(w,t) for sent in CEposTags for (w,t) in sent]


#tagdict = findtags('NN', nltk.corpus.brown.tagged_words(categories='news'))
tagdict = findtags('NN', tagged_words)
for tag in sorted(tagdict):
    print tag, tagdict[tag]



#for pos in CEposTags:
#    print pos