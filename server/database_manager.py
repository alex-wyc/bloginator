from pymongo import MongoClient
import time

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
def add_post(username, title, content, timestamp): # tested
    ps = list(db.posts.find({'title':title, 'username':username}))
    if ps == []:
        post = {"username" : username,
                "title" :  title,
                "content" : content,
                "timestamp" : timestamp}
        db.posts.insert(post)
        return True
    else:
        return False
"""
This method fetches all the data we have stored on registered users.
Returns a list of dictionary in the form of users
"""
def fetch_all_users(): # tested
    users = db.users.find()
    return list(users)

def edit_post(oldtitle, author, title, content, timestamp): # tested
    posts = fetch_all_posts()
    for post in posts:
        if post['username'] == author and post['title'] == title:
            return False

    a = db.posts.update(
        {"title": oldtitle, "username":author}, 
        {"$set": {
            "title": title, 
            "content": content, 
            "timestamp": timestamp}}
    )
    return a['updatedExisting']
 
def fetch_all_posts(): # tested
    return list(db.posts.find().sort([("timestamp", 1)]))

"""
This registers a user and adds them to the database assuming all validity
checks have passed on the username except for uniqueness. This function
will return True if the registration was successful and False if there
already exists a user with given username.
"""
def register_user(username, password, fullname): # tested
  us = list(db.users.find({'username':username}))
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
def fetch_all_comments(postTitle, postAuthor):# tested
    comments = list(db.comments.find({'postTitle':postTitle, 'postAuthor':
        postAuthor}))
    return comments

'''
Adds a comment to a given post
returns false if post doesn't exist
'''
def add_comment(postTitle, postAuthor, author, comment, timestamp): #tested
    ps = list(db.posts.find({'title':postTitle, 'username':postAuthor}))
    if ps == []:
        return False;
    comment = {'postTitle': postTitle,
               'postAuthor': postAuthor,
               'username': author,
               'content': comment,
               'timestamp': timestamp}
    db.comments.insert(comment)
    return True

if __name__ == "__main__":
    db.drop_collection('users')
    db.drop_collection('posts')
    db.drop_collection('comments')
    print register_user("hiWorld", '12345', 'yicheng')
    print register_user("alex-wyc", '12345', 'yicheng')
    print fetch_all_users()
    print add_post("hiWorld", 'test1', "this is a test", 15)
    print add_post("hiWorld", 'test1', "this is a test", 15)
    print add_post("alex-wyc", 'test1', 'this is a test', 6)
    print fetch_all_posts()
    print edit_post("test1", "alex-wyc", "test2", "this is another test", 10)
    print edit_post("test5", "hiWorld", 'test5', 'this should not show up', 10)
    print edit_post("test2", "alex-wyc", 'test2', 'this should not show up either', 20)
    print fetch_all_posts()
    print get_post_by_title_and_author("test2", "alex-wyc")
    print add_comment('test2', 'alex-wyc', 'hiWorld', 'this is a comment', 10)
    print fetch_all_comments('test2', 'alex-wyc')
    print fetch_all_comments('test3', 'dne')
