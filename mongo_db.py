"""

Module for saving, loading  and updating MongoDB
"""

import pymongo

def save_to_mongo(data, mongo_db, mongo_db_coll, **mongo_conn_kw):
    """Saves data to Mongo"""
    client = pymongo.MongoClient(**mongo_conn_kw)
    db = client[mongo_db]
    coll = db[mongo_db_coll]
    return coll.insert(data)

def load_from_mongo(mongo_db, mongo_db_coll, return_cursor=False,
                    criteria=None, projection=None, **mongo_conn_kw):
    """Loads data from Mongo"""   
    client = pymongo.MongoClient(**mongo_conn_kw)
    db = client[mongo_db]
    coll = db[mongo_db_coll]

    if criteria is None:
        criteria = {}
    
    if projection is None:
        cursor = coll.find(criteria)
    else:
        cursor = coll.find(criteria, projection)

    if return_cursor:
        return cursor
    else:
        return [ item for item in cursor ]
    
def update_mongo(update, mongo_db, mongo_db_coll, criteria=None, upsert=False, multi=False, **mongo_conn_kw):
   """Updates Mongo""" 
   client = pymongo.MongoClient(**mongo_conn_kw)
   db = client[mongo_db]
   coll = db[mongo_db_coll]
   
   if criteria is None:
        criteria = {}
#   
   return coll.update(criteria, update, upsert=upsert, multi=multi)
