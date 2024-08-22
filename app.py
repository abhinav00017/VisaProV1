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
from blueprints.profile import profile

from db.records import Records

from decorators import login_is_required

app = Flask(__name__)
app.secret_key = os.urandom(24)

app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

app.register_blueprint(authenticate)
app.register_blueprint(landing)
app.register_blueprint(visagpt)
app.register_blueprint(profile)

app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(days=7)
Session(app)

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='Lax',
)

# records = Records()

# BackendOpenAI = BackendOpenAI(os.getenv('OPENAI_API_KEY'))


# @app.route('/chat', methods=['POST'])
# @login_is_required
# def chat(status=None):
#     if status == "loggedout":
#         return redirect("/login_landing")
#     message = request.json.get('message')
#     thread_id = request.json.get('threadId')
#     response_data_1 = BackendOpenAI.query_inserstion(thread_id, message)
#     print(response_data_1)
#     response_data_2 = BackendOpenAI.run_thread(thread_id)
#     print(response_data_2)
#     response_data_3 = BackendOpenAI.run_thread_status(thread_id)
#     while response_data_3['data'][0]['status'] != 'completed':
#         print(response_data_3['data'][0]['status'],
#               '----', response_data_3['data'][0]['id'])
#         response_data_3 = BackendOpenAI.run_thread_status(thread_id)
#     print(response_data_3)
#     response_data_4 = BackendOpenAI.get_thread_response(thread_id)
#     response_answer = response_data_4['data'][0]['content'][0]['text']['value']
#     threads = session.get('threads', [])
#     for i in threads:
#         if i['id'] == thread_id:
#             i['messages'].append({'sender': 'user', 'content': message})
#             i['messages'].append(
#                 {'sender': 'assistant', 'content': response_answer})
#     return jsonify({'response': response_answer, 'threadId': thread_id})


# def load_chat(thread_id):
#     # thread_id = request.json.get('threadId')
#     thread = BackendOpenAI.get_thread_data(thread_id)
#     print(thread)
#     messages = []
#     for message in thread['data']:
#         messages.append({
#             'id': message['id'],
#             'sender': message['role'],
#             'content': message['content'][0]['text']['value']
#         })
#     messages = messages[::-1]
#     history = {
#         'id': thread_id,
#         'title': thread_id,
#         'messages': messages
#     }
    
#     session["threads"].append(history)
#     print(session["threads"])
#     return jsonify(session["threads"])


# @app.route('/threads/<string:thread_id>', methods=['GET'])
# def get_data(thread_id):
#     threads = session.get('threads', [])
#     thread = None
#     print("one ", threads)
#     print(thread_id)
#     if threads != []:
#         thread = next((t for t in threads if t['id'] == thread_id), None)
#     if thread == None:
#         load_chat(thread_id)
#         print("two ", threads)
#         thread = next((t for t in threads if t['id'] == thread_id), None)
#     print("three ", thread)
#     if thread:
#         return jsonify(thread)
#     return jsonify({'error': 'Thread not found'}), 404


if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8080, debug=False)
    app.run(port=8080,debug=False)
