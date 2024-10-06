from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import MySQLdb
import bcrypt


app = Flask(__name__)
CORS(app)


# mysql configs
app.config["MYSQL_HOST"] = "localhost"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "Binhnam2402"
app.config["MYSQL_DB"] = "ecomdb"

# connect to mysql
db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="Binhnam2402",
    db="ecomdb"
)


# endpoint for login
@app.route("/login", methods=["POST"])
def login():
    email = request.json["email"]
    password = request.json["password"]

    # get the password of email from db
    cursor = db.cursor()
    cursor.execute("select password from Users where email = %s", (email,))
    result = cursor.fetchone()

    # compare password with given password (with hashing)
    if result:
        hashed_password = result[0].encode('utf-8')
        if bcrypt.checkpw(password.encode('utf-8'), hashed_password):
            return jsonify({"status": "success", "message": "Login successful!"})
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
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # insert data into db
    try:
        cursor.execute(
            "insert into Users (name, email, password) values (%s, %s, %s)", (name, email, hashed_password.decode('utf-8'))
        )
        db.commit()
        return jsonify({"status": "success", "message": "Registration successful!"})
    except MySQLdb.IntegrityError:
        return jsonify({"status": "fail", "message": "Email already exists!"})


if __name__ == "__main__":
    app.run(debug=True)
