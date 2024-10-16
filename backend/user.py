from __main__ import app, db, decrypt_session_string
from flask import request, jsonify


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
