import os
from flask import Flask,render_template, request,json,jsonify, session
from flask import Blueprint, render_template, redirect, url_for, request, flash, session, send_file, send_from_directory
from collections import OrderedDict
import re
from flask_restful import Resource, Api
import os
import json

# for logging testing
from logging.handlers import RotatingFileHandler
from flask import Flask, request, jsonify
from time import strftime
import logging
import traceback
# end for logging testing

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
    


@app.after_request
def after_request(response):
    """ Logging after every request. """
    # This avoids the duplication of registry in the log,
    # since that 500 is already logged via @app.errorhandler.
    if response.status_code != 500:
        ts = strftime('[%Y-%b-%d %H:%M]')
        logger.error('%s %s %s %s %s %s',
                      ts,
                      request.remote_addr,
                      request.method,
                      request.scheme,
                      request.full_path,
                      response.status)
    return response

@app.errorhandler(Exception)
def exceptions(e):
    """ Logging after every Exception. """
    ts = strftime('[%Y-%b-%d %H:%M]')
    tb = traceback.format_exc()
    logger.error('%s %s %s %s %s 5xx INTERNAL SERVER ERROR\n%s',
                  ts,
                  request.remote_addr,
                  request.method,
                  request.scheme,
                  request.full_path,
                  tb)
    return "Internal Server Error", 500

@app.route("/d3")
def d3():
    print("")
    return render_template('d3.html')

@app.route("/d3_data")
def d3_data():
  path = os.getcwd()
  print("current path -----> ", path)
  with open (path + "/static/data/d3_data.json", "r") as f:
    data_dict = json.load(f)
    print("data_array -----> ", data_dict)
    
  return json.dumps(data_dict)

@app.route("/d3_data1")
def d3_data1():
  path = os.getcwd()
  print("current path -----> ", path)
  with open (path + "/static/data/miserables.json", "r") as f:
    data_dict = json.load(f)
    print("data_array -----> ", data_dict)

@app.route("/d3_data2")
def d3_data2():
  path = os.getcwd()
  print("current path -----> ", path)
  with open (path + "/static/data/d3_data2.json", "r") as f:
    data_dict = json.load(f)
    print("data_array -----> ", data_dict)
    
  return json.dumps(data_dict)

# @app.route("/path")
# def path():
#   path = os.getcwd()
#   print("current path -----> ", path)
#   with open ("/static/data/d3_data.json", r) as f:
#     data_array = f.readlines()
#   return json.dumps(data_array) 
  
@app.route("/network")
def d3_network():
    print("in d3 network")
    return render_template('network.html')

@app.route("/network1")
def d3_network1():
    print("in d3 network1")
    return render_template('network1.html')

@app.route("/network2")
def d3_network2():
    print("in d3 network2")
    return render_template('network2.html')

@app.route("/network3")
def d3_network3():
    print("in d3 network3")
    return render_template('network3.html')


