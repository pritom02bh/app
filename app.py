from flask import Flask, render_template, request, redirect, url_for,  session
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

# Student View

@app.route("/student_id.html", methods=["GET", "POST"])
def get_student_data():
    if request.method == "POST":
        student_number = request.form.get("student_number")
        cursor = db.cursor(dictionary=True)
        
        # Query to fetch student data
        student_query = "SELECT * FROM student WHERE student_number = %s"
        cursor.execute(student_query, (student_number,))
        student = cursor.fetchone()

        # Query to fetch grade report for the student
        grade_report_query = "SELECT grade FROM grade_report WHERE student_number = %s"
        cursor.execute(grade_report_query, (student_number,))
        grade_report = cursor.fetchall()

        cursor.close()

        if student:
            return render_template("student_data.html", student=student, grade_report=grade_report)
        else:
            return "Student not found"
    
    return render_template("student_id.html")


# End of Student View


# Grade View

@app.route("/grades.html", methods=["GET", "POST"])
def get_grade_view():
    if request.method == "POST":
        student_number = request.form.get("student_number")
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM grade_report WHERE student_number = %s"
        cursor.execute(query, (student_number,))
        student_g = cursor.fetchone()
        cursor.close()
        if student_g is not None:
            return render_template("grade_view.html", data=student_g)
        else:
            return "Student not found"
    return render_template("grades.html")


# End of Grade &  view

# Section Part

@app.route("/section_info_input.html", methods=["GET", "POST"])
def get_section_info():
    if request.method == "POST":
        section_identifier = request.form.get("section_identifier")
        cursor = db.cursor(dictionary=True)
        query = "SELECT * FROM section WHERE section_identifier = %s"
        cursor.execute(query, (section_identifier,))
        section_data = cursor.fetchone()
        cursor.close()
        if section_data is not None:
            return render_template("section_info.html", data=section_data)
        else:
            return "Section not found"
    return render_template("section_info_input.html")


# End of Section Part

# Prerequisite Part

@app.route("/prerequisite_info_input.html", methods=["GET", "POST"])
def get_prerequisite_info():
    if request.method == "POST":
        course_number = request.form.get("course_number")
        cursor = db.cursor(dictionary=True)
        query = "SELECT course_number, prerequisite_number FROM prerequisite WHERE course_number = %s"
        cursor.execute(query, (course_number,))
        prerequisite_data = cursor.fetchall()
        cursor.close()
        if prerequisite_data:
            return render_template("prerequisite_info.html", data = prerequisite_data)
        else:
            return "No prerequisites found for the given course number"
    return render_template("prerequisite_info_input.html")

# End of Prerequisite

# course Part


@app.route("/course_input.html", methods=["GET", "POST"])
def get_course_info():
    if request.method == "POST":
        course_number = request.form.get("course_number")
        cursor = db.cursor(dictionary=True)
        
        # Query to fetch course data from course table
        course_query = "SELECT * FROM course WHERE course_number = %s"
        cursor.execute(course_query, (course_number,))
        course = cursor.fetchone()
        
         # Query to fetch prerequisite course numbers for the course from prerequisite table
        prerequisite_query = "SELECT prerequisite_number FROM prerequisite WHERE course_number = %s"
        cursor.execute(prerequisite_query, (course_number,))
        prerequisites = cursor.fetchall()
        
        cursor.close()
        
        if course:
            return render_template("course_info.html", course=course, prerequisites=prerequisites)
        else:
            return "Course not found"
    return render_template("course_input.html")


# End of course

# Instructor View
@app.route('/instructor_id.html', methods=['GET', 'POST'])
def instructor_id():
    if request.method == 'POST':
        instructor_number = request.form['instructor_number']
        cursor = db.cursor()
        cursor.execute("SELECT * FROM student WHERE instructor_number = %s", (instructor_number,))
        result = cursor.fetchall()
        cursor.close()

        if result:
            return render_template('instructor_data.html', data=result)
        else:
            return "Instructor not found."
    return render_template('instructor_id.html')

# End of Instructor View

if __name__ == '__main__':
    app.run()
