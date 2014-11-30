# -*- coding: utf-8 -*-
"""
Topic Mining of Wikipedia literature using LDA method.
"""
from gensim import corpora, models
#from itertools import chain, izip_longest
#from urllib import urlopen
from operator import itemgetter
#import mongo_db
import csv
import numpy as np
from matplotlib import pyplot as plt
#from matplotlib import ticker
from collections import Counter
#import pandas as pd
import nltk.corpus
import Data
import stack_plot
import bars

# load complete papers information and abstracts seperately
papers, abstracts = Data.load_data()    
# load the transformed documents
dictionary, corpus_tfidf, corpus = Data.prepare_data()  
#number_of_topics = 50
def lda_function(number_of_topics):
    """Applies LDA model to the data. 
       Returns the first six terms of the topics as a list of strings,
       the years of publication for the papers of each topic, and the LDA model.
       """
    
    lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary, num_topics=number_of_topics)
    topics = []

    #z = {}
    publish_years = []
    #count = 0

    for i in range(0, number_of_topics):
        temp = lda.show_topic(i, 6)   
        terms = []
        for term in temp:
            terms.append(term[1])
        topics.append(" ".join(terms))
        topic_terms = "TOPIC #" + str(i) + ": "+ ", ".join(terms)
        print topic_terms
        print "-"*80
        print "The contribution of first three terms:"
        print lda.print_topic(i,3)
        year = []
        for k in range(len(papers)) :
            # maximally probable topic for paper k
            if max(lda[corpus[k]],key=itemgetter(1))[0] == i :
            #print 'Article:' + str(papers[k][''])
            #print 'Manual Topic:' +str(papers[k]['Topic(s)'])
            #print 'Year:' + papers[k]['Year']
                #count += 1
                year.append(int(papers[k]['Year']))
                #z = Counter(la)
        publish_years.append(year) 
        
            #la = dict(izip_longest(*[iter(topics)] * 2, fillvalue=papers[k]['Year']))
        print  
    return topics,publish_years,lda   
    
number_of_topics = 50    
topics,publish_years,lda = lda_function(number_of_topics)


def save_results():
    """Saves the generated topics and the papers predicted to belong to each
       topic in csv format for later interpretation"""

    with open('topics.csv', 'wb') as csvfile:
            write_results = csv.writer(csvfile, delimiter = ' ',
                             quotechar=' ', quoting=csv.QUOTE_MINIMAL)
            for index,topic in enumerate(topics):
                write_results.writerow("TOPIC#"+str(index)+" " + topic)
                write_results.writerow(" ")
                for k in range(len(papers)) :
                    if max(lda[corpus[k]],key=itemgetter(1))[0] == index :
                        write_results.writerow('- '+str(papers[k]['']) )  
                write_results.writerow(" ")        
#print ha
def inspect_results():
    """Asks the user for a number of paper and prints the title of paper, 
       the manual topic and the terms of the predicted topic"""
    Topics = [str(index) + ' '  +' '.join(tokenize_topics[index]) for index, i in enumerate(tokenize_topics)]
    elements = []
    for i in range(len(papers))    :
        elements.append({'Article': str(papers[i]['']), 'Manual Topic': str(papers[i]['Topic(s)']), 'Predicted Topic': 'topic #'+Topics[max(lda[corpus[i]],key=itemgetter(1))[0]]})
    print "Compare manual topic with predicted topic"
    element = raw_input('Inspect article (choose a number between 0 and 499, press q to quit): ')
    boundary = [str(i) for i in range(len(papers))]
    while element != 'q':
        if element in boundary:    
            print elements[int(element)]
            element = raw_input('Choose another article or press q to quit: ')
        
        else:
            print 'Try again!'
            element = raw_input('You should choose a number between 0 and 499: ')
                
#years =[]
#for i in publish_years:
#    years.append(Counter(i))
#for x in range(2002, 2015):
#    for i in range(len(years)):
#        if years[i][x] == 0 :
#            years[i][x] = 0                                
def fnx(j) :
    """Takes number of topic and returns a list of the number of papers 
       published from 2002 to 2014 for each topic"""
    years =[]
    for i in publish_years:
        years.append(Counter(i))
    for x in range(2002, 2015):
        for i in range(len(years)):
            if years[i][x] == 0 :
                years[i][x] = 0    
    return  years[j].values()  
    

Y = [fnx(y) for y in range(number_of_topics)]    
X = np.arange(2002, 2015)   
tokenize_topics = [nltk.word_tokenize(topic) for topic in topics]
TopicTitles = [str(index) + ' '  +' '.join(tokenize_topics[index][:2]) for index, i in enumerate(tokenize_topics)]

num_of_papers = [sum(y) for y in Y]
i = 1
popular_topics = []
popular_papers = []
m = max(num_of_papers)
inl = num_of_papers.index(m)
popular_topics.append(num_of_papers.index(m))
popular_papers.append(m)

def la(m, i, inl):
    
        k = max([ind,n] for n,ind in enumerate(num_of_papers) if n not in popular_topics)
        popular_topics.append(k[1])
        popular_papers.append(k[0])
       # popular_papers.append(max(num_of_papers.index(n) for n in num_of_papers if n!=m))
        i += 1 
        m = k[0]
        inl = k[1]
        if i == 5:
            return popular_topics, popular_papers
        else:
            la(m,i, inl)
        

la(m,i,inl)
    
PopularTopicTitles = []  
  
for popular in popular_topics:
    for topic in topics:
        if popular == topics.index(topic):
            PopularTopicTitles.append(str(popular)+topic)
plt.figure(num=4,figsize=(18,16))
labels = PopularTopicTitles + ['other topics'] 
other = len(papers) - sum(popular_papers) 
              
plt.pie(popular_papers + [other], labels=labels,
        autopct='%1.1f%%', shadow=True, startangle=90)
## Set aspect ratio to be equal so that pie is drawn as a circle.
plt.axis('equal')
#
plt.show()             
#        
#        
save_results()
#
stack_plot.stack(number_of_topics, TopicTitles, X, Y)
#
bars.bar_charts(number_of_topics, Y, TopicTitles)
#            
inspect_results()            
        
    

    #print 
    #print 'Which LDA topic maximally describes a document?\n'
    #print 'Article:'+ str(papers[i][''])
#print 'Original document: ' + abstracts[0]
#print 'Preprocessed document: ' + str(texts[0])
#print 'Matrix Market format: ' + str(corpus[0])
    #print 'Topic probability mixture: ' + str(lda[corpus[i]])
    #print 'Maximally probable topic: topic #' + str(max(lda[corpus[i]],key=itemgetter(1))[0])
#print 'TOPIC #0'    
#for i in range(100):
#    
#    if max(lda[corpus[i]],key=itemgetter(1))[0] == 0 :
#      
#        print 'Article:' + str(papers[i][''])
    
#topic_main = [str(max(lda[corpus[i]],key=itemgetter(0))[0]) for i in range(0,100)]
#topic0 = [index for index, i in enumerate(topic_main) if i == '0']
#topic1 = [index for index, i in enumerate(topic_main) if i == '1']
#topic2 = [index for index, i in enumerate(topic_main) if i == '2']
#topic3 = [index for index, i in enumerate(topic_main) if i == '3']
#topic4 = [index for index, i in enumerate(topic_main) if i == '4']
#topic5 = [index for index, i in enumerate(topic_main) if i == '5']
