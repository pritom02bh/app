from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector
from flask_mysqldb import MySQL
from passlib.hash import sha256_crypt

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

# Student View

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
            return render_template("student_data.html", student = student)
        else:
            return "Student not found"
    return render_template("student_id.html")

# End of Student View


# Instructor View
@app.route('/instructor_id.html', methods=['GET', 'POST'])
def instructor_id():
    if request.method == 'POST':
        instructor_number = request.form['instructor_number']

        # Check if instructor exists in the database
        cursor = db.cursor()
        cursor.execute("SELECT * FROM student WHERE instructor_number = %s", (instructor_number,))
        result = cursor.fetchall()
        cursor.close()

        if result:
            return render_template('instructor_data.html', data=result)
        else:
            return "Instructor not found."
    return render_template('instructor_id.html')

if __name__ == '__main__':
    app.run()
