from flask import Flask, render_template, request, redirect
from flask_login import login_user, LoginManager, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

from keys.config import load_config
from db.make_session import create_session
from db.requests import get_user_id, add_user, get_password, get_user
from db.models import Users

app = Flask(__name__)
config = load_config()

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
    return render_template("main.html", product_types=[], products=[])


@app.route("/products")
@login_required
def product_page():
    return render_template("main.html", product_types=[], products=[])


# ipp block

@app.route("/ipp/list")
def ipp_page():
    return render_template("ipp_global_type.html", product_types=[])


# global_type и type подставятся автоматом. Не трогай


@app.route("/ipp/list/<global_type>")
def ipp_global_type_page(global_type=''):
    return render_template("ipp_type.html", global_type=global_type.upper(), product_types=[])


@app.route("/ipp/list/<global_type>/<type>")
def ipp_type_page(global_type='', type=''):
    return render_template("ipp_create.html", global_type=global_type.upper(), type=type.upper())


# user block


@app.route("/user/<global_type>")
def user_global_type_page(global_type=''):
    return render_template("user_type.html", global_type=global_type.upper(), product_types=[])


@app.route("/user/<global_type>/<type>")
def user_type_page(global_type='', type=''):
    # вместо in_cart нужно добавлять в карзину (атрибут .in_cart)
    if request.method == 'POST':
        print(request.form)
        if request.form.get('В корзину') == 'В корзину':
            in_cart = 1
        if request.form.get('-') == '-' and in_cart != 0:
            in_cart -= 1
        if request.form.get('+') == '+':
            in_cart += 1
    return render_template("user_product_list.html", global_type=global_type.upper(), products=[], filters=Product().filter, type=type)


@app.route("/user/<global_type>/<type>/<prod>", methods=['GET', 'POST'])
def user_product_page(global_type, type, prod):
    # вместо in_cart нужно добавлять в карзину (атрибут .in_cart)
    if request.method == 'POST':
        print(request.form)
        if request.form.get('В корзину') == 'В корзину':
            in_cart = 1
        if request.form.get('-') == '-' and in_cart != 0:
            in_cart -= 1
        if request.form.get('+') == '+':
            in_cart += 1
    return render_template("user_product.html", product=None)


@app.route("/userbasket")
def user_basket_page():
    return render_template("user_basket.html", products=[], summa=0)


if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080)
