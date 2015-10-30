from pymongo import MongoClient
import time

from util import Util
import hashlib
import re

def hash(text):
    return hashlib.sha256(text).hexdigest()

def checkUsername(username):
    return not re.search('[^a-zA-Z0-9]', username) and len(username) > 0


connection = MongoClient()

db = connection['bloginator']

"""
COLLECTIONS 
users: username, password, fullname
posts: username, title, content, timestamp
comments: postTitle, postAuthor, username, content, timestamp
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

def edit_post(oldtitle, title, content, timestamp):
    db.posts.update(
        {"title": oldtitle}, 
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
        p = [ post["username"],
              post["title"],
              post["content"],
              post["timestamp"]]
        l.append(p)
    return l

"""
This registers a user and adds them to the database assuming all validity
checks have passed on the username except for uniqueness. This function
will return True if the registration was successful and False if there
already exists a user with given username.
"""
def register_user(username, password, fullname):
  us = list(db.users.find({'username':username}))
  print us
  if us == []:
    t = {'username':username, 'password':password, 'fullname':fullname}
    db.users.insert(t)
    result = True
  else:
    result = False
  return result

"""
This method returns the data of a post given the title and author os the post
"""
def get_post_by_title_and_author(post_title, post_author):
    p = list(db.posts.find({'username':post_author, 'title':post_title}))
    return p


"""
This method fetches all the data we have stored on user comments given a
postTitle and post.
"""
def fetch_all_comments(postTitle, postAuthor):
    comments = list(db.comments.find({'postTitle':postTitle, 'postAuthor':
        postAuthor}))
    return comments


