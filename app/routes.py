from app import app
from flask import render_template, flash, redirect, request, session, url_for
from app.forms import LoginForm, RegistrationForm
from flaskext.mysql import MySQL

mysql = MySQL(autocommit=True)
mysql.init_app(app)

"""
#Profile Pages
def get_user(userid):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM userdata where userid = ?", (userid))
    user = cur.fetchone()

    if user is None:
        abort(404)
    return user

#Event Pages
def get_event(eventid):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM Recruitment where eventid = ?", (eventid))
    event = cur.fetchone()

    if event is None:
        abort(404)
    return event


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route('/')
@app.route('/index')
def index():
    if session['loggedin'] is True:
        user = {'username': session['username']}
        if cur.execute("SELECT * FROM recruitments") is None:
            # Placeholder for text that says, No Recruitments Ongoing. Start one now!
            pass

        cur = mysql.get_db().cursor()
        cur.execute("SELECT * FROM Recruitments")
        events = cur.fetchall()
        return render_template('index.html', event=events)

    session['loggedin'] = False
    user = {'username': ' '}
    return render_template('index.html', title='Home', user=user)

#Profile Pages 2
@app.route('/profile/<int:userid>')
def profile(userid):
    user = get_user(userid)
    return render_template('profile.html', user=user)

#Event Pages 2
@app.route('/event/<int:eventid>')
def events(eventid):
    event = get_event(eventid)
    form = VolunteerForm()


    return render_template('event.html', event=event,form=form)

"""
@app.route('/')
@app.route('/index')
def index():
    user = {'username': ' '}
    if session['loggedin'] is True:
        user = {'username': session['username']}
    session['loggedin'] = False
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
            cur.execute("INSERT INTO userdata(firstname, lastname, username, middlename, pass, city, province, email) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)", (firstName, lastName,username, middlename, password, city, province, email))
        cur.close()
        return redirect(url_for('login'))
    return render_template('registration.html', title='Register', form=form)

