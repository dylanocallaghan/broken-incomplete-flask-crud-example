from flask import Flask, request, render_template, redirect, url_for, session, abort
from flask_mysqldb import MySQL
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
CORS(app)

# MySQL instance configurations
app.config['MYSQL_USER'] = 'crud'
app.config['MYSQL_PASSWORD'] = 'crud1234'
app.config['MYSQL_DB'] = 'flaskdb'
app.config['MYSQL_HOST'] = '34.123.115.164'
app.config['SECRET_KEY'] = 'your_secret_key'
mysql = MySQL(app)

# Routes

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO users(username, email, password) VALUES (%s, %s, %s)", (username, email, password))
        mysql.connection.commit()
        cur.close()

        return redirect(url_for('signin'))

    return render_template('signup.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = cur.fetchone()
        cur.close()

        if user and check_password_hash(user[3], password):
            session['username'] = user[1]
            return redirect(url_for('dashboard'))

        return 'Invalid credentials. Please try again.'

    return render_template('signin.html')

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('signin'))

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('signin'))

@app.route('/add')  # Add Student
def add():
    name = request.args.get('name')
    email = request.args.get('email')
    cur = mysql.connection.cursor()
    s = """INSERT INTO students(studentName, email) VALUES (%s, %s)"""
    cur.execute(s, (name, email))
    mysql.connection.commit()
    cur.close()
    return '{"Result":"Success"}'

@app.route("/")  # Default - Show Data
def read():
    return redirect(url_for('signin'))
# Custom error handler for 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return redirect(url_for('signin'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)
