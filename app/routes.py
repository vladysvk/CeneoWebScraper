import os
import json
import pandas as pd
from app import app
from app.forms import ProductIdForm
from app.models import Product
from flask import render_template, redirect, request, url_for, send_file, after_this_request
from app.utils import create_if_not_exists


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/extract")
def display_form():
    form = ProductIdForm()
    return render_template("extract.html", form=form)

@app.route("/extract", methods=['POST'])
def extract():
    form = ProductIdForm(request.form)
    if form.validate():
        product_id = form.product_id.data
        product = Product(product_id)
        product.extract_name()
        product.extract_opinions()
        product.calculate_stats()
        product.generate_charts()
        print(product)
        product.save_opinions()
        product.save_info()
        return redirect(url_for('product', product_id=product_id))
    else:
         return render_template("extract.html", form=form)


@app.route("/product/<product_id>")
def product(product_id):
    return render_template("product.html", product_id=product_id)

@app.route("/charts/<product_id>")
def charts(product_id):
    return render_template("charts.html", product_id=product_id)

@app.route("/products")
def products():
    product_list = []
    products_dir = os.path.join("app", "data", "products")
    if not os.path.exists(products_dir):
        return "Products directory not found", 404
    for fn in os.listdir(products_dir):
        fn = fn.split(".")[0]
        product = Product(product_id=fn)
        product.read_info()
        product_list.append(product)
    return render_template("products.html", products=product_list)

@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/products/download/<product_id>/<format>")
def download(product_id, format):
    path = os.path.join("app", "data", "opinions", f"{product_id}.json")
    if not os.path.exists(path):
       return "Product not found", 404
    
    with open(path, "r", encoding="utf-8") as jf: 
        opinions = json.load(jf)

    df = pd.DataFrame(opinions)

    filename = f"{product_id}_opinions.{format}"
    fpath = os.path.join("app\\temp", filename)
    create_if_not_exists("app\\temp")





    if format == "csv":
        df.to_csv(fpath, index=False)
    elif format == "xlsx":
        df.to_excel(fpath, index=False)
    elif format == "json":
        df.to_json(fpath, orient="records", indent=2)
    else:
        return "Unsupported format", 400
    """
    @after_this_request
    def remove_f(response):
        try:
            os.remove(f"temp\\{filename}")
        except Exception:
            print("File not deleted")
        
        return response
    """
    return send_file(f"temp\\{filename}", as_attachment=True)
