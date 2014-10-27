
from gensim import corpora, models
from itertools import chain
from urllib import urlopen
from operator import itemgetter
import csv
import simplejson as json
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
    

stoplist = set('for a of the and to in'.split())
texts = [[word for word in abstract.lower().split() if word not in stoplist]
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
lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=50)
for i in range(0, 50):
    temp = lda.show_topic(i, 10)
    terms = []
    for term in temp:
        terms.append(term[1])
    print "Top 10 terms for topic #" + str(i) + ": "+ ", ".join(terms)
    
print 
print 'Which LDA topic maximally describes a document?\n'
print 'Original document: ' + abstracts[0]
print 'Preprocessed document: ' + str(texts[0])
print 'Matrix Market format: ' + str(corpus[0])
print 'Topic probability mixture: ' + str(lda[corpus[0]])
print 'Maximally probable topic: topic #' + str(max(lda[corpus[0]],key=itemgetter(0))[0])
