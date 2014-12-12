# -*- coding: utf-8 -*-
"""
Topic Mining of Wikipedia literature using LDA method.
"""
from gensim import models
from operator import itemgetter
import csv
import numpy as np
from collections import Counter
import nltk.corpus
import Data
import stack_plot
import bars
from toolbox_02450 import clusterval
import piechart
from matplotlib import pyplot as plt
import time

# load complete papers information and abstracts seperately
papers, abstracts = Data.load_data()
# load the transformed documents
dictionary, corpus_tfidf, corpus = Data.prepare_data()

def lda_function(number_of_topics):
    """
    Apply LDA model to the data.
    Return the first six terms of the topics as a list of strings,
    the years of publication for the papers of each topic, and the LDA model.
    """

    lda = models.LdaModel(corpus=corpus_tfidf, id2word=dictionary,
                          num_topics=number_of_topics, iterations=100)

    topics = []

    publish_years = []
    for i in range(0, number_of_topics):
        temp = lda.show_topic(i, 6)
        terms = []
        for term in temp:
            terms.append(term[1])
        topics.append(" ".join(terms))
        year = []
        for k in range(len(papers)):
            # maximally probable topic for paper k
            if max(lda[corpus[k]], key=itemgetter(1))[0] == i:
                year.append(int(papers[k]['Year']))

        publish_years.append(year)

    return topics, publish_years, lda

number_of_topics = 50
start_time_lda = time.time()
topics, publish_years, lda = lda_function(number_of_topics)
elapsed = time.time() - start_time_lda
print "Elapsed time: %s" % elapsed
def save_results():
    """
    Save the generated topics and the papers predicted to belong to each
    topic in csv format for later interpretation.
    """
    with open('topics.csv', 'wb') as csvfile:
        write_results = csv.writer(csvfile, delimiter=' ',
                                   quotechar=' ', quoting=csv.QUOTE_MINIMAL)
        for index, topic in enumerate(topics):
            write_results.writerow("TOPIC#"+str(index)+" " + topic)
            write_results.writerow(" ")
            for k in range(len(papers)):
                if max(lda[corpus[k]], key=itemgetter(1))[0] == index:
                    write_results.writerow('- '+str(papers[k]['']))
            write_results.writerow(" ")

def inspect_results(number_of_topics):
    """
    Show first six terms of topics. Ask the user for a number
    of paper and print the title of paper, the manual topic
    and the terms of the predicted topic.
    """

    for i in range(0, number_of_topics):

        topic_terms = "TOPIC #" + str(i) + ": "+ topics[i]
        print topic_terms
        print "-"*80
        print "The contribution of first three terms:"
        print lda.print_topic(i, 3)
        print

    Topics = [str(index) + ' '  +' '.join(tokenize_topics[index])
              for index, i in enumerate(tokenize_topics)]
    elements = []
    for i in range(len(papers)):
        elements.append({'Article': str(papers[i]['']),
                         'Manual Topic': str(papers[i]['Topic(s)']),
                         'Predicted Topic': 'topic #'
                           +Topics[max(lda[corpus[i]], key=itemgetter(1))[0]]})
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

def fnx(j):
    """
    Take number of topic and return a list of the number of papers
    published from 2002 to 2014 for each topic.
    """
    years = []
    for i in publish_years:
        years.append(Counter(i))
    for x in range(2002, 2015):
        for i in range(len(years)):
            if years[i][x] == 0:
                years[i][x] = 0
    return  years[j].values()


Y = [fnx(j) for j in range(number_of_topics)]
X = np.arange(2002, 2015)
tokenize_topics = [nltk.word_tokenize(topic) for topic in topics]
TopicTitles = [str(index) + ' '  +' '.join(tokenize_topics[index][:2])
               for index, i in enumerate(tokenize_topics)]

manual_topics = [paper['Topic(s)'] for paper in papers]
topics_split = [topic.split(',') for topic in manual_topics]
classLabels = [topic[0] for topic in topics_split]
classNames = sorted(set(classLabels))
classDict = dict(zip(classNames, range(62)))
y = np.mat([classDict[value] for value in classLabels]).T

def validity(tokenize_topics):
    """Measure entropy for different number of topics."""
    Entropy = []
    K = [10, 20, 30, 40, 50]

    for k in K:

        topics, publish_years, lda = lda_function(k)
        tokenize_topics = [nltk.word_tokenize(topic) for topic in topics]
        elements = []
        Topics2 = [index for index, i in enumerate(tokenize_topics)]
        # take the first manual topic for each paper
        for i in range(len(papers)):
            elements.append(Topics2[max(lda[corpus[i]], key=itemgetter(1))[0]])
        # compute cluster validity:
        Entropy.append(clusterval(y, elements)[0])

    plt.figure(5)
    plt.title('Cluster validity')
    plt.hold(True)
    plt.plot(K, Entropy)
    plt.xlabel('Number of topics')
    plt.ylim(0, 1.1)
    plt.show()

    return Entropy

entropy = validity(tokenize_topics)

num_of_papers = [sum(k) for k in Y]

piechart.pie_plot(topics, papers, num_of_papers)

stack_plot.stack(number_of_topics, TopicTitles, X, Y)

bars.bar_charts(number_of_topics, Y, TopicTitles)
inspect_results(number_of_topics)

save_results()
