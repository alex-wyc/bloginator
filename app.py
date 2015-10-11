from flask import Flask
from flask import render_template, sessions
from flask.ext.bower import Bower

app = Flask(__name__)
Bower(app)
  
@app.route("/")
def home():
    return render_template('index.html')

if __name__ == '__main__':
  app.debug = True
  app.run(host='0.0.0.0', port=8080)


