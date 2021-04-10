from app import app
from flask import render_template, flash, redirect, request, session, url_for
from flaskext.mysql import MySQL
from app.forms import StartEventForm

mysql = MySQL(autocommit=True)
mysql.init_app(app)

@app.route('/start-event-portal', methods=['GET', 'POST'])
def eventPortal():
    form = StartEventForm()
    if session['loggedin'] == True and request.method == "POST":
        userid = session['id']
        eventName = form.eventName.data
        description = form.description.data
        volunteerCount = form.volunteerCount.data
        city = form.city.data
        province = form.province.data
        startEvent = form.startEvent.data
        endEvent = form.endEvent.data
        cur = mysql.get_db().cursor()
        if userid != '' and eventName != '' and description != '' and volunteerCount != '' and city != '' and province != '' and startEvent != '' and endEvent != '':
            cur.execute("INSERT INTO Recruitment (userid, title, description, volunteerno, city, province, start_date, end_date) VALUES ({0}, '{1}', '{2}', {3}, '{4}', '{5}', '{6}', '{7}')".format(userid, eventName, description, volunteerCount, city, province, startEvent, endEvent))
        cur.close()
    return render_template('startEvent.html', title = 'Host Event', form=form)

@app.route('/add-friend/<int:friend_id>', methods=['GET', 'POST'])
def addFriend(friend_id):
    if session['loggedin'] == True and request.method == "POST":
        userid = session['id']
        friendid = friend_id
        if userid != '' and friendid = '':
            cur.execute("INSERT INTO friends (userid, friendid) VALUES ({0}, {1})".format(userid, friendid))
    return redirect(f'/profile/{friendid}')

@app.route('/add-friend/<int:friend_id>', methods=['GET', 'POST'])
def removeFriend(friend_id):
    if session['loggedin'] == True and request.method == "POST":
        userid = session['id']
        friendid = friend_id
        if userid != '' and friendid = '':
            cur.execute("DELETE FROM friends WHERE userid = {0} AND friendid = {1}".format(userid, friendid))
    return redirect(f'/profile/{friendid}')