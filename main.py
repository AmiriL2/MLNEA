from flask import Flask, render_template, request
import pymysql
import pymysql.cursors

app = Flask(__name__)

connect = pymysql.connect(
    host='10.100.33.60',
    user='alayne',
    password='228043303',
    database= 'alayne_socialmedia',
    cursorclass=pymysql.cursors.DictCursor
)

@app.route('/')
def index():
    return render_template("home.html.jinja")

@app.route('/registration', methods=['GET', 'POST'])
def registration():
    if request.method == 'POST':
        fname = request.form['first_name']
        username = request.form['username']
        phonenumber = request.form['phonenumber']
        email = request.form['email']
        password = request.form['password']


        Cursor = connect.cursor()
        Cursor.execute(f"INSERT INTO `Users` (`First_Name`, `email`, `phone`, `password`, `username`) VALUES ('{fname}','{email}','{phonenumber}','{password}','{username}')")
        Cursor.close()
        connect.commit()

    return render_template("sign-up.html.jinja")

@app.route('/homepage')
def homepage():
    return render_template("homepage.html.jinja")