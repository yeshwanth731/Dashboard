from flask import Flask, redirect, url_for, render_template
import pyodbc



app = Flask(__name__)

conn_str = (
    r'DRIVER={ODBC Driver 17 for SQL Server};'
    r'SERVER=LAPTOP-Q5L4HKVP\SQLEXPRESS;'
    r'DATABASE=Test_db;'
    r'Trusted_Connection=yes;'

)

@app.route("/")
def home():
    return render_template("base.html")

@app.route("/all/runtime")
def All_runtime():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Runtime")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    conn.close
    return render_template("AllRuntime.html", users=rows, columns=columns)

@app.route("/milestone")
def Milestone():
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM  Runtime")
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    conn.close
    return render_template("milestone.html", users=rows, columns=columns)


if __name__ == "__main__":
    app.run(debug=True)
