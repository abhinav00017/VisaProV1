from flask import (Blueprint, redirect, request, url_for, flash)

import os

from services.googlelogin import GoogleLogin

authenticate = Blueprint("authenticate", __name__)

googlelogin = GoogleLogin()


@authenticate.route("/login")
def login():
    response = googlelogin.login()
    if response[1] == 500:
        flash(response[0])
        return redirect("/")
    return redirect(response[0])


@authenticate.route('/callback')
def callback():
    response = googlelogin.callback(request)
    if response[1] == 500:
        flash(response[0])
        return redirect("/")
    return redirect("/visagpt/home")


@authenticate.route("/logout")
def logout():
    response = googlelogin.logout()
    if response[1] == 500:
        flash(response[0])
        return redirect("/")
    return redirect("/logout-successfull")


@authenticate.route("/logout-successfull")
def logoutsuccessfull():
    return "Loggedout Successsfully <a href='/'><button>home</button></a>"