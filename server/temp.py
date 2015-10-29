from pymongo import MongoClient
import time
import datetime
import random
from util import Util

connection = MongoClient()

db = connection['bloginator']

"""
COLLECTIONS 
users: username, password, fullname
posts: postId, username, title, content, timestamp
comments: postId, username, content, timestamp
"""


def edit_post(post_id, title, content, timestamp):
    db.posts.update(
        {"postId": post_id}, 
        {"$set": {
            "title": title, 
            "content": content, 
            "timestamp": timestamp}}
    )
 
def fetch_all_posts():
    posts = db.posts.find().sort([("timestamp", 1)])
    l = []
    p = []
    for post in posts:
        p = [ post["postId"],
              post["username"],
              post["title"],
              post["content"],
              post["timestamp"]]
        l.append(p)
    return l



  
if __name__ == '__main__':
    print db.collection_names()
    db.user.insert({"username": "Bob"})
    print db.collection_names()
   
""" 
    d = {"postId": "1", 
         "username": "Bob", 
         "title": "The Post", 
         "timestamp": "The Time",
         "content": "Content"
}
    db.posts.drop()
    db.posts.insert(d)
    res = db.posts.find()
    for r in res:
        print r

    timestamp = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
    edit_post("1", "New Title", "New Content", timestamp)
   
    res = db.posts.find()
    for r in res:
        print r

    l = fetch_all_posts()
    print l
"""
