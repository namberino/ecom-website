from __main__ import app, db
from flask import request, jsonify


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


@app.route("/create_account", methods=["POST"])
def create_account():
    return None


@app.route("/edit_account", methods=["POST"])
def edit_account():
    return None


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
