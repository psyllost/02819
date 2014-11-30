# -*- coding: utf-8 -*-
"""
Module for loading the papers from DB and transforming them
"""
from gensim import corpora, models
import nltk.corpus
import mongo_db

#def extract_entities():
#    """Reads the webpage, extracts paper entities as a list of dictionaries,
#       and stores in the database"""
#    
#    url = "http://wikilit.referata.com/" + \
#    "wiki/Special:Ask/" + \
#    "-5B-5BCategory:Publications-5D-5D/" + \
#    "-3FHas-20author%3DAuthor(s)/-3FYear/" + \
#    "-3FPublished-20in/-3FAbstract/-3FHas-20topic%3DTopic(s)/" + \
#    "-3FHas-20domain%3DDomain(s)/" +  \
#    "format%3D-20csv/limit%3D-20500/offset%3D0"
#
#
## Get and read the web page
## Object from urlopen has read function
#
#    web = urlopen(url)
#
#    lines = csv.reader(web, delimiter=',', quotechar='"')
#
#    header = []
#    papers = []
#    for row in lines:     
#        line = [unicode(cell, 'utf-8') for cell in row]
#        if not header:     
#            header = line
#            continue   
#        papers.append(dict(zip(header, line)))
#
#
#    abstracts=[]
#    for abstract, i in enumerate(papers):
#        abstracts.append(papers[abstract]['Abstract'])
#    mongo_db.save_to_mongo(papers, "wikilit_mining", "papers") 
#    #mongo_db.save_to_mongo(abstracts, "wikilit_mining", "abstracts")
#    
#extract_entities()    
    
def load_data():
    """Loads the papers from the database and returns them.
       Returns their abstracts seperately as well"""
    papers = mongo_db.load_from_mongo("wikilit_mining","papers")
    abstracts = [papers[abstract]['Abstract'] for abstract,i in enumerate(papers)]
    
    return papers, abstracts
    
papers, abstracts = load_data()    
    
def prepare_data():
    """Tokenizes the documents,remove stopwords and words that appear only 
       once. Generates and stores a bag-of-words dictionary, converts it to
       sparse vectors, and transforms it. Returns the results."""
    stopwords = nltk.corpus.stopwords.words('english')

    texts = [[word for word in abstract.lower().split() 
              if word not in stopwords and word.isalpha() 
                  and word != 'wikipedia'] for abstract in abstracts]
    all_tokens = sum(texts, [])
    tokens_once = set(word for word in set(all_tokens)
                        if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
              for text in texts] 
         
    dictionary = corpora.Dictionary(texts)
    dictionary.save('C:/Users/Ioanna/abstracts.dict')  

    corpus = [dictionary.doc2bow(text) for text in texts]
    corpora.MmCorpus.serialize('C:/Users/Ioanna/abstracts.mm', corpus) 

    dictionary = corpora.Dictionary.load('C:/Users/Ioanna/abstracts.dict')
    corpus = corpora.MmCorpus('C:/Users/Ioanna/abstracts.mm')
    tfidf = models.TfidfModel(corpus) 

    corpus_tfidf = tfidf[corpus]
    
    return dictionary, corpus_tfidf, corpus
