#SentenceTokenization.py - by Tarek Kanan, 9/15/2014, for VT CS4984, CL
from __future__ import division
import nltk
from nltk.corpus import PlaintextCorpusReader

# Aimed to get sentence versions of collections so POS routines can work on sentences.

# CE: means ClassEvent
# YS: means YourSmall - commented out so you can run this on your collection later
# YB: means YourBig - be sure to adapt this to run on the cluster
# Be sure to use the correct paths from your machine instead of what is below.

CEcorpus_root = '/Users/tarek/Desktop/Cl/ClassEvent'
#YScorpus_root = '/Users/tarek/Desktop/CL/EventCollections/China_Flood'
#YBcorpus_root = '/Users/tarek/Desktop/CL/EventCollections/YourBigCollection'

CEwordlists = PlaintextCorpusReader(CEcorpus_root, ".*\.txt")
#YSwordlists = PlaintextCorpusReader(YScorpus_root, ".*\.txt")
#YBwordlists = PlaintextCorpusReader(YBcorpus_root, ".*\.txt")

CE = CEwordlists.raw()
#YS = YSwordlists.raw()
#YB = YBwordlists.raw()


# tokenizing sentences for the ClassEvent, YourSmall, and YourBig collections
sent_tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')

CEsents = sent_tokenizer.tokenize(CE)
#YSsents = sent_tokenizer.tokenize(YS)
#YBsents = sent_tokenizer.tokenize(YB)

# To print CEsents, YSsents, and YBsents as lists
print 'ClassEvent Sentence tokens: ', (CEsents)
#print 'YourSmall Sentence tokens: ', (YSsents)
#print 'YourBig Sentence tokens: ', (YBsents)

#To print CEsents, YSsents and YBsents as strings
print 'ClassEvent Sentence tokens: '
print "\n".join(CEsents)
#print 'YourSmall Sentence tokens: '
#print '\n'.join(YSsents)
#print 'YourBig Sentence tokens: '
#print '\n'.join(YBsents)

#To print part of the CEsents, YSsents and YBsents lists
print 'ClassEvent Sentence tokens: ', (CEsents[1:10])
#print 'YourSmall Sentence tokens: ', (YSsents[1:10])
#print 'YourBig Sentence tokens: ', (YBsents[1:10])

