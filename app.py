import os
from flask import Flask,render_template, request,json,jsonify
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, send_file, send_from_directory

app = Flask(__name__)

@app.route('/result')
def result():
    data = request.args.get('data')
    data_1 = [].append(json.loads(data))
    print(data_1)
    return data

@app.route('/signup')
def signUp():
    data = {"ip":"1.1.1.1",
          "config1": "blah",
          "config2": "bleh"
           }
    return render_template('signUp.html', data=data)

# @app.route('/signupuser', methods=['POST'])
# def signupuser():
#     # test = request.args.get('mydata')
#     # print(test)
#     # print("something is not right")
#     # # user =  request.form['username'];
#     # # password = request.form['password'];
#     return json.dumps({'status':'200!'})

if __name__=="__main__":
    app.run(debug=True)
