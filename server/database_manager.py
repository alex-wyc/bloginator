from pymongo import MongoClient
import time

from util import Util

connection = MongoClient()

db = connection['bloginator']

"""
COLLECTIONS 
users: username, password, fullname
posts: username, title, content, timestamp
comments: postId, username, content, timestamp
"""

"""
This method adds a post into the database given the username of the person
posting and the content of the post.
"""
def add_post(username, title, content, timestamp):
    db.posts.insert(
        {"username" : username},
        {"title" :  title},
        {"content" : content},
        {"timestamp" : timestamp}
    )

"""
This method fetches all the data we have stored on registered users.
Returns a list of dictionary in the form of users
"""
def fetch_all_users():
    users = db.users.find()
    return list(users)


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

