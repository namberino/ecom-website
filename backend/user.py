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

    cursor.execute("select * from Users where email = %s", (email,))
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
