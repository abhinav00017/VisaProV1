from flask import (Blueprint, redirect, request, url_for, flash, render_template, session)

import os

from decorators import login_is_required

from db.records import Records

records = Records() 

profile = Blueprint("profile", __name__)

@profile.route('/profile/newuser', methods=['POST'])
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

@profile.route('/profile')
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
    return render_template('/profile/index.html', username=data['user_name'], email=email, country=data['country'], phonenumber=data['phonenumber'])

@profile.route('/profile/update', methods=['POST'])
@login_is_required
def profile_update(status=None):
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
    # return redirect("/profile")
    return {"status": "Profile Updated Successfully"}