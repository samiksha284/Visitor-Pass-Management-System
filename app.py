from flask import Flask, render_template, request, redirect, url_for, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

# Connect to MySQL
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="yourpassword",
        database="visitor_management"
    )

# Home Route
@app.route('/')
def home():
    return render_template('index.html')

# Visitor Registration Route
@app.route('/register_visitor', methods=['GET', 'POST'])
def register_visitor():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        gate = request.form['gate']
        pre_registered = 'pre_registered' in request.form

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("INSERT INTO visitors (first_name, last_name, email, gate, pre_registered, status) VALUES (%s, %s, %s, %s, %s, %s)",
                       (first_name, last_name, email, gate, pre_registered, 'Registered'))

        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('dashboard'))

    return render_template('register_visitor.html')

# Dashboard Route
@app.route('/dashboard')
def dashboard():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM visitors")
    visitors = cursor.fetchall()

    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template('dashboard.html', visitors=visitors, employees=employees)

if __name__ == '__main__':
    app.run(debug=True)
