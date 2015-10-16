from flask import Flask
from flask import redirect, render_template, request, session

from server.database_manager import DatabaseManager
from server.util import Util

app = Flask(__name__)
dbm = DatabaseManager.create()


@app.route('/')
@app.route('/home')
def home():
  user = session.get('user', None)
  posts = dbm.fetch_all_posts();
  return render_template('index.html', user=user, posts=posts)


@app.route('/post', methods=['GET', 'POST'])
def post():
  if request.method == 'GET':
    return redirect('/')

  user = session.get('user', None)
  content = request.form.get('content', '').strip()
  if user and content and content != '':
    dbm.add_post(user, content)
  return redirect('/')


@app.route('/signup', methods=['GET', 'POST'])
def signup():
  if request.method == 'GET':
    return render_template('signup.html')

  fullname = request.form.get('fullname', '')
  username = request.form.get('username', '')
  password = request.form.get('password', '')
  confirm_password = request.form.get('confirmPassword', '')
  
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
    return render_template('signup.html', message='Username taken.')
  # If their username was invalid, tell them so.
  return render_template('signup.html', message='Invalid username.')


@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return redirect('/')

  # Logs the user in if they are authorized.
  username = request.form.get('username', '')
  password = request.form.get('password', '')
  if dbm.is_user_authorized(username, password):
    session['user'] = username
    return render_template('index.html', user=username)
  return render_template('index.html', message='Invalid credentials.')


@app.route('/logout', methods=['GET', 'POST'])
def logout():
  if session.get('user', None):
    session['user'] = 0;
  return redirect('/')


if __name__ == '__main__':
  app.debug = True
  app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
  app.run(host='0.0.0.0', port=8080)

