from flask import render_template, request, redirect, Blueprint
from flask_login import login_user, login_required, logout_user, current_user

from werkzeug.security import generate_password_hash, check_password_hash

from db.requests import *

from .data_init import session


blueprint_login = Blueprint(
    'login_api',
    __name__,
    template_folder="./templates"
)


@blueprint_login.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@blueprint_login.route("/account/login")
def login():
    return render_template("login.html")


@blueprint_login.route("/account/registeruser")
def registeruser():
    return render_template("register_user.html")


@blueprint_login.route("/account/registeripp")
def registeripp():
    return render_template("register_ipp.html")


@blueprint_login.route("/account/loginaccount", methods=['POST'])
def loginuser():
    if request.method == 'POST':
        user_login = request.form.get("login")
        password = request.form.get("password")
        hash_pass = get_password(session, user_login)
        if hash_pass:
            hash_pass = hash_pass[0][0]
            if check_password_hash(hash_pass, password):
                user_id = get_user_id(session, user_login)
                login_user(user_id, remember=True)
                if current_user.ipp:
                    return redirect("/ipp/list")
                return redirect("/")
    return redirect("/account/login")


@blueprint_login.route("/account/newbuyer", methods=['POST'])
def registernewbuyer():
    if request.method == 'POST':
        user_name = str(request.form.get("name"))
        login = str(request.form.get("login"))
        password = str(request.form.get("password"))
        repeat_password = str(request.form.get("repeat_password"))
        if password == repeat_password:
            password = generate_password_hash(password)
            add_user(session, user_name=user_name, login=login, password=password)
            return redirect("/")
    return redirect("/account/registeruser")


@blueprint_login.route("/account/newipp", methods=['POST'])
def registernewipp():
    if request.method == 'POST':
        user_name = request.form.get("name")
        login = request.form.get("login")
        password = request.form.get("password")
        repeat_password = request.form.get("repeat_password")
        ipp = request.form.get("ipp")
        if password == repeat_password:
            password = generate_password_hash(password)
            add_user(session, user_name=user_name, ipp=ipp, login=login, password=password, user_type="ipp")
            return redirect("/")
    return redirect("/account/registeripp")
