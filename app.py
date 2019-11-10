import os
from flask import Flask,render_template, request,json,jsonify, session
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, send_file, send_from_directory

app = Flask(__name__)


app.config['SECRET_KEY'] = 'the random string' 

@app.route('/result')
def result():
    data = request.args.get('data')
    # data_1 = [].append(json.loads(data))
    # print(data_1)
    return data

@app.route('/')
def first_page():
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
    string_var = "This is a string"

    session["cli_username"] = "cli_username_value"
    session["cli_password"] = "cli_password_value"

    return render_template('apphome.html', data=data, string_var=string_var)

if __name__=="__main__":
    app.run(debug=True)
