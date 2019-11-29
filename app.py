import os
from flask import Flask,render_template, request,json,jsonify, session
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, send_file, send_from_directory
from collections import OrderedDict
import re
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


# Test API

class HelloWorld(Resource):
    def get(self):
        message = "<pre>class HelloWorld(Resource): def get(self):  return {'hello': 'world' }</pre>"
        return {'hello': 'world', 'message': json.dumps(message),}

api.add_resource(HelloWorld, '/hello')
 
# 
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
    # here data exists because it needs to feed the earlier testing with form. otherwise the data_from_form_input is the data obtained from the
    # auto complete input then returned back to apphome page
    return render_template('apphome.html', form_data = data_from_form_input , data=data, string_var="")


@app.route('/array_test', methods=['GET','POST'])
def array_test():
    data2 = []
    ord_dict = OrderedDict() 
    print(type(ord_dict))
    num = ''
    if request.method == 'POST':
        print("in array_test function...")
        # data = request.args.get('data')
        data1= json.loads(request.get_json())
        # print(data1[0])
        print(json.dumps(data1, indent=4))
        # process dict
            
        
        for item in data1:
          # find the number
          ord_dict = OrderedDict() 
          for key in item.keys():
            print("key type is ----> ", type(key))
            
            if re.findall(r'\d+',key) != []:
                print("i am inside if... ")
                num = re.findall(r'\d+', key)[0]
                print(num)
                # ord_dict[]
                ord_dict["xcid"] = item[num]
                ord_dict[num] = item[num]
                ord_dict["frequency"] = item["frequency"]
                ord_dict["och_trail"] = item["och_trail"]
                ord_dict["och_trail"] = item["och_trail"]
                ord_dict["tech_az"] = item["tech_az"]
                ord_dict["tech_za"] = item["tech_za"]

                data2.append(ord_dict) 

        data2.sort(key=(lambda x: x["xcid"]))
        print(data2)
        return json.dumps(data2)
        
    else: 
        data1 = []
        sorted_data1= []
        return render_template('array_test.html', data = data1 ,  sorted_data = sorted_data1)

@app.route('/doc')
def doc():
  return  render_template('doc.html')

@app.route("/easyui")
def easyui():
  return render_template('easyui.html')

@app.route("/test")
def test():
  return render_template('test.html')

@app.route("/test_js")
def test_js():
  return render_template("test.js")
    


if __name__=="__main__":
    app.run(debug=True, port=5001)
