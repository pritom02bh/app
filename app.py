from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from flask_mysqldb import MySQL

app = Flask(__name__)

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="5607",
    database="register_db"
)
cursor = db.cursor()

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route("/student_id.html", methods=["GET", "POST"])
def get_student_data():
    if request.method == "POST":
        student_number = request.form.get("student_number")
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM student WHERE student_number = %s"
        cursor.execute(query, (student_number,))
        student = cursor.fetchone()
        cursor.close()
        if student_number:
            return render_template("student_data.html", student_data=get_student_data)
        else:
            return "Student not found"
    return render_template("student_id.html")




if __name__ == '__main__':
    app.run()
