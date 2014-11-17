from gensim import corpora, models
from itertools import chain, izip_longest
from urllib import urlopen
from operator import itemgetter
import csv
import simplejson as json
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import ticker
from collections import Counter

#The code for extracting entities from referata was taken by fnielsen git repository
# Define a url as a Python string (note we are only getting 100 documents)
url = "http://wikilit.referata.com/" + \
    "wiki/Special:Ask/" + \
    "-5B-5BCategory:Publications-5D-5D/" + \
    "-3FHas-20author%3DAuthor(s)/-3FYear/" + \
    "-3FPublished-20in/-3FAbstract/-3FHas-20topic%3DTopic(s)/" + \
    "-3FHas-20domain%3DDomain(s)/" +  \
    "format%3D-20csv/limit%3D-20100/offset%3D0"


# Get and read the web page
doc = urlopen(url).read()  # Object from urlopen has read function

# Show the first 1000 characters
#print(doc[:1000])


web = urlopen(url)
# 'web' is now a file-like handle
lines = csv.reader(web, delimiter=',', quotechar='"')
# JSON format instead that Semantic MediaWiki also exports
url_json = "http://wikilit.referata.com/" + \
    "wiki/Special:Ask/" + \
    "-5B-5BCategory:Publications-5D-5D/" + \
    "-3FHas-20author/-3FYear/" + \
    "-3FPublished-20in/-3FAbstract/-3FHas-20topic)/" + \
    "-3FHas-20domain/" +  \
    "format%3D-20json"
# Read JSON into a Python structure
response = json.load(urlopen(url_json))

# response['printrequests'] is a list, map iterates over the list
columns = map(lambda item: item['label'], response['printrequests'])
# gives ['', 'Has author', 'Year', 'Published in', 'Abstract', 
#        'Has topic)', 'Has domain']
# Reread CSV
lines = csv.reader(urlopen(url), delimiter=',', quotechar='"')
# Iterate over 'lines' and insert the into a list of dictionaries
header = []
papers = []
for row in lines:      # csv module lacks unicode support!
    line = [unicode(cell, 'utf-8') for cell in row]
    if not header:     # Read the first line as header
        header = line
        continue   
    papers.append(dict(zip(header, line)))

# 'papers' is now an list of dictionaries

abstracts=[]
for abstract,i in enumerate(papers):
    abstracts.append(papers[abstract]['Abstract'])
    
import nltk.corpus
stopwords = nltk.corpus.stopwords.words('english')
#stoplist = set('for a of the and to in wikipedia'.split())
texts = [[word for word in abstract.lower().split() if word not in stopwords and word.isalpha() and word != 'wikipedia']
         for abstract in abstracts]
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
     for text in texts] 
        
#print texts
dictionary = corpora.Dictionary(texts)
dictionary.save('C:/Users/Ioanna/abstracts.dict')  

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('C:/Users/Ioanna/abstracts.mm', corpus) # store to disk, for later use

dictionary = corpora.Dictionary.load('C:/Users/Ioanna/abstracts.dict')
corpus = corpora.MmCorpus('C:/Users/Ioanna/abstracts.mm')
tfidf = models.TfidfModel(corpus) # step 1 -- initialize a model

corpus_tfidf = tfidf[corpus]
#lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=50)
#corpus_lsi = lsi[corpus_tfidf]
#lsi.print_topics(20)
lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=6)
topics = []

z = {}
ha = []
for i in range(0, 6):
    temp = lda.show_topic(i, 6)
    terms = []
    for term in temp:
        terms.append(term[1])
    topics.append(" ".join(terms))
    print "Top 6 terms for topic #" + str(i) + ": "+ ", ".join(terms)
    print "-"*80
    la = []
    for k in range(100) :
        if max(lda[corpus[k]],key=itemgetter(1))[0] == i :
            #print 'Article:' + str(papers[k][''])
            print 'Year:' + papers[k]['Year']
            la.append(int(papers[k]['Year']))
            z = Counter(la)
    ha.append(la) 
        
            #la = dict(izip_longest(*[iter(topics)] * 2, fillvalue=papers[k]['Year']))
    print  

print ha
years =[]
for i in ha:
    years.append(Counter(i))
print years    

for x in range(2002, 2015):
    for i in range(len(years)):
        if years[i][x] == 0 :
            years[i][x] = 0
        

def fnx(i) :
    return  years[i].values()  

X = np.arange(2002, 2015)
Y1 = fnx(0)
Y2 = fnx(1)
Y3 = fnx(2)
Y4 = fnx(3)
Y5 = fnx(4)
Y6 = fnx(5)
#
fig, ax = plt.subplots()
x_formatter = ticker.ScalarFormatter(useOffset=False)
y_formatter = ticker.ScalarFormatter(useOffset=False)
ax.yaxis.set_major_formatter(y_formatter)
ax.xaxis.set_major_formatter(x_formatter)
ax.stackplot(X, Y1, Y2, Y3, Y4, Y5, Y6)
plt.show()
