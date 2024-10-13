from __main__ import app, db
from flask import request, jsonify


@app.route("/get_products", methods=["GET"])
def get_products():
    cursor = db.cursor()

    cursor.execute("select * from Products")
    products = cursor.fetchall()

    # store result in a list of dictionaries
    product_list = []
    for product in products:
        product_dict = {
            "id": product[0],
            "name": product[1],
            "price": product[2],
            "amount": product[3],
            "description": product[4]
        }
        product_list.append(product_dict)

    return jsonify({"status": "success", "products": product_list})


@app.route("/get_product", methods=["GET"])
def get_product():
    return None


@app.route("/create_product", methods=["PUT"])
def create_product():
    return None


@app.route("/edit_product", methods=["POST"])
def edit_product():
    return None


@app.route("/delete_product", methods=["DELETE"])
def delete_product():
    product_id = request.args.get("id")

    cursor = db.cursor()

    # check if product exists
    cursor.execute("select * from Products where id = %s", (product_id,))
    product = cursor.fetchone()

    if product:
        cursor.execute("delete from Products where id = %s", (product_id,))
        db.commit()

        return jsonify({"status": "success", "message": "Product deleted successfully!"})
    else:
        return jsonify({"status": "fail", "message": "Product not found!"})

