from flask import (Blueprint, redirect, request, url_for, flash, render_template, session)

import os
import json

from decorators import login_is_required

from db.records import Records

from utils.backendopenai import BackendOpenAI

from 

backendopenai = BackendOpenAI(os.getenv('OPENAI_API_KEY'))
records = Records()

visagpt = Blueprint("visagpt", __name__)

@visagpt.route('/visagpt/home')
@login_is_required
def home(status=None):
    if status == "loggedout":
        return render_template('/frontend/landingpage.html')
    data = records.retrieve_record(session["email"])
    if data == None:
        return redirect("/visagpt/add_new_user_data")
    return render_template('/frontend/Home_screen.html', name=session["name"])

@visagpt.route("/visagpt/add_new_user_data")
@login_is_required
def add_new_user_data(status=None):
    if status == "loggedout":
        return redirect("/login_landing")
    return render_template('/frontend/Add_new_user_data.html')

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
    thread_data = BackendOpenAI.create_thread()
    email = session["email"]
    data = records.retrieve_record(email)
    if data["threads"] != None:
        data["threads"].append(thread_data)
    else:
        data["threads"] = [thread_data]
    data['email'] = email
    records.update_record(data)
    return thread_data