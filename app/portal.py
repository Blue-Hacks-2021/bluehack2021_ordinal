from app import app
from flask import render_template, flash, redirect, request, session, url_for
from flaskext.mysql import MySQL
from app.forms import StartEventForm

mysql = MySQL(autocommit=True)
mysql.init_app(app)

@app.route('/start-event-portal', methods=['GET', 'POST'])
def eventportal():
    form = StartEventForm()
    if session['loggedin'] == True:
        userid = session['id']
        eventName = form.eventName.data
        description = form.eventName.data
        volunteerCount = form.eventName.data
        city = form.eventName.data
        province = form.eventName.data
        startEvent = form.eventName.data
        endEvent = form.eventName.data
        cur = mysql.get_db().cursor()
        if userid != '' and eventName != '' and description != '' and volunteerCount != '' and city != '' and province != '' and startEvent != '' and endEvent != '':
            cur.execute("INSERT INTO Recruitment (userid, title, description, volunteerno, city, province, start_date, end_date) 
            VALUES ({userid}, '{eventName}', '{description}', {volunteerCount}, '{city}', '{province}', '{startEvent}', '{endEvent}')")
        cur.close()
        return render_template()

    else:
        return 'Auth Error'