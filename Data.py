# -*- coding: utf-8 -*-
"""
Module for loading the papers from DB and transforming the abstracts.
"""
from gensim import corpora, models
import nltk.corpus
import mongo_db

def load_data():
    """
    Load the papers from the database and return them.
    Return their abstracts seperately as well.
    """
    papers = mongo_db.load_from_mongo("wikilit", "papers")
    abstracts = [papers[abstract]['Abstract'] for abstract, i in enumerate(papers)]
    return papers, abstracts

papers, abstracts = load_data()

def prepare_data():
    """
    Tokenize the documents,remove stopwords and words that appear only
    once. Generate and store a bag-of-words dictionary, convert it to
    sparse vectors, and transform it. Return the results.
    """
    stopwords = nltk.corpus.stopwords.words('english')

    texts = [[word for word in abstract.lower().split()
              if word not in stopwords and word.isalpha()
              and word != 'wikipedia'] for abstract in abstracts]
    # romove words that appear only once in all documents
    all_tokens = sum(texts, [])
    tokens_once = set(word for word in set(all_tokens)
                      if all_tokens.count(word) == 1)
    texts = [[word for word in text if word not in tokens_once]
             for text in texts]

    dictionary = corpora.Dictionary(texts)

    corpus = [dictionary.doc2bow(text) for text in texts]

    tfidf = models.TfidfModel(corpus)

    corpus_tfidf = tfidf[corpus]

    return dictionary, corpus_tfidf, corpus
