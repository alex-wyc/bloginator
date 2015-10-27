from pymongo import MongoClient
import time

from util import Util


connection = MongoClient()

db = connection['bloginator']
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
This method returns the data of a post given the id of the post.
"""
def get_post_by_id(post_id):
  p = db.posts.find({'postId':post_id})
  return p


"""
This method fetches all the data we have stored on user comments.
"""
def fetch_all_comments():
  comments = db.comments.find()
  return comments


if __name__ == '__main__':
  db.users.drop()
  print db.collection_names()

  res = db.users.find()
  for r in res:
    print r

  print register_user("Bob","butt","Bobby Flay")
  print register_user("Felicity","Nig","Felly Ng")
  print db.users.find()
