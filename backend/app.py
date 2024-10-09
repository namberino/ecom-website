from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import MySQLdb
import bcrypt
import os
import rsa
import base64


load_dotenv()
app = Flask(__name__)
CORS(app)
public_key, private_key = rsa.newkeys(1024)


# connect to mysql
db = MySQLdb.connect(
    host=os.getenv("MYSQL_HOST"),
    user=os.getenv("MYSQL_USER"),
    passwd=os.getenv("MYSQL_PASSWORD"),
    db=os.getenv("MYSQL_DB")
)


def encrypt_session_string(data):
    encrypted_data = rsa.encrypt(data.encode(), public_key)
    return base64.b64encode(encrypted_data).decode()


def decrypt_session_string(data):
    encrypted_data = base64.b64decode(data.encode())
    return rsa.decrypt(encrypted_data, private_key).decode()


# endpoint for login
@app.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    # get the password of email from db
    cursor = db.cursor()
    cursor.execute("select password, role from Users where email = %s", (email,))
    result = cursor.fetchone()

    # compare password with given password (with hashing)
    if result:
        hashed_password = result[0].encode('utf-8')
        
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            session_str = f"{email};{result[0]};{result[1]}"
            encrypted_session_str = encrypt_session_string(session_str)

            return jsonify({"status": "success", "message": "Login successful!", "session_string": encrypted_session_str})
        else:
            return jsonify({"status": "fail", "message": "Invalid credentials!"})
    else:
        return jsonify({"status": "fail", "message": "Invalid credentials!"})


# endpoint for registration
@app.route("/register", methods=["POST"])
def register():
    name = request.json["name"]
    email = request.json["email"]
    password = request.json["password"]

    cursor = db.cursor()

    # check if email already exists
    cursor.execute("select * from Users where email = %s", (email,))
    email_exists = cursor.fetchone()
    if email_exists:
        return jsonify({"status": "fail", "message": "Email already exists!"})

    # hash password
    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

    # insert data into db
    cursor.execute("insert into Users (name, email, password, role) values (%s, %s, %s, %s)", (name, email, hashed_password.decode('utf-8'), "user"))
    db.commit()
    return jsonify({"status": "success", "message": "Registration successful!"})


@app.route("/validate_session", methods=["POST"])
def validate_session():
    encrypted_session_str = request.json["session_string"]
    session_str = decrypt_session_string(encrypted_session_str).split(";")

    cursor = db.cursor()

    # check if session is valid
    cursor.execute("select * from Users where email = %s and password = %s and role = %s", (session_str[0], session_str[1], session_str[2]))
    valid_user = cursor.fetchone()
    if valid_user:
        return jsonify({"status": "success", "message": "Valid session string."})

    return jsonify({"status": "fail", "message": "Invalid session string."})


if __name__ == "__main__":
    app.run(debug=True)
