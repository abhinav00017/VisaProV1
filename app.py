import os
import pathlib
from flask import Flask, request, session, abort, redirect, render_template, jsonify, url_for
from flask_session import Session
from functools import wraps
from datetime import timedelta
import requests
import json

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from utils.backendopenai import BackendOpenAI
from db.records import Records

# from dotenv import load_dotenv
# load_dotenv()

app = Flask(__name__)
app.secret_key = os.urandom(24)

google_client_id = os.getenv('GOOGLE_CLIENT_ID')
google_client_secret = os.getenv('GOOGLE_SECRET_KEY')
google_redirect_uri = os.getenv('GOOGLE_REDIRECT_URI')

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

flow = Flow.from_client_config(
    client_config={
        "web": {
            "client_id": google_client_id,
            "project_id": "your-project-id",  # Optional, for your reference
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": google_client_secret,
            "redirect_uris": [google_redirect_uri],
            "javascript_origins": ["https://visaprov1-app-twl2y.ondigitalocean.app"]
        }
    },
    scopes=["https://www.googleapis.com/auth/userinfo.email",
            "openid", "https://www.googleapis.com/auth/userinfo.profile"],
    redirect_uri=google_redirect_uri
)


@app.route("/login")
def login():
    auth_uri, state = flow.authorization_url(access_type='offline')
    session['state'] = state
    return redirect(auth_uri)


@app.route('/callback')
def callback():
    if 'state' not in session or 'state' not in request.args:
        return 'State parameter missing', 400

    if session.get('state') != request.args['state']:
        return 'State does not match!', 400

    flow.fetch_token(authorization_response=request.url)


    credentials = flow.credentials
    service = build('oauth2', 'v2', credentials=credentials)
    user_info = service.userinfo().get().execute()

    email = user_info.get('email')
    name = user_info.get('name')
    picture = user_info.get('picture')
    google_id = user_info.get('id')

    session["email"] = email
    session["name"] = name
    session["picture"] = picture
    session["google_id"] = google_id
    session["threads"] = [] 

    print("Email: ", email)
    print("Name: ", name)
    print("Picture: ", picture)
    print("Google ID: ", google_id)

    return redirect(url_for('home_screen'))


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/logout-successfull")


@app.route("/logout-successfull")
def logoutsuccessfull():
    return "Loggedout Successsfully <a href='/'><button>home</button></a>"


def login_is_required(function):
    @wraps(function)
    def wrapper(*args, **kwargs):
        if "google_id" not in session:
            kwargs['status'] = "loggedout"  # Authorization required
            return function(*args, **kwargs)
        else:
            email = session["email"]
            print(session)
            return function(*args, **kwargs)
    return wrapper


def login_to_home(function):
    def wrapper1(*args, **kwargs):
        print(session['email'])
        if "google_id" not in session:
            return redirect("/")
        else:
            return redirect("/protected_area")
    return wrapper1


@app.route('/')
@login_is_required
def hello(status=None):
    if status == "loggedout":
        return render_template('/frontend/landingpage.html')
    email = session["email"]
    data = records.retrieve_record(email)
    if data == None:
        return redirect("/add_new_user_data")
    return redirect('/home_screen')


@app.route("/login_landing")
@login_is_required
def login_landing(status=None):
    if status == "loggedout":
        return render_template('/frontend/Login_landing.html')
    email = session["email"]
    data = records.retrieve_record(email)
    if data == None:
        return redirect("/add_new_user_data")
    return redirect('/home_screen')


@app.route("/home_screen")
@login_is_required
def home_screen(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    email = session["email"]
    data = records.retrieve_record(email)
    if data == None:
        return redirect("/add_new_user_data")
    return render_template('/frontend/Home_screen.html', name=session["name"])


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
    app.run(host='0.0.0.0', port=8080, debug=False)
