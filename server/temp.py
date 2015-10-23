# This class handles the all queries to the database to get or modify
# data.
# Author: Alvin Lin (alvin.lin@stuypulse.com)

from pymongo import MongoClient
import time

from util import Util

connection = MongoClient()

db = connection['bloginator']

    
 
def create():
    
    if ("users" in db.collection_names()):
        db.createCollection("users")
    if ("posts" in db.collection_names()):
        db.createCollection("posts")
    if ("comments" in db.collection_names()):
        db.createCollection("comments")
   




  
if __name__ == '__main__':
    print db.collection_names()
    create()
    print db.collection_names()
