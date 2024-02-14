from flask import Flask, render_template, request, redirect
import flask_login
import pymysql
import pymysql.cursors


app = Flask(__name__)

app.secret_key = "632^9723))&@%$*BCT*#G@(DB211"

login_manager = flask_login.LoginManager()

login_manager.init_app(app)


class User:
    is_authenticated = True
    is_anonymous = False
    is_active = True

    def __init__(self, ID, username, email, profilepic):
        self.username = username
        self.ID = ID
        self.email = email
        self.profilepic = profilepic

    def get_id(self):
        return str(self.ID)

    
connect = pymysql.connect(
    host='10.100.33.60',
    user='alayne',
    password='228043303',
    database= 'alayne_socialmedia',
    cursorclass=pymysql.cursors.DictCursor
)

@login_manager.user_loader
def load_user(user_id):
    Cursor = connect.cursor()
    Cursor.execute(f"SELECT * FROM `Users` WHERE `ID` = " + str(user_id))
    result = Cursor.fetchone()
    Cursor.close()
    connect.commit()

    if result is None:
        return None
    return User(result["ID"], result["username"], result["email"], result["profilepic"])

@app.route('/')
def index():
    if flask_login.current_user.is_authenticated:
        return redirect('/feedpage')
    return render_template("home.html.jinja")

@app.route('/feedpage')
@flask_login.login_required
def homepage():
    cursor = connect.cursor()
    sql = "SELECT * FROM `Posts` JOIN `Users` on Posts.User_ID = User_ID ORDER BY `Timestamp` "
    cursor.execute(sql)
    posts = cursor.fetchall()
    cursor.close()

    return render_template('/homepage.html.jinja', Posts=posts)

@app.route('/sign-up', methods=['GET','POST'])
def signup():

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
        return redirect('/login')
    
    if flask_login.current_user.is_authenticated:
        return redirect('/feedpage')
    return render_template('sign_up_page.html.jinja')

@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            Cursor = connect.cursor()
            Cursor.execute(f"SELECT * FROM `Users` WHERE username='{username}'")
            result = Cursor.fetchone()
            
            if result['password'] == password:
                user = load_user(result['ID'])
                flask_login.login_user(user)
                return redirect('/feedpage')
            
        if flask_login.current_user.is_authenticated:
            return redirect('/feedpage')

        return render_template("sign-in-page.html.jinja")