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
        discussions.append({'comment': comments[i][2], 'comment_date': comments[i][3], 'reply': reply[2], 'reply_date': reply[3]})

    # Volunteer Button
    if request.method == "POST" and formVolunteer.validate_on_submit() and formVolunteer.volunteer.data:
        cur = mysql.get_db().cursor()
        cur.execute("Insert INTO Volunteers values ({0},{1}) ".format(user[0],event[0]))

        return redirect(url_for('index'))

    # Comment an Inquiry
    if request.method == "POST" and formComment.validate_on_submit() and formComment.submitComment.data:
        textComment = formComment.textComment
        
        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO Comments (eventid, commenttext) VALUES ({0}, '{1}')".format(event[0], textComment)) 
        
        return redirect('/event/{0}'.format(event[0]))

    # Reply to an Inquiry
    if request.method == "POST" and formReply.validate_on_submit() and formReply.submitReply.data:
        textReply = formReply.textReply
        
        cur = mysql.get_db().cursor()
        cur.execute("INSERT INTO Reply (commentid, replytext) VALUES ({0}, '{1}')".format("""Need comment id""", replyComment)) 
        
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

