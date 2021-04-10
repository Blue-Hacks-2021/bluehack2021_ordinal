from app import app
from flask import render_template, flash, redirect, request, session, url_for
from app.forms import LoginForm, RegistrationForm, VolunteerForm, CommentForm, ReplyForm
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
    return redirect(url_for('login'))
    """
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
    """

@app.route('/home')
def home():
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM Recruitment")
    events = cur.fetchall()
    event_hosts = []

    for i in range(len(events)):
        event_hosts.append(get_user(events[i][1]))

    return render_template('home.html', title='Home', events=events, event_hosts=event_hosts)

#Profile Pages 2

@app.route('/profile')
def profile():
    """
    user = get_user(user_id)
    cur = mysql.get_db().cursor()
    #if cur.execute("SELECT * FROM recruitment") is None:
        # Placeholder for text that says, No Recruitments Ongoing. Start one now!
    
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM Recruitment r INNER JOIN Volunteers v ON r.eventid = v.eventid where v.userid = {0}".format(user[0]))
    jevents = cur.fetchall()
    cur.execute("SELECT count(*) FROM Recruitment r INNER JOIN Volunteers v ON r.eventid = v.eventid where v.userid = {0}".format(user[0]))
    jeventcount = cur.fetchone()
    cur.execute("SELECT * FROM Recruitment where userid = {0} ".format(user[0]))
    events = cur.fetchall()
    
    cur.execute("SELECT count(*) FROM Recruitment where userid = {0} ".format(user[0]))
    eventcount = cur.fetchone()
    return render_template('profile.html', user=user, events=events, eventcount=eventcount[0],jevents=jevents, jeventcount=jeventcount[0])
    """
    return render_template('profile.html', title='Profile')
    

#Event Pages 2
@app.route('/event/<int:event_id>', methods=['GET', 'POST'])
def event(event_id):
    event = get_event(event_id)
    cur = mysql.get_db().cursor()
    cur.execute("SELECT * FROM userdata where userid = {0}".format(session['id']))
    user = cur.fetchone()

    formVolunteer = VolunteerForm()
    formComment = CommentForm()
    formReply = ReplyForm()

    #Comment and Reply Section
    cur.execute("SELECT * FROM Comments where eventid = {0} ".format(event[0]))
    comments = cur.fetchall()
    discussions = []

    for i in range(len(comments)):
        cur.execute("SELECT * FROM Reply where commentid = {0} ".format(comments[i][0]))
        reply = cur.fetchone()
        if reply is not None:
            discussions.append({'comment': comments[i][2], 'comment_date': comments[i][3], 'reply': reply[2], 'reply_date': reply[3]})
        else:
            discussions.append({'comment': comments[i][2], 'comment_date': comments[i][3], 'reply': '', 'reply_date': ''})

    # Volunteer Button
    cur.execute("SELECT * FROM Volunteers where eventid = {0} and userid = {1}".format(event[0], session['id']))
    volunteered = cur.fetchone()
    if volunteered is None:
        if request.method == "POST" and formVolunteer.volunteer.data:
            cur = mysql.get_db().cursor()
            cur.execute("Insert INTO Volunteers values ({0},{1}) ".format(user[0],event[0]))

            return redirect(url_for('index'))

    # Comment an Inquiry
    if request.method == "POST" and formComment.submitComment.data:
        textComment = formComment.textComment.data
        
        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO Comments (eventid, commenttext) VALUES ({0}, '{1}')".format(event[0], textComment)) 
        
        return redirect('/event/{0}'.format(event[0]))

    # Reply to an Inquiry
    if request.method == "POST" and formReply.submitReply.data:
        textReply = formReply.textReply.data
        
        for i in range(len(comments)):
            cur = mysql.get_db().cursor()
            cur.execute("INSERT INTO Reply (commentid, replytext) VALUES ({0}, '{1}')".format(placeholder, textReply)) 
        
        return redirect('/event/{0}'.format(event[0]))


    return render_template('event.html', event=event,formVolunteer=formVolunteer, formComment=formComment, formReply=formReply, discussions=discussions)

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
            if account is None:
                return "Login Error"
            session['id'] = account[0]
            session['username'] = account[3]
            session['loggedin'] = True

            return redirect('/home')
    return render_template('loginPage.html', title='Sign In', form=form)

@app.route('/logout/', methods=['GET'])
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
    return render_template('register.html', title='Register', form=form)
    
"""
@app.route('/register')
def register():
    return render_template('register.html', title='Registration')

@app.route('/home')
def home():
    return render_template('home.html', title='Home')

@app.route('/profile')
def profile():
    return render_template('profile.html', title='Profile')

@app.route('/create-event')
def createEvent():
    return render_template('create-event.html', title='Create event')

@app.route('/event')
def eventPage():
    return render_template('event.html', title='Event')

@app.route('/volunteered')
def volunteeredPage():
    return render_template('volunteered-events.html', title='Volunteered')
"""