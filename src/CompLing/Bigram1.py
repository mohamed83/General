import nltk

from nltk.corpus import PlaintextCorpusReader
from nltk.util import ngrams
from nltk.corpus import stopwords
import operator

#print"Calling the Empty Line Function\n"
def filter_empty_lines(str, encoding="utf8"):
    lines = str.split("\n")
    result = ""
    for line in lines:
        if len(line.strip()) > 0:
            result = result + "\n" + line.encode(encoding)
    return result
#print "End Calling the Function\n"
    
class_event_corpus_root = '/home/mohamed/bigramData/sample'
print "Reading from the Corpus\n"
corpusReader = PlaintextCorpusReader(class_event_corpus_root, ".*\.txt", encoding="utf8")
print "Call TextUtils"
#string = filter_empty_lines(corpusReader.raw())
string = corpusReader.raw()
#words = [w.encode('utf8') for w in corpusReader.words() if len(w.strip()) > 3]
words = [w.encode('utf8') for w in corpusReader.words() if len(w.strip()) > 3]
print "Remove the Stopwords\n"
stop = stopwords.words('english')
#stop = [w.encode('utf8') for w in stop]
#stop = [w for w in stop]
words = [w for w in words if w.isalpha()]
words = [w for w in words if not w in stop]

#string = " ".join(words)
print "Generate the N-Grams\n" 
N = 2
#bigrams = ngrams(string.split(), N)
bigrams = ngrams(words, N)


    


D = dict()
for bigram in bigrams:
    if bigram in D:
        D[bigram] += 1
    else:
        D[bigram] = 1
'''
strparts = string.split()

print"Start Creating 2-grams\n"
for i in range(len(strparts)-N): # N-grams
    try:
        
'''      
print"Done Creating 2-grams\n"
       
sorted_D = sorted(D.iteritems(), key=operator.itemgetter(1), reverse=True)
#print "The top 3000 most frequent bi-grams in the corpus: "
#print sorted_D [:3000]
f = open("/home/mohamed/bigramData/Bigrams1.txt","w")

print"Start Writing into File\n"

for t in sorted_D[:10000]:
    f.write(str(t[0])+"\n")
f.close()

print "Done Writing into File\n"
