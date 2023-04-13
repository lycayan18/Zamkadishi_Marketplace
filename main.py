import flask
from flask import Flask, render_template, request, redirect
from flask_login import login_user, LoginManager, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from keys.config import load_config
from db.make_session import create_session
from db.requests import *
from db.models import Users

app = Flask(__name__)
config = load_config()
user_id = 6

app.config["SECRET_KEY"] = config.flask.secret_key

session = create_session(config.db.engine)
login_manager = LoginManager(app)


# login block


@login_manager.user_loader
def load_user(user_id):
    return get_user(session, user_id)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect("/")


@app.route("/account/login")
def login():
    return render_template("login.html")


@app.route("/account/registeruser")
def registeruser():
    return render_template("register_user.html")


@app.route("/account/registeripp")
def registeripp():
    return render_template("register_ipp.html")


@app.route("/account/loginaccount", methods=['POST'])
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
                return redirect("/")
    return redirect("/account/login")


@app.route("/account/newbuyer", methods=['POST'])
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


@app.route("/account/newipp", methods=['POST'])
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


# main block


# product_types - левое меню
# передаешь список типов товара с атрибутами: photo, global_type

# products - правое меню меню
# передаешь список продуктов с атрибутами: photo, cost, name

# названия атрибутов поменяю если что

@app.route("/")
def main_page():
    product_types = get_category_type(session)
    products = get_top_products(session)
    return render_template("main.html", product_types=product_types, products=products)


@app.route("/products")
@login_required
def product_page():
    product_types = get_category_type(session)
    products = get_top_products(session)
    return render_template("main.html", product_types=product_types, products=products)


# ipp block

@app.route("/ipp/list")
def ipp_page():
    product_types = get_category_type(session)
    return render_template("ipp_global_type.html", product_types=product_types)


@app.route("/ipp/list/<global_type_id>")
def ipp_global_type_page(global_type_id):
    global_type = get_category_type_by_id(session, global_type_id)
    product_types = get_category_by_category_type(session, global_type_id)
    return render_template("ipp_type.html", global_type=global_type, product_types=product_types)


@app.route("/ipp/list/<global_type_id>/<type_id>")
def ipp_type_page(global_type_id, type_id):
    global_type = get_category_type_by_id(session, global_type_id)
    type = get_category_by_id(session, type_id)
    characteristics = get_characteristics(session, type_id)
    return render_template("ipp_create.html", global_type=global_type, type=type, characteristics=characteristics)


# user block


@app.route("/user/<global_type_id>")
def user_global_type_page(global_type_id):
    global_type = get_category_type_by_id(session, global_type_id)
    product_types = get_category_by_category_type(session, global_type_id)
    return render_template("user_type.html", global_type=global_type, product_types=product_types)


@app.route("/user/<global_type_id>/<type_id>", methods=['GET', 'POST'])
def user_type_page(global_type_id, type_id):
    if request.method == 'POST':
        req = list(request.form.keys())[0].split('.')
        if 'in' in req:
            add_plus_product_to_basket(session, user_id, req[2])
        if '-' in req:
            add_minus_product_to_basket(session, user_id, req[2])
        if '+' in req:
            add_plus_product_to_basket(session, user_id, req[2])
    global_type = get_category_type_by_id(session, global_type_id)
    type = get_category_by_id(session, type_id)
    products = get_products_by_category(session, type_id)
    char = [get_products_characteristics(session, i.id) for i in products]
    filters = get_category_filters(session, type_id)
    basket = get_user_basket(session, user_id)
    cart = {}
    for i in basket:
        cart[i[0]] = i[1]
    return render_template("user_product_list.html", global_type=global_type, type=type,
                           products=products, char=char, filters=filters, cart=cart)


@app.route("/user/<global_type_id>/<type_id>/<prod_id>", methods=['GET', 'POST'])
def user_product_page(global_type_id, type_id, prod_id):
    if request.method == 'POST':
        req = list(request.form.keys())[0].split('.')
        if 'in' in req:
            add_plus_product_to_basket(session, user_id, req[2])
        if '-' in req:
            add_minus_product_to_basket(session, user_id, req[2])
        if '+' in req:
            add_plus_product_to_basket(session, user_id, req[2])
    global_type = get_category_type_by_id(session, global_type_id)
    type = get_category_by_id(session, type_id)
    product = get_product_by_id(session, prod_id)
    char = get_products_characteristics(session, product.id)
    basket = get_user_basket(session, user_id)
    cart = {}
    for i in basket:
        cart[i[0]] = i[1]
    return render_template("user_product.html", global_type=global_type, type=type, product=product,
                           char=char, cart=cart)


@app.route("/userbasket", methods=['GET', 'POST'])
def user_basket_page():
    if request.method == 'POST':
        req = list(request.form.keys())[0].split('.')
        if 'in' in req:
            add_plus_product_to_basket(session, user_id, req[2])
        if '-' in req:
            add_minus_product_to_basket(session, user_id, req[2])
        if '+' in req:
            add_plus_product_to_basket(session, user_id, req[2])
    basket = get_user_basket(session, user_id)
    cart = {}
    for i in basket:
        cart[i[0]] = i[1]
    products = [get_product_by_id(session, i[0]) for i in basket]
    char = [get_products_characteristics(session, i.id) for i in products]
    summa = 0
    for i in cart.keys():
        summa += get_product_by_id(session, i).price * cart[i]
    print(char)
    return render_template("user_basket.html", products=products, basket=basket, char=char, cart=cart, summa=summa)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
