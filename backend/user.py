from __main__ import app, db, encrypt_session_string, decrypt_session_string
from flask import request, jsonify
import bcrypt


@app.route("/get_info_from_session", methods=["POST"])
def get_info_from_session():
    encrypted_session_str = request.json["session_string"]
    session_str = decrypt_session_string(encrypted_session_str).split(";")

    cursor = db.cursor()

    cursor.execute("select id, name from Users where email = %s", (session_str[0],))
    account = cursor.fetchone()

    account_dict = {
        "id": account[0],
        "name": account[1],
        "email": session_str[0]
    }
    return jsonify({"status": "success", "message": "Got account information!", "account": account_dict})


@app.route("/user_edit_info", methods=["POST"])
def user_edit_info():
    account_id = request.json["id"]
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    if not name or not email:
        return jsonify({"status": "fail", "message": "Name and email must not be empty!"})

    cursor = db.cursor()

    cursor.execute("select * from Users where email = %s and not email = (select email from Users where id = %s)", (email, account_id))
    existing_account = cursor.fetchone()

    if existing_account:
        return jsonify({"status": "fail", "message": "Email is already associated with another account."})
    else:
        hashed_password = ""

        if password == "":
            cursor.execute("update Users set name = %s, email = %s where id = %s", (name, email, account_id))
            db.commit()

            cursor.execute("select password from Users where id = %s", (account_id,))
            password = cursor.fetchone()[0]
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        else:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            cursor.execute("update Users set name = %s, email = %s, password = %s where id = %s", (name, email, hashed_password.decode(), account_id))
            db.commit()

        session_str = f"{email};{hashed_password.decode()};user"
        encrypted_session_str = encrypt_session_string(session_str)

        return jsonify({"status": "success", "message": "Account updated successfully!", "session_string": encrypted_session_str})


@app.route("/add_to_cart", methods=["POST"])
def add_to_cart():
    product_id = request.json["product_id"]
    account_id = request.json["user_id"]
    amount = request.json["amount"]

    cursor = db.cursor()

    cursor.execute("select id, amount from Cart where user_id = %s and product_id = %s", (account_id, product_id))
    cart_item = cursor.fetchone()
    
    if cart_item:
        # update the amount of the existing product in the cart
        new_amount = cart_item[1] + amount
        cursor.execute("update Cart set amount = %s where id = %s", (new_amount, cart_item[0]))
    else:
        # insert a new product into the cart
        cursor.execute("insert into Cart (user_id, product_id, amount) values (%s, %s, %s)", (account_id, product_id, amount))

    db.commit()

    return jsonify({"status": "success", "message": "Product added to cart successfully!"})
