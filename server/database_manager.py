# This class handles the all queries to the database to get or modify
# data.
# Author: Alvin Lin (alvin.lin@stuypulse.com)

import sqlite3

from util import Util

DATABASE = 'db/bloginator.db'

class DatabaseManager():
  def __init__(self, connection):
    self.connection = connection

  @staticmethod
  def create():
    connection = sqlite3.connect(DATABASE);
    c = connection.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
              username text NOT NULL PRIMARY KEY,
              password text NOT NULL);
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS posts (
              postId text NOT NULL PRIMARY KEY,
              username text NOT NULL,
              content text,
              timestamp integer NOT NULL)
              """)
    c.execute("""CREATE TABLE IF NOT EXISTS comments (
              commentId text NOT NULL PRIMARY KEY,
              postId text NOT NULL,
              username text NOT NULL,
              content text,
              timestamp integer NOT NULL)
              """)
    connection.commit()
    connection.close()
    return DatabaseManager(connection)

  def register_user(self, username, password):
    self.connection = sqlite3.connect(DATABASE);
    c = self.connection.cursor()
    result = True
    try:
      c.execute('INSERT INTO users VALUES (?, ?)',
                (username, Util.hash(password)))
    except sqlite3.IntegrityError:
      result = False
    self.connection.commit()
    self.connection.close()
    return result

if __name__ == '__main__':
  d = DatabaseManager.create()
  print d.register_user('username', 'password')
