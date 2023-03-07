from api.cline import Cline
from flask import Flask, request, render_template, redirect
import datetime as dt
import pytz, argparse
import api.keys as keys
import time
import os
from api.utils import *
import json
from dotenv import load_dotenv

load_dotenv()

app         = Flask(__name__)
url         = os.environ.get('URL')

if (url):
    api         = Cline(url=url)
else:
    api         = Cline()

account     = os.environ.get('ACCOUNT')
privatekey  = os.environ.get('PRIVATE_KEY')
table       = 'records'

def get():
    try:
        tableJs = api.get_table(account, account, table, limit=2000)
    except Exception as e:
        tableJs = e
    return tableJs

def push(mod, trans_id, text):
    action = mod
    
    if (action == 'cr' or action == 'up'):
        action_data = {
            "id": int(time.time()) if action == 'cr' else trans_id, 
            "owner": account,
            "data": text
        }
    elif (action == 'dl'):
        action_data = {
            "id": trans_id
        }
    else:
        redirect("/", code=302)

    payload = {
        "account": account,
        "name": action + table,
        "authorization": [{
            "actor": account,
            "permission": "owner",
        }]
    }

    # Converting payload to binary
    data = api.abi_json_to_bin(account, action + table, action_data)
    payload['data'] = data['binargs']

    # final transaction formed
    trx = {"actions": [payload]}
    trx['expiration'] = str((dt.datetime.utcnow() + dt.timedelta(seconds=60)).replace(tzinfo=pytz.UTC))

    key = keys.INRKey(privatekey)
    
    resp = api.push_transaction(trx, key, broadcast=True)
    result = json.dumps(resp, indent = 4) 

    return result

@app.route("/", methods=["POST", "GET"])
def view_index():
    if request.method == "POST":
        message     = request.form['text']
        name        = 'cr'
        trans_id    = ''
        push(name, trans_id, message)
        redirect("/", code=302)
    return render_template("index.html", datas=get())

@app.route("/post_submit", methods=["GET"])
def submit_redirect():
    return redirect("/", code=302)

@app.route("/edit/<data_id>", methods=["POST", "GET"])
def edit_data(data_id):
    f = ''

    if request.method == "POST":
        message     = request.form['text']
        name        = 'up'
        trans_id    = data_id
        f = push(name, trans_id, message)
    elif request.method == "GET":
        message     = ''
        name        = 'dl'
        trans_id    = data_id
        f = push(name, trans_id, message)
    
    if(f):
        redirect("/", code=302)

if __name__ == "__main__":
    app.run(debug=True)
