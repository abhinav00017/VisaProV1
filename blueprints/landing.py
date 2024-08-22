from flask import (Blueprint, redirect, request, url_for, flash, render_template, session)

import os

from decorators import login_is_required

from db.records import Records

records = Records()

landing = Blueprint("landing", __name__)

@landing.route('/')
@login_is_required
def home(status=None):
    if status == "loggedout":
        return render_template('landing/index.html')
    data = records.retrieve_record(session["email"])
    if data == None:
        return redirect("/add_new_user_data")
    return redirect('/visagpt/home')

@landing.route("/login_landing")
@login_is_required
def login_landing(status=None):
    if status == "loggedout":
        return render_template('/authenticate/index.html')
    data = records.retrieve_record(session["email"])
    if data == None:
        return redirect("/add_new_user_data")
    return redirect('/visagpt/home')

