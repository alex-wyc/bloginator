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
  result = True
  us = db.users.find({'username':username})
  if us is None:
    t = {'username':username, 'password':password, 'fullname':fullname}
    db.users.insert(t)
  else:
    result = False
  return result

"""
This method returns the data of a post given the id of the post.
"""
def get_post_by_id(post_id):
  connection = sqlite3.connect(self.database)
  c = connection.cursor()
  c.execute("""SELECT rowid,username,title,content,timestamp
  FROM posts WHERE rowid=?""",
            (post_id,))
  post = c.fetchone()
  return post


"""
This method fetches all the data we have stored on user comments.
"""
def fetch_all_comments():
  comments = db.comments.find()
  return comments


if __name__ == '__main__':
  print db.collection_names()
  db.user.insert({"username": "Bob"})
  print db.collection_names()
  print register_user("Bob","butt","Bobby Flay")
