from app import app
from flask import render_template, flash, redirect, request, session, url_for
from app.forms import LoginForm, RegistrationForm
from flaskext.mysql import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required

mysql = MySQL(autocommit=True)
mysql.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
@app.route('/index')
def index():
    session['loggedin'] = False
    user = {'username': ' '}
    if session['loggedin'] is True:
        user = {'username': session['username']}
    return render_template('index.html', title='Home', user=user)

@app.route('/test')
def test():
    if "account" in session:
        return f"User ID: {session['id']}, Username: {session['username']}, Status: {session['loggedin']}"

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        input_user = form.username.data
        input_pass = form.password.data
        cur = mysql.get_db().cursor()
        if cur.execute("SELECT * FROM userdatatb WHERE username = %s AND pass = %s", (input_user, input_pass)) is not None:
            cur.execute("SELECT * FROM userdatatb WHERE username = %s AND pass = %s", (input_user, input_pass))
            account = cur.fetchone()
            session['id'] = account[0]
            session['username'] = account[3]
            session['loggedin'] = True

            return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET'])
def logout():
    session.pop('id', None)
    session.pop('username', None)
    session['loggedin'] = False
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == "POST":
        firstName = form.firstName.data
        lastName = form.lastName.data
        username = form.username.data
        middlename = form.middleName.data
        password = form.password.data
        city = form.city.data
        province = form.province.data
        email = form.email.data
        cur = mysql.get_db().cursor()
        if firstName != '' and lastName != '' and username != '' and password != '' and city != '' and province != '' and email != '':
            cur.execute("INSERT INTO userdatatb(firstname, lastname, username, middlename, pass, city, province, email) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)", (firstName, lastName,username, middlename, password, city, province, email))
        cur.close()
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)

    