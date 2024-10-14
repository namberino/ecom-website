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


@app.route("/create_product", methods=["POST"])
def create_product():
    name = request.json["name"]
    price = request.json["price"]
    amount = request.json["amount"]
    description = request.json["description"]

    if not name or not price or not amount or not description:
        return jsonify({"status": "fail", "message": "All fields must not be empty!"})

    try:
        float(price)
        int(amount)
    except:
        return jsonify({"status": "fail", "message": "Invalid data type for price and amount"})

    cursor = db.cursor()

    cursor.execute("select * from Products where name = %s", (name,))
    product = cursor.fetchone()
    if product:
        return jsonify({"status": "fail", "message": "Product already exists!"})

    cursor.execute("insert into Products (name, price, amount, description) values (%s, %s, %s, %s)", (name, price, amount, description))
    db.commit()
    return jsonify({"status": "success", "message": "Product created successfully!"})


@app.route("/edit_product", methods=["POST"])
def edit_product():
    prod_id = request.json["id"]
    name = request.json["name"]
    price = request.json["price"]
    amount = request.json["amount"]
    description = request.json["description"]

    if not prod_id or not name or not price or not amount or not description:
        return jsonify({"status": "fail", "message": "All fields must not be empty!"})

    try:
        float(price)
        int(amount)
    except:
        return jsonify({"status": "fail", "message": "Invalid data type for price and amount"})

    cursor = db.cursor()
    cursor.execute("update Products set name = %s, price = %s, amount = %s, description = %s where id = %s", (name, price, amount, description, prod_id))
    db.commit()
    return jsonify({"status": "success", "message": "Product updated successfully!"})


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

