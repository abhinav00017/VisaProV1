import os
from flask import Flask, request, session, redirect, render_template, jsonify, url_for
from flask_session import Session
from functools import wraps
from datetime import timedelta
import json

from werkzeug.middleware.proxy_fix import ProxyFix

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build
from google.auth.exceptions import GoogleAuthError

from utils.backendopenai import BackendOpenAI

from blueprints.authenticate import authenticate
from blueprints.landing import landing
from blueprints.visagpt import visagpt

from db.records import Records

from decorators import login_is_required

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

app.register_blueprint(authenticate)
app.register_blueprint(landing)
app.register_blueprint(visagpt)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
Session(app)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

records = Records()

BackendOpenAI = BackendOpenAI(os.getenv('OPENAI_API_KEY'))

@app.route("/save_user_data", methods=['POST'])
@login_is_required
def save_user_data(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    data = request.get_json()
    print(data)
    email = session["email"]
    data['email'] = email
    print(records.create_record(data))
    return "Data Saved Successfully"


@app.route("/add_new_user_data")
@login_is_required
def add_new_user_data(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    return render_template('/frontend/Add_new_user_data.html')


@app.route("/threads")
@login_is_required
def thread(status=None):
    print(session)
    if status == "loggedout":
        return redirect("/login_landing")
    email = session["email"]
    data = records.retrieve_record(email)
    print(data)
    if data.get("threads") == None:
        data["threads"] = []
        return json.dumps({
            "threads_list": data["threads"]
        })
    return json.dumps({
        "threads_list": data["threads"]
    })


@app.route('/add_thread', methods=['GET', 'POST'])
@login_is_required
def newUser(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    thread_data = BackendOpenAI.create_thread()
    print(thread_data)
    email = session["email"]
    data = records.retrieve_record(email)
    print(data)
    if data["threads"] != None:
        data["threads"].append(thread_data)
    else:
        data["threads"] = [thread_data]
    data['email'] = email
    print(records.update_record(data))
    return thread_data


@app.route('/add_user', methods=['POST'])
@login_is_required
def addUser(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    data = request.get_json()
    print(data)
    email = session["email"]
    data['email'] = email
    print(records.create_record(data))
    return "true"


@app.route('/getuser', methods=['GET', 'POST'])
@login_is_required
def getUser(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    data = request.get_json()
    thread_id = data['thread_id']
    response_data = BackendOpenAI.get_thread(thread_id)
    print(response_data)
    return response_data


@app.route('/modifyuser', methods=['PUT'])
@login_is_required
def modifyUser(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    data = request.get_json()
    print(data)
    thread_id = data['thread_id']
    action = data['action']
    response_data = BackendOpenAI.modify_thread(thread_id, action)
    print(response_data)
    return f"<h1>Thread Id {response_data}</h1>"


@app.route('/deleteuser', methods=['DELETE'])
@login_is_required
def deleteUser(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    data = request.get_json()
    thread_id = data['thread_id']
    response_data = BackendOpenAI.delete_thread(thread_id)
    print(response_data)
    return f"<h1>Thread Id {response_data}</h1>"


@app.route('/chat', methods=['POST'])
@login_is_required
def chat(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    message = request.json.get('message')
    thread_id = request.json.get('threadId')
    response_data_1 = BackendOpenAI.query_inserstion(thread_id, message)
    print(response_data_1)
    response_data_2 = BackendOpenAI.run_thread(thread_id)
    print(response_data_2)
    response_data_3 = BackendOpenAI.run_thread_status(thread_id)
    while response_data_3['data'][0]['status'] != 'completed':
        print(response_data_3['data'][0]['status'],
              '----', response_data_3['data'][0]['id'])
        response_data_3 = BackendOpenAI.run_thread_status(thread_id)
    print(response_data_3)
    response_data_4 = BackendOpenAI.get_thread_response(thread_id)
    response_answer = response_data_4['data'][0]['content'][0]['text']['value']
    threads = session.get('threads', [])
    for i in threads:
        if i['id'] == thread_id:
            i['messages'].append({'sender': 'user', 'content': message})
            i['messages'].append(
                {'sender': 'assistant', 'content': response_answer})
    return jsonify({'response': response_answer, 'threadId': thread_id})


def load_chat(thread_id):
    # thread_id = request.json.get('threadId')
    thread = BackendOpenAI.get_thread_data(thread_id)
    print(thread)
    messages = []
    for message in thread['data']:
        messages.append({
            'id': message['id'],
            'sender': message['role'],
            'content': message['content'][0]['text']['value']
        })
    messages = messages[::-1]
    history = {
        'id': thread_id,
        'title': thread_id,
        'messages': messages
    }
    
    session["threads"].append(history)
    print(session["threads"])
    return jsonify(session["threads"])


@app.route('/threads/<string:thread_id>', methods=['GET'])
def get_data(thread_id):
    threads = session.get('threads', [])
    thread = None
    print("one ", threads)
    print(thread_id)
    if threads != []:
        thread = next((t for t in threads if t['id'] == thread_id), None)
    if thread == None:
        load_chat(thread_id)
        print("two ", threads)
        thread = next((t for t in threads if t['id'] == thread_id), None)
    print("three ", thread)
    if thread:
        return jsonify(thread)
    return jsonify({'error': 'Thread not found'}), 404


@app.route('/profile_page')
@login_is_required
def profile_page(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    email = session["email"]
    data = records.retrieve_record(email)
    if data == None:
        return redirect("/add_new_user_data")
    if data.get('phonenumber') == None:
        data['phonenumber'] = ''
    else:
        data['phonenumber'] = data.get('phonenumber')
    return render_template('/frontend/Profile.html', username=data['user_name'], email=email, country=data['country'], phonenumber=data['phonenumber'])


@app.route('/update_profile', methods=['POST'])
@login_is_required
def update_profile(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    update_data = request.get_json()
    email = session["email"]
    data = records.retrieve_record(email)
    data['user_name'] = update_data['user_name']
    data['country'] = update_data['country']
    data['email'] = update_data['email']
    data['phonenumber'] = update_data['phonenumber']
    print(records.update_record(data))
    return {"status": "Profile Updated Successfully"}


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=False)
    app.run(port=8080,debug=False)
