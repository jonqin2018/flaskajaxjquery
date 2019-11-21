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
    string_var = "192.168.1.1"

    session["cli_username"] = "cli_username_value"
    session["cli_password"] = "cli_password_value"

    return render_template('apphome.html', data=data, string_var=string_var)

@app.route('/fetch')
def fetch():
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
    string_var = "192.168.1.1"

    session["cli_username"] = "cli_username_value"
    session["cli_password"] = "cli_password_value"

    return jsonify(data)


@app.route('/TechType_fix_config')
#Process selected checkbox
def techType_config():
    """
    input: data received from UI in below format, 
           {
                "ipaddress": ["wp-nr-351"]
                "package": "{'17': 'config xc 17 usertech zatech 14,11', '37': 'config xc 37 usertech zatech 12,10', '36': 'config xc 36 usertech zatech 12,10'}"
            }                       
           cli_username: is from session["cli_username"]
           cli_password: is from session["cli_password"]
    output: output_data
    """
    data = request.args.get('data')
    data_dict = json.loads(data)
    ne_ipaddress = data_dict["ipaddress"] # list []
    config_dict = json.loads(data_dict["package"].replace("\'", "\""))
    # print(type(config_dict))
    # print(json.dumps(config_dict,indent=4))
    
    cmds = config_dict# list []
    
    # print("ne_ipaddress --> ", ne_ipaddress)
    # print("cmds -- > ", cmds)
    username = session["cli_username"]
    password = session["cli_password"]

    ############ WARNING CONFIGURATION#############
    # 
    # nokia_excute_cmd(ne_ipaddress,cmds, username, password) 
    #
    #################

    # return 'show xc xcid' for verification
   
    for item in cmds:
       
        print(item)
    
    # print(json.dumps(output_data))
 
    return json.dumps(config_dict)


@app.route('/form_process')
def form_process():
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
    data_from_form_input = request.args.get('q')
    print(data)
    flash("got data")
    return render_template('apphome.html', form_data = data_from_form_input , data=data, string_var="")

if __name__=="__main__":
    app.run(debug=True, port=5001)
