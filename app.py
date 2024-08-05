from flask import Flask, request
from flask_mysqldb import MySQL
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app)

# MySQL instance configurations
app.config['MYSQL_USER'] = 'crud_user'
app.config['MYSQL_PASSWORD'] = 'QLPM6T5vSb23bbDw'
app.config['MYSQL_DB'] = 'flask-crud-db'
# Use Unix socket for Cloud SQL instance connection
app.config['MYSQL_HOST'] = '/cloudsql/your-project-id:europe-west2:flask-crud-instance'
mysql = MySQL(app)

@app.route("/add")  # Add Student
def add():
    name = request.args.get('name')
    email = request.args.get('email')
    cur = mysql.connection.cursor()  # create a connection to the SQL instance
    s = """INSERT INTO students(studentName, email) VALUES (%s, %s)"""
    cur.execute(s, (name, email))  # execute an SQL statement
    mysql.connection.commit()
    cur.close()
    return '{"Result":"Success"}'

@app.route("/")  # Default - Show Data
def read():
    cur = mysql.connection.cursor()  # create a connection to the SQL instance
    cur.execute('''SELECT * FROM students''')  # execute an SQL statement
    rv = cur.fetchall()  # retrieve all rows returned by the SQL statement
    Results = []
    for row in rv:  # format the output results and add to return string
        Result = {}
        Result['Name'] = row[1].replace('\n', ' ')
        Result['Email'] = row[2]
        Result['ID'] = row[0]
        Results.append(Result)
    cur.close()
    response = json.dumps(Results)
    return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080)  # run the Flask app at port 8080

