# -*- coding: utf-8 -*-
"""
Module for gathering papers entities from WikiLit and storing them to DB
for later processing. Run it once to save to Mongo.
"""

from urllib import urlopen
import csv
import mongo_db

def extract_entities():
    """
    Read the webpage, extract paper entities as a list of dictionaries,
    and store in the database.
    """

    url = "http://wikilit.referata.com/" + \
    "wiki/Special:Ask/" + \
    "-5B-5BCategory:Publications-5D-5D/" + \
    "-3FHas-20author%3DAuthor(s)/-3FYear/" + \
    "-3FPublished-20in/-3FAbstract/-3FHas-20topic%3DTopic(s)/" + \
    "-3FHas-20domain%3DDomain(s)/" +  \
    "format%3D-20csv/limit%3D-20500/offset%3D0"

    web = urlopen(url)
    lines = csv.reader(web, delimiter=',', quotechar='"')

    header = []
    papers = []
    for row in lines:
        line = [unicode(cell, 'utf-8') for cell in row]
        if not header:
            header = line
            continue
        papers.append(dict(zip(header, line)))

    abstracts=[]
    for abstract, i in enumerate(papers):
        abstracts.append(papers[abstract]['Abstract'])
    mongo_db.save_to_mongo(papers, "wikilit", "papers")


extract_entities()

