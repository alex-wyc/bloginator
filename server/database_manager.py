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
              timestamp integer NOT NULL)
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS comments (
              postId text NOT NULL,
              username text NOT NULL,
              content text,
              timestamp integer NOT NULL)
              """)
    connection.commit()
    connection.close()
    return DatabaseManager(DATABASE)

  # This registers a user and adds them to the database assuming all validity
  # checks have passed on the username except for uniqueness. This function
  # will return True if the registration was successful and False if there
  # already exists a user with given username.
  def register_user(self, username, password):
    connection = sqlite3.connect(self.database);
    c = connection.cursor()
    result = True
    try:
      c.execute('INSERT INTO users VALUES (?, ?)',
                (username, Util.hash(password)))
    except sqlite3.IntegrityError:
      result = False
    connection.commit()
    connection.close()
    return result

  def is_user_authorized(self, username, password):
    connection = sqlite3.connect(self.database)
    c = connection.cursor()
    # We can assume username is a unique field.
    c.execute('SELECT password FROM users WHERE username=?',
              (username,))
    actual_password = str(c.fetchone()[0])
    connection.close()
    return actual_password == Util.hash(password)

  def add_post(self, username, content):
    connection = sqlite3.connect(self.database)
    c = connection.cursor()
    c.execute('INSERT INTO posts VALUES (?, ?, ?',
              (username, content, time.time()))
    connection.commit()
    connection.close()

  def fetch_all_users(self):
    connection = sqlite3.connect(self.database)
    c = connection.cursor()
    c.execute('SELECT * FROM users');
    users = c.fetchall()
    connection.close()
    return users

  def fetch_all_posts(self):
    connection = sqlite3.connect(self.database)
    c = connection.cursor()
    c.execute('SELECT * FROM posts')
    posts = c.fetchall()
    connection.close()
    return posts

  def fetch_all_comments(self):
    connection = sqlite3.connect(self.database)
    c = connection.cursor()
    c.execute('SELECT * FROM comments')
    comments = c.fetchall()
    connection.close()
    return comments

if __name__ == '__main__':
  d = DatabaseManager.create()
  print d.register_user('username', 'password')
  print d.register_user('bob', 'de bilder')
  d.add_post('bob', 'yo')
