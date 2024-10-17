from __main__ import app, db
from flask import request, jsonify
import bcrypt


@app.route("/get_accounts", methods=["GET"])
def get_accounts():
    cursor = db.cursor()

    cursor.execute("select * from Users")
    accounts = cursor.fetchall()

    account_list = []
    for account in accounts:
        account_dict = {
            "id": account[0],
            "name": account[1],
            "email": account[2],
            "password": "*****",
            "role": account[4]
        }
        account_list.append(account_dict)

    return jsonify({"status": "success", "accounts": account_list})


@app.route("/get_account", methods=["GET"])
def get_account():
    account_id = request.args.get("id")

    cursor = db.cursor()

    cursor.execute("select * from Users where id = %s", (account_id,))
    account = cursor.fetchone()

    if account:
        account_dict = {
            "name": account[1],
            "email": account[2],
            "role": account[4]
        }
        return jsonify({"status": "success", "message": "Account found!", "account": account_dict})
    else:
        return jsonify({"status": "fail", "message": "Account not found!"})


@app.route("/create_account", methods=["POST"])
def create_account():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    if not name or not email or not password:
        return jsonify({"status": "fail", "message": "All fields must not be empty!"})

    cursor = db.cursor()

    cursor.execute("select * from Users where email = %s", (email,))
    existing_account = cursor.fetchone()
    if existing_account:
        return jsonify({"status": "fail", "message": "Account already exists!"})

    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    cursor.execute("insert into Users (name, email, password, role) values (%s, %s, %s, %s)", (name, email, hashed_password.decode(), "user"))
    db.commit()
    return jsonify({"status": "success", "message": "Account created successfully!"})


@app.route("/edit_account", methods=["POST"])
def edit_account():
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
        if password == "":
            cursor.execute("update Users set name = %s, email = %s where id = %s", (name, email, account_id))
            db.commit()
        else:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            cursor.execute("update Users set name = %s, email = %s, password = %s where id = %s", (name, email, hashed_password.decode(), account_id))
            db.commit()

        return jsonify({"status": "success", "message": "Account updated successfully!"})


@app.route("/delete_account", methods=["DELETE"])
def delete_account():
    account_id = request.args.get("id")

    cursor = db.cursor()

    cursor.execute("select * from Users where id = %s", (account_id,))
    account = cursor.fetchone()

    if account:
        cursor.execute("delete from Users where id = %s", (account_id,))
        db.commit()
        return jsonify({"status": "success", "message": "Account deleted successfully!"})
    else:
        return jsonify({"status": "fail", "message": "Account not found!"})
