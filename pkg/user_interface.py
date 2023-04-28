from flask import render_template, request, redirect, Blueprint
from flask_login import current_user

from db.requests import *
from .data_init import user_required, product_query,  session


blueprint_user = Blueprint(
    'user_api',
    __name__,
    template_folder="./templates"
)


def update_basket(request):
    req = list(request.form.keys())[0].split('.')
    states = {'in': add_plus_product_to_basket, '-': add_minus_product_to_basket, '+': add_plus_product_to_basket}
    for i in ['in', '-', '+']:
        if i in req:
            states[i](session, current_user.id, req[2])


def get_cart():
    basket = get_user_basket(session, current_user.id)
    cart = {}
    for i in basket:
        cart[i[0]] = i[1]
    summa = 0
    for i in cart.keys():
        summa += get_product_by_id(session, i).price * cart[i]
    return cart, summa


@blueprint_user.route("/")
def main_page():
    product_types = get_category_type(session)
    products = get_top_products(session)
    return render_template("main.html", product_types=product_types, products=products)


@blueprint_user.route("/user/<global_type_id>")
@user_required
def user_global_type_page(global_type_id):
    global_type = get_category_type_by_id(session, global_type_id)
    product_types = get_category_by_category_type(session, global_type_id)
    return render_template("user_type.html", global_type=global_type, product_types=product_types)


@blueprint_user.route("/user/search", methods=['GET', 'POST'])
@user_required
def user_search():
    if request.method == 'POST':
        req = request.form['search_input']
        product = get_product_by_name(session, req)
        if product:
            return redirect(f'/user/1/1/{product.id}')
        else:
            return redirect('/')


@blueprint_user.route("/user/<global_type_id>/<type_id>", methods=['GET', 'POST'])
@user_required
def user_type_page(global_type_id, type_id):
    if request.method == 'POST':
        update_basket(request)

    price_from = request.args.get("from")
    price_to = request.args.get("to")
    ids, values = set(), []
    for i in list(request.args)[2:]:
        phr = i.split("_")
        ids.add(int(phr[0]))
        values.append(phr[1])

    global_type = get_category_type_by_id(session, global_type_id)
    type = get_category_by_id(session, type_id)

    products = product_query(session, type_id, ids, values, price_from, price_to)
    char = [get_products_characteristics(session, i.id) for i in products]
    filters = get_category_filters(session, type_id)
    return render_template("user_product_list.html", global_type=global_type, type=type,
                           products=products, char=char, filters=filters, cart=get_cart()[0])


@blueprint_user.route("/user/<global_type_id>/<type_id>/<prod_id>", methods=['GET', 'POST'])
@user_required
def user_product_page(global_type_id, type_id, prod_id):
    if request.method == 'POST':
        update_basket(request)
    global_type = get_category_type_by_id(session, global_type_id)
    type = get_category_by_id(session, type_id)
    product = get_product_by_id(session, prod_id)
    char = get_products_characteristics(session, product.id)
    return render_template("user_product.html", global_type=global_type, type=type, product=product,
                           char=char, cart=get_cart()[0])


@blueprint_user.route("/userbasket", methods=['GET', 'POST'])
@user_required
def user_basket_page():
    if request.method == 'POST':
        update_basket(request)
        req = list(request.form.keys())[0].split('.')
        if 'order' in req:
            add_basket_to_history(session, current_user.id)
            return render_template('order.html')
    basket = get_user_basket(session, current_user.id)
    products_history = get_user_history_basket(session, current_user.id)
    products = [get_product_by_id(session, i[0]) for i in basket]
    char = [get_products_characteristics(session, i.id) for i in products]
    return render_template("user_basket.html", products=products, basket=basket,
                           char=char, cart=get_cart()[0], summa=get_cart()[1], products_history=products_history)
