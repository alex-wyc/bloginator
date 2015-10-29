# This class handles the all queries to the database to get or modify
# data.
# Author: Alvin Lin (alvin.lin@stuypulse.com)

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
  This checks if a user is authorized given their username and password.
  Returns True if and only if the given user exists and the given password
  matches the stored password. Returns False if the given user does not
  exist or the given password does not match the stored one.
  """
  def is_user_authorized(self, username, password):
    connection = sqlite3.connect(self.database)
    c = connection.cursor()
    # We can assume username is a unique field.
    c.execute('SELECT password FROM users WHERE username=?',
              (username,))
    actual_password = c.fetchone()
    connection.close()
    if actual_password:
      return actual_password[0] == Util.hash(password)
    return False

  """
  This method adds a post into the database given the username of the person
  posting and the content of the post.
  """
  def add_post(self, username, title, content, timestamp):
    connection = sqlite3.connect(self.database)
    c = connection.cursor()
    c.execute('INSERT INTO posts VALUES (?, ?, ?, ?)',
              (username, title, content, timestamp))
    connection.commit()
    connection.close()

  """
  This method updates a post given the post id and the new title and content.
  """

   def edit_post(post_id, title, content, timestamp):
     db.posts.update(
       {"postId": post_id}, 
       {"$set": {
         "title": title, 
         "content": content, 
         "timestamp": timestamp}}
     )


  """
  This method returns the data of a post given the id of the post.
  """
  def get_post_by_id(post_id):
    p = list(db.posts.find({'postId':post_id}))
    return p

  """
  This method fetches all the posts from a specific user.
  """
  def get_posts_by_user(self, user):
    connection = sqlite3.connect(self.database)
    c = connection.cursor()
    c.execute("""SELECT rowid,username,title,content,timestamp
              FROM posts WHERE username=?""",
              (user,))
    posts = c.fetchall()
    connection.close()
    return posts
  
  """
  This method fetches all the data we have stored on registered users.
  """
  def fetch_all_users(self):
    connection = sqlite3.connect(self.database)
    c = connection.cursor()
    c.execute('SELECT * FROM users');
    users = c.fetchall()
    connection.close()
    return users

  """
  This method fetches all the data we have stored on user posts.
  Returns a list
  """
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


  """
  This method fetches all the data we have stored on user comments with a specific postId.
  """
  def fetch_all_comments(postId):
    comments = list(db.comments.find({'postId':postId}))
    return comments

if __name__ == '__main__':
  d = DatabaseManager.create()
  print d.register_user('username', 'password', 'blah')
  print d.register_user('bob', 'de bilder', 'blah')
  d.add_post('bob', 'yo')
