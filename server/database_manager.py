# This class handles the all queries to the database to get or modify
# data.
# Author: Alvin Lin (alvin.lin@stuypulse.com)

import sqlite3
import time

from util import Util

DATABASE = 'db/bloginator.db'

class DatabaseManager():
  def __init__(self, database):
    self.database = database

  @staticmethod
  def create():
    connection = sqlite3.connect(DATABASE);
    c = connection.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
              username text NOT NULL PRIMARY KEY,
              password text NOT NULL,
              fullname text NOT NULL);
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS posts (
              username text NOT NULL,
              content text,
              timestamp real NOT NULL)
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS comments (
              postId text NOT NULL,
              username text NOT NULL,
              content text,
              timestamp real NOT NULL)
              """)
    connection.commit()
    connection.close()
    return DatabaseManager(DATABASE)
  """
  This registers a user and adds them to the database assuming all validity
  checks have passed on the username except for uniqueness. This function
  will return True if the registration was successful and False if there
  already exists a user with given username.
  """
  def register_user(self, username, password, fullname):
    connection = sqlite3.connect(self.database);
    c = connection.cursor()
    result = True
    try:
      c.execute('INSERT INTO users VALUES (?, ?, ?)',
                (username, Util.hash(password), fullname))
    except sqlite3.IntegrityError:
      result = False
    connection.commit()
    connection.close()
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
  def add_post(self, username, content):
    connection = sqlite3.connect(self.database)
    c = connection.cursor()
    c.execute('INSERT INTO posts VALUES (?, ?, ?)',
              (username, content, time.time()))
    connection.commit()
    connection.close()

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
  """
  def fetch_all_posts(self):
    connection = sqlite3.connect(self.database)
    c = connection.cursor()
    c.execute('SELECT * FROM posts')
    posts = c.fetchall()
    connection.close()
    return posts

  """
  This method fetches all the data we have stored on user comments.
  """
  def fetch_all_comments(self):
    connection = sqlite3.connect(self.database)
    c = connection.cursor()
    c.execute('SELECT * FROM comments')
    comments = c.fetchall()
    connection.close()
    return comments

if __name__ == '__main__':
  d = DatabaseManager.create()
  print d.register_user('username', 'password', 'blah')
  print d.register_user('bob', 'de bilder', 'blah')
  d.add_post('bob', 'yo')
