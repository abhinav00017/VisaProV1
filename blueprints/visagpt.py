from flask import (Blueprint, redirect, request, url_for, flash, render_template, session, jsonify)

import os
import json

from decorators import login_is_required

from services.visagpt import Visagpt

from db.records import Records

from utils.backendopenai import BackendOpenAI

from dotenv import load_dotenv

load_dotenv()

backendopenai = BackendOpenAI(os.getenv('OPENAI_API_KEY'))
records = Records()

visagpt = Blueprint("visagpt", __name__)

@visagpt.route('/visagpt/home')
@login_is_required
def home(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    data = records.retrieve_record(session["email"])
    if data == None:
        return redirect("/visagpt/add_new_user_data")
    return render_template('/visagpt/index.html', name=session["name"])

@visagpt.route("/visagpt/add_new_user_data")
@login_is_required
def add_new_user_data(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    return render_template('/registration/index.html')

@visagpt.route("/visagpt/threads")
@login_is_required
def threads(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    email = session["email"]
    data = records.retrieve_record(email)
    if data.get("threads") == None:
        data["threads"] = []
        return json.dumps({
            "threads_list": data["threads"]
        })
    return json.dumps({
        "threads_list": data["threads"]
    })


@visagpt.route('/visagpt/add_thread', methods=['GET', 'POST'])
@login_is_required
def newUser(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    thread_data = backendopenai.create_thread()
    email = session["email"]
    data = records.retrieve_record(email)
    if data["threads"] != None:
        data["threads"].append(thread_data)
    else:
        data["threads"] = [thread_data]
    data['email'] = email
    records.update_record(data)
    return thread_data

@visagpt.route('/visagpt/threads/<string:thread_id>', methods=['GET'])
def get_data(thread_id):
    threads = session.get('threads', [])
    thread = None
    print("one ", threads)
    print(thread_id)
    if threads != []:
        thread = next((t for t in threads if t['id'] == thread_id), None)
    if thread == None:
        Visagpt.load_chat(thread_id)
        print("two ", threads)
        thread = next((t for t in threads if t['id'] == thread_id), None)
    print("three ", thread)
    if thread:
        return jsonify(thread)
    return jsonify({'error': 'Thread not found'}), 404

@visagpt.route('/visagpt/chat', methods=['POST'])
@login_is_required
def chat(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    message = request.json.get('message')
    thread_id = request.json.get('threadId')
    print(thread_id, message)
    response_data_1 = backendopenai.query_inserstion(thread_id, message)
    response_data_2 = backendopenai.run_thread(thread_id)
    response_data_3 = backendopenai.run_thread_status(thread_id)
    while response_data_3['data'][0]['status'] != 'completed':
        print(response_data_3['data'][0]['status'],
              '----', response_data_3['data'][0]['id'])
        response_data_3 = backendopenai.run_thread_status(thread_id)
    print(response_data_3)
    response_data_4 = backendopenai.get_thread_response(thread_id)
    response_answer = response_data_4['data'][0]['content'][0]['text']['value']
    threads = session.get('threads', [])
    for i in threads:
        if i['id'] == thread_id:
            i['messages'].append({'sender': 'user', 'content': message})
            i['messages'].append(
                {'sender': 'assistant', 'content': response_answer})
    return jsonify({'response': response_answer, 'threadId': thread_id})