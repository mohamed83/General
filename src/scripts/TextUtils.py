#Unit3 Solutions prepared by XuanZhang and Tarek Kanan
#CS4984 Class (Computational Linguistics) Oct. 2014

import string
import nltk

#The next three functions used to clean up the corpus and can be used in the coming units.


def is_ascii(s):
    return all(ord(c) < 128 for c in s)


# Remove the non English words
def filter_non_alpha_words(words):
    result =[]
    for w in words:
        flag = True
        for ch in w:
            if not ch.isalpha():
                flag = False
                break
        if flag:
            result = result + [w]
    
    return result

# Remove the non English characters, punctuation, and numbers
def filter_non_alpha_chars(str):
    result = ""
    pcSet = set(string.punctuation)
    dgSet = set(string.digits)
    for ch in str:
        if ch.isalpha() or ch in pcSet or ch in dgSet or ch == " ":
            result = result + ch
    return result

# Remove the empty lines
def filter_empty_lines(str, encoding="utf8"):
    lines = str.split("\n")
    result = ""
    for line in lines:
        if len(line.strip()) > 0:
            result = result + "\n" + line.encode(encoding)
    return result


# Return the words with specified tags out of the specified text, used with question 11.5.5 
def findtags(tag_prefix, tagged_text):
    cfd = nltk.ConditionalFreqDist((tag, word) for (word, tag) in tagged_text
                                   if tag.startswith(tag_prefix))
    return dict((tag, cfd[tag].keys()) for tag in cfd.conditions())