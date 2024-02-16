from flask import Flask, render_template, request, redirect, g
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
        self.id = ID
        self.email = email
        self.profilepic = profilepic

    def get_id(self):
        return str(self.ID)

def connect_db():
    return pymysql.connect(
        host='10.100.33.60',
        user='alayne',
        password='228043303',
        database= 'alayne_socialmedia',
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=True
    )

def get_db():    
        if not hasattr(g, 'db'):
            g.db = connect_db()
        return g.db    

@app.teardown_appcontext
def close_db(error):
        if hasattr(g, 'db'):
            g.db.close() 

@login_manager.user_loader
def load_user(user_id):
    Cursor = get_db().cursor()
    Cursor.execute(f"SELECT * FROM `Users` WHERE `ID` = " + str(user_id))
    result = Cursor.fetchone()
    Cursor.close()
    get_db().commit()

    if result is None:
        return None
    return User(result["ID"], result["username"], result["email"], result["profilepic"])

@app.route('/')
def index():
    if flask_login.current_user.is_authenticated:
        return redirect('/feedpage')
    return render_template("home.html.jinja")

@app.route('/feedpage', methods=['GET', 'POST'])
@flask_login.login_required
def homepage():
    cursor = get_db().cursor()
    sql = "SELECT * FROM `Posts` JOIN `Users` ON Posts.User_ID = `Users`.ID ORDER BY `Timestamp` "
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

        Cursor = get_db().cursor()
        Cursor.execute(f"INSERT INTO `Users` (`First_Name`, `email`, `phone`, `password`, `username`) VALUES ('{fname}','{email}','{phonenumber}','{password}','{username}')")
        Cursor.close()
        get_db().commit()
        return redirect('/login')
    
    if flask_login.current_user.is_authenticated:
        return redirect('/feedpage')
    return render_template('sign_up_page.html.jinja')

@app.route('/login', methods=['GET', 'POST'])
def login():
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            Cursor = get_db().cursor()
            Cursor.execute(f"SELECT * FROM `Users` WHERE username='{username}'")
            result = Cursor.fetchone()
            
            if result['password'] == password:
                user = load_user(result['ID'])
                flask_login.login_user(user)
                return redirect('/feedpage')
            
        if flask_login.current_user.is_authenticated:
            return redirect('/feedpage')

        return render_template("sign-in-page.html.jinja")

@app.route('/post', methods=['POST', 'GET'])
@flask_login.login_required
def user_post():
    description = request.form['Description']
    Image = request.form['Image']
    User_ID = flask_login.current_user.id
    Cursor = get_db().cursor()
    Cursor.execute("INSERT INTO `Posts` (`User_ID`, `Description`, `Image`, `Timestamp`) VALUES (%s, %s,  %s, NOW())", (User_ID, description, Image))
    Cursor.close()
    get_db().commit()
    return redirect('/feedpage')

@app.route('/profile')
def profile():
    return render_template("profile.html.jinja")