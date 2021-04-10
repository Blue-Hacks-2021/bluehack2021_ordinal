from app import app
from flask import render_template, flash, redirect, request, session, url_for
from app.forms import LoginForm, RegistrationForm, VolunteerForm
from flaskext.mysql import MySQL

mysql = MySQL(autocommit=True)
mysql.init_app(app)

#
#@login_manager.user_loader
#def load_user(user_id):
#   return User.get(user_id)


#Profile Pages
def get_user(user_id):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM userdata where userid = %s", (user_id))
    user = cur.fetchone()

    if user is None:
        abort(404)
    return user

#Event Pages
def get_event(event_id):
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM Recruitment where eventid = %s ", event_id )
    event = cur.fetchone()

    if event is None:
        abort(404)
    return event

@app.route('/')
@app.route('/index')
def index():
    user = {'username': ' '}
    if session['loggedin'] is True:
        user = {'username': session['username']}
        cur = mysql.get_db().cursor()
        #if cur.execute("SELECT * FROM recruitment") is None:
            # Placeholder for text that says, No Recruitments Ongoing. Start one now!
            
        cur.execute("SELECT * FROM Recruitment")
        events = cur.fetchall()
        return render_template('index.html', user=user, events=events)

    session['loggedin'] = False
    user = {'username': ' '}
    return render_template('index.html', title='Home', user=user)



#Profile Pages 2
@app.route('/profile/<int:user_id>')
def profile(user_id):

    user = get_user(user_id)
    cur = mysql.get_db().cursor()
    #if cur.execute("SELECT * FROM recruitment") is None:
        # Placeholder for text that says, No Recruitments Ongoing. Start one now!
            

    cur.execute("SELECT * FROM Recruitment where userid = {0} ".format(user[0]))
    events = cur.fetchall()
    
    cur.execute("SELECT count(*) FROM Recruitment where userid = {0} ".format(user[0]))
    eventcount = cur.fetchone();
    return render_template('profile.html', user=user, events=events, eventcount=eventcount[0])

#Event Pages 2
@app.route('/event/<int:event_id>')
def event(event_id):
    event = get_event(event_id)
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM userdata where userid = {0}".format(event[1]))
    user = cur.fetchone()
    form = VolunteerForm()
    if form.validate_on_submit():
        cur = mysql.get_db().cursor()
        cur.execute("Insert INTO Volunteers values ({0},{1} ".format(user[0],event[0]))
        cur.execute("Update Recruitment set volunteerno = volunteerno + 1 where eventid = {0}".format(evemt[0]))

        return render_template('event.html', event=event,form=form)

    return render_template('event.html', event=event,form=form)


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
        if cur.execute("SELECT * FROM userdata WHERE username = %s AND pass = %s", (input_user, input_pass)) is not None:
            cur.execute("SELECT * FROM userdata WHERE username = %s AND pass = %s", (input_user, input_pass))
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

