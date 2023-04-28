from flask import render_template, request, Blueprint
from flask_login import current_user

from db.requests import *
from .data_init import ipp_required, session

from werkzeug.utils import secure_filename
from os.path import join


blueprint_ipp = Blueprint(
    'ipp_api',
    __name__,
    template_folder="./templates"
)


@blueprint_ipp.route("/ipp/list")
@ipp_required
def ipp_page():
    product_types = get_category_type(session)
    return render_template("ipp_global_type.html", product_types=product_types)


@blueprint_ipp.route("/ipp/list/<global_type_id>")
@ipp_required
def ipp_global_type_page(global_type_id):
    global_type = get_category_type_by_id(session, global_type_id)
    product_types = get_category_by_category_type(session, global_type_id)
    return render_template("ipp_type.html", global_type=global_type, product_types=product_types)


@blueprint_ipp.route("/ipp/list/<global_type_id>/<type_id>", methods=['GET', 'POST'])
@ipp_required
def ipp_type_page(global_type_id, type_id):
    if request.method == "POST":
        manufactur = request.form.get('manufacturer')
        price = request.form.get('price')
        file = request.files["photo"]
        filename = secure_filename(file.filename)
        file.save(join('./static/img/', filename))

        add_product(session, manufactur, type_id, int(price), filename, current_user.ipp, request.form)

    global_type = get_category_type_by_id(session, global_type_id)
    type = get_category_by_id(session, type_id)
    characteristics = get_characteristics(session, type_id)
    return render_template("ipp_create.html", global_type=global_type, type=type, characteristics=characteristics)
