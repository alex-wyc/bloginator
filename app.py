from flask import Flask
from flask import redirect, render_template, request, session
from flask.ext.bower import Bower

from server.database_manager import DatabaseManager
from server.util import Util

app = Flask(__name__)
dbm = DatabaseManager.create()


@app.route('/')
@app.route('/home')
def home():
  #user = session['user']
  return render_template('index.html')


@app.route('/post', methods=['GET', 'POST'])
def post():
  if request.method == 'GET':
    return redirect('/')
  return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    return render_template('signup.html')

  fullname = request.form['fullname']
  username = request.form['username']
  password = request.form['password']
  confirm_password = request.form['confirmpassword']
  print request.form

  # Check the validity of the username.
  if Util.checkUsername(username) and password == confirm_password:
    # If the username was valid, attempt to register the user.
    if dbm.register_user(username, password, fullname):
      # If the registration was successful, redirect them to the
      # homepage.
      session['user'] = username
      return redirect('/')
    # If the registration was not successful, keep them here and
    # tell them the error.
    return render_template('signup.html', message='Username taken')
  # If their username was invalid, tell them so.
  return render_template('signup.html', message='Invalid username')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return redirect('/')

  # Logs the user in if they are authorized.
  username = request.form['username']
  password = request.form['password']
  if dbm.is_user_authorized(username, password):
    session['user'] = username
    return render_template('dashboard.html', user=username)
  return render_template('index.html', message='invalid credentials')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
  if session.get('user', None):
    del session['user']
  return redirect('/')


if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=8080)

