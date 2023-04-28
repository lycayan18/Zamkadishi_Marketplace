from keys.config import load_config
from db.make_session import create_session
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
from flask import Flask, render_template, request, redirect

from db.requests import *


config = load_config()
session = create_session(config.db.engine)

login_manager = LoginManager()


@login_manager.user_loader
def load_user(user_id):
    return get_user(session, user_id)


def ipp_required(func):
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.ipp:
                return func(*args, **kwargs)
        return redirect("/")
    decorated_function.__name__ = func.__name__
    return decorated_function


def user_required(func):
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if not current_user.ipp:
                return func(*args, **kwargs)
        return redirect("/ipp/list")
    decorated_function.__name__ = func.__name__
    return decorated_function


def product_query(session, type_id, ids, values, price_from, price_to):
    if price_to and price_from:
        if price_from.isdigit() and price_to.isdigit():
            return get_products_by_filters(session, type_id, list(ids), values,
                                           price_from=int(price_from), price_to=int(price_to))
    return get_products_by_filters(session, type_id, list(ids), values)


def ipp_not_required(func):
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            if current_user.ipp:
                return redirect("/")
        return func(*args, **kwargs)

    return decorated_function
