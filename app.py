import os
from flask import Flask,render_template, request,json

app = Flask(__name__)

@app.route('/')
def hello():
    return 'Welcome to Python Flask!'

@app.route('/signup')
def signUp():
    data = {"ip":"1.1.1.1",
          "config1": "blah",
          "config2": "bleh"
           }
    return render_template('signUp.html', data=data)

@app.route('/signUpUser', methods=['POST'])
def signUpUser():
    user =  request.form['username'];
    password = request.form['password'];
    return json.dumps({'status':'OK','user':user,'pass':password});

if __name__=="__main__":
    app.run(debug=True)
