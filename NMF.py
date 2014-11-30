# -*- coding: utf-8 -*-
"""
Topic Mining of the Wikipedia literature using Non-Negative Matrix 
Factorization.
"""
from sklearn import decomposition
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np              
import Data
from compiler.ast import flatten
from gensim import corpora, models
import string
import nltk.corpus

papers, abstracts = Data.load_data() 
dictionary, corpus_tfidf, corpus= Data.prepare_data()  
#texts = flatten((texts))
words = []
for paper in papers:
    words.append(map(string.lower, nltk.word_tokenize(paper['Abstract'])))
#for paper in papers:
#    words = map(string.lower, nltk.word_tokenize(paper['Abstract']))
#    paper.update({'words': words})
all_words = [ word for paper in words for word in paper ]

 
## Count the occurences of all words
#wordcounts = dict([ [t, all_words.count(t)] for t in set(all_words) ])
#
#stopwords = nltk.corpus.stopwords.words('english')
# 
#terms = {}
#for word, count in wordcounts.iteritems():
#    if count > 2 and word not in stopwords and word.isalpha():
#        terms[word] = count
# 
# 
## Change the ordering of value and key for sorting
#items = [(v, k) for k, v in terms.items()]
# 
#for count, word in sorted(items, reverse=True)[:5]:
#    print("%5d %s" % (count, word))
# 
#
## Wikipedia is the main topic of all the papers to remove it
#terms.pop('wikipedia')
 

terms = list(dictionary.token2id)


# Construct a bag-of-words matrix
M = np.asmatrix(np.zeros([len(papers), len(terms)]))
for n, paper in enumerate(words):
   for m, term in enumerate(terms):
        M[n,m] = words[n].count(term)

def nmf(M, components=5, iterations=5000):
    """Applies NMF and returns the results"""
    # Initialize to matrices
    W = np.asmatrix(np.random.random(([M.shape[0], components])))
    H = np.asmatrix(np.random.random(([components, M.shape[1]])))
    for n in range(0, iterations): 
        H = np.multiply(H, (W.T * M) / (W.T * W * H + 0.001))
        W = np.multiply(W, (M * H.T) / (W * (H * H.T) + 0.001))
        print "%d/%d" % (n, iterations)    
    return (W, H)
    
## Perform the actual computation
W, H = nmf(M, iterations=50, components=50)

for component in range(W.shape[1]):
    print("="*80)
    print("TOPIC %d: " % (component,))
    indices = (-H[component,:]).getA1().argsort()
    print([dictionary[i] for i in indices[:6] ])
    print("-")
    indices = (-W[:,component]).getA1().argsort()
    print("\n".join([ papers[i][''] for i in indices[:5] ]))    