@app.route("/tree_view")
def tree_view():
  data =  [
    {
        "num": "1",
        "card_id": "5/6",
        "card_type": "130SCX10"
    },
    {
        "num": "2",
        "card_id": "8/6",
        "card_type": "260SCX2"
    },
    {
        "num": "3",
        "card_id": "10/6",
        "card_type": "130SCX10"
    },
    {
        "num": "4",
        "card_id": "5/8",
        "card_type": "130SCX10"
    },
    {
        "num": "5",
        "card_id": "8/8",
        "card_type": "260SCX2"
    },
    {
        "num": "6",
        "card_id": "2/10",
        "card_type": "130SCX10"
    },
    {
        "num": "7",
        "card_id": "8/10",
        "card_type": "260SCX2"
    },
    {
        "num": "8",
        "card_id": "3/12",
        "card_type": "130SCX10"
    },
    {
        "num": "9",
        "card_id": "5/12",
        "card_type": "130SCX10"
    },
    {
        "num": "10",
        "card_id": "8/12",
        "card_type": "260SCX2"
    },
    {
        "num": "11",
        "card_id": "3/16",
        "card_type": "130SCX10"
    },
    {
        "num": "12",
        "card_id": "6/6",
        "card_type": "260SCX2"
    },
    {
        "num": "13",
        "card_id": "6/4",
        "card_type": "260SCX2"
    },
    {
        "num": "14",
        "card_id": "2/14",
        "card_type": "260SCX2"
    },
    {
        "num": "15",
        "card_id": "9/14",
        "card_type": "260SCX2"
    },
    {
        "num": "16",
        "card_id": "4/14",
        "card_type": "130SCX10"
    },
    {
        "num": "17",
        "card_id": "6/12",
        "card_type": "130SCX10"
    },
    {
        "num": "18",
        "card_id": "2/12",
        "card_type": "260SCX2"
    },
    {
        "num": "19",
        "card_id": "1/12",
        "card_type": "130SCX10"
    },
    {
        "num": "20",
        "card_id": "7/16",
        "card_type": "260SCX2"
    },
    {
        "num": "21",
        "card_id": "10/8",
        "card_type": "130SCX10"
    },
    {
        "num": "22",
        "card_id": "9/16",
        "card_type": "130SCX10"
    },
    {
        "num": "23",
        "card_id": "5/11",
        "card_type": "130SCX10"
    },
    {
        "num": "24",
        "card_id": "10/16",
        "card_type": "130SCX10"
    },
    {
        "num": "25",
        "card_id": "10/4",
        "card_type": "130SCX10"
    },
    {
        "num": "26",
        "card_id": "10/10",
        "card_type": "130SCX10"
    },
    {
        "num": "27",
        "card_id": "6/14",
        "card_type": "130SCX10"
    },
    {
        "num": "28",
        "card_id": "5/16",
        "card_type": "130SCX10"
    },
    {
        "num": "29",
        "card_id": "6/16",
        "card_type": "130SCX10"
    },
    {
        "num": "30",
        "card_id": "8/16",
        "card_type": "130SCX10"
    },
    {
        "num": "31",
        "card_id": "8/2",
        "card_type": "130SCX10"
    },
    {
        "num": "32",
        "card_id": "7/4",
        "card_type": "130SCX10"
    },
    {
        "num": "33",
        "card_id": "4/8",
        "card_type": "130SCX10"
    },
    {
        "num": "34",
        "card_id": "4/6",
        "card_type": "130SCX10"
    },
    {
        "num": "35",
        "card_id": "3/8",
        "card_type": "130SCX10"
    },
    {
        "num": "36",
        "card_id": "2/6",
        "card_type": "130SCX10"
    },
    {
        "num": "37",
        "card_id": "11/12",
        "card_type": "130SCX10"
    },
    {
        "num": "38",
        "card_id": "11/4",
        "card_type": "130SCX10"
    },
    {
        "num": "39",
        "card_id": "11/6",
        "card_type": "260SCX2"
    },
    {
        "num": "40",
        "card_id": "11/8",
        "card_type": "260SCX2"
    },
    {
        "num": "41",
        "card_id": "11/14",
        "card_type": "130SCX10"
    }
]

  data_sorted = []
  
  data.sort(key=(lambda x: int(x["card_id"].split("/")[0])))
  # data was sorted by slot
  # print(json.dumps(data, indent=4))
  # get slot number put in array
  slot_card_array = []
  slot_number = int(data[0]['card_id'].split("/")[0])
    
  for item in data:
    if slot_number != int(item['card_id'].split("/")[0]):
      #deal with slot_card-array previously stored items
      slot_card_array.sort(key=(lambda x: int(x["card_id"].split("/")[1])))
      for x in slot_card_array:
        data_sorted.append(x)
      slot_card_array = []
      slot_number = int(item['card_id'].split("/")[0])
      #append this first item in next slot 
      slot_card_array.append(item)

    else:  
      slot_card_array.append(item)
    
  #deal with last slot as there's no trigger to add the element
  slot_card_array.sort(key=(lambda x: int(x["card_id"].split("/")[1])))  
  for x in slot_card_array:
    data_sorted.append(x)
  
   
  print(json.dumps(data_sorted, indent=4))
  print("size after sorted ----->", len(data_sorted))
  print("size original ----->", len(data))
  return render_template('tree_view.html', data1=json.dumps(data_sorted))


from datetime import datetime, time
import random
import time
begin = time.time()
@app.route("/fetch_random_data")
def fetch_random():
  global begin
  
  # random_number = random.randint(1, 100)
  end = time.time()
  time_elapsed = int ((end - begin) / 60)
  return json.dumps({"number":time_elapsed})


if __name__=="__main__":
    
    # maxBytes to small number, in order to demonstrate the generation of multiple log files (backupCount).
    handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
    # getLogger(__name__):   decorators loggers to file + werkzeug loggers to stdout
    # getLogger('werkzeug'): decorators loggers to file + nothing to stdout
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.ERROR)
    logger.addHandler(handler)
    app.run(debug=True, port=5001)
