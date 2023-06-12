from db import MySQL, register, login, checkAccount
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS
# import MySQLdb.cursors
# import re

app = Flask(__name__)
CORS(app)

# Secret Key
app.config['SECRET_KEY'] = 'cobadulu'

# Intialize MySQL
mysql = MySQL(app)

@app.route('/', methods=['GET'])
def index():
    return "Logue App"

# App Registration
@app.route('/register', methods=['POST'])
def registerAccount():
    fullname = request.form['fullname']
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']
    try:
        return register(mysql, fullname, username, email, password)
    except Exception as e:
        err = jsonify(msg=f'{e}'), 500
        return err
    
# Acoount Check
@app.route('/account',methods=['GET'])
def accounts():
    try:
        user = checkAccount(mysql)
        return jsonify(user)
    except Exception as e:
        err = jsonify(msg=f'{e}'),500
        return err

# App Login
@app.route('/login', methods=['POST'])
def loginAccount():
    username = request.form['username']
    password = request.form['password']
    try:
        account = login(mysql, username, password)
        if account != "":
            return jsonify({"message": "Login Successful" , "user": account}),200
        return jsonify({"msg": "Wrong Email or Password"}), 401
    except Exception as e:
        err = jsonify(msg=f'{e}'),500
        return err

# App Logout
@app.route('/login/logout')
def logoutAccount():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

# App Home
@app.route('/login/home')
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


if __name__ == "__main__":
    app.run(debug=True)

#app.run(host='localhost', port=3306)