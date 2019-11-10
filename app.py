import os
from flask import Flask,render_template, request,json,jsonify
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, send_file, send_from_directory

app = Flask(__name__)

@app.route('/result')
def result():
    data = request.args.get('data')
    # data_1 = [].append(json.loads(data))
    # print(data_1)
    return data

@app.route('/signup')
def signUp():
    data = [ 
            {"IP":"1.1.1.1",
             "CONFIG1": "blah",
             "CONFIG2": "bleh"
            }, 
           
            {"IP":"2.2.2.2",
              "CONFIG1": "blah2",
              "CONFIG2": "bleh2",
            },

            {"IP":"3.3.3.3",
              "CONFIG1": "blah3",
              "CONFIG2": "bleh3",
            }

           ]
    return render_template('signUp.html', data=data)

if __name__=="__main__":
    app.run(debug=True)
