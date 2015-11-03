import jinja2
from flask import Flask
from flask import redirect, render_template, request, session
from functools import wraps
import datetime

from pymongo import MongoClient
#need to remove sql thing
from server.database_manager import *

app = Flask(__name__)


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if "user" not in session or session["user"] == 0:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function
  

@app.route('/')
@app.route('/home')
def home():
  user = session.get('user', None)
  posts = fetch_all_posts()
  print user
  print posts
  return render_template('index.html', user=user, posts=posts)


@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
  if request.method == 'GET':
    return redirect('/')

  user = session.get('user', None)
  title = request.form.get('title', '').strip()
  content = request.form.get('content', '').strip()
  timestamp = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")
  if user:
    add_post(user, title, content,timestamp)
  return redirect('/')

@app.route('/myposts')
@login_required
def myposts():
    user = session.get('user',None)
    posts = get_posts_by_author(user)
    return render_template('myposts.html',user=user,posts=posts)

@app.route('/edit/<post_id>', methods=['GET', 'POST'])
@login_required
def edit(post_id):
  if request.method == 'GET':
    user = session.get('user',None)
    posts = get_posts_by_user(user)
    app.jinja_env.add_extension(jinja2.ext.loopcontrols)
    return render_template('edit.html',user = user, posts = posts,post_id = int(post_id))

  title = request.form.get('title', '').strip()
  content = request.form.get('content', '').strip()
  timestamp = datetime.datetime.now().strftime("%A, %d. %B %Y %I:%M%p")

  user = session.get('user', None)
  if user:
    post = get_post_by_id(post_id)
    if post and post[1] == user:
      edit_post(post_id, title, content, timestamp)
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
  if checkUsername(username) and password == confirm_password:
    # If the username was valid, attempt to register the user.
    if register_user(username, password, fullname):
      # If the registration was successful, redirect them to the
      # homepage.
      session['user'] = username
      return redirect('/')
    # If the registration was not successful, keep them here and
    # tell them the error.
    return render_template('signup.html', message='Username taken.')
  # If their username was invalid, tell them so.
  return render_template('signup.html', message='Invalid username.')


@app.route('/login')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
  if request.method == 'GET':
    return render_template('login.html')

  # Logs the user in if they are authorized.
  username = request.form.get('username', '')
  password = request.form.get('password', '')
  if is_user_authorized(username, password):
    session['user'] = username
    return redirect('/')
  return render_template('index.html', message='Invalid credentials.')


@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
  if session.get('user', None):
    session['user'] = 0;
  return redirect('/')


if __name__ == '__main__':
  app.debug = True
  app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
  app.run(host='0.0.0.0', port=8080)

