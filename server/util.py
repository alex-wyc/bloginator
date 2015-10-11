# This file contains utility methods used on the server side.
# Author: Alvin Lin (alvin.lin@stuypulse.com)

import hashlib

class Util():

  @staticmethod
  def hash(text):
    return hashlib.sha256(text).hexdigest()
