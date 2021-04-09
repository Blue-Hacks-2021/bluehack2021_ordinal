from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm, RegistrationForm

@app.route('/')
@app.route('/index')
def index():
    cur = mysql.connection.cursor()
    
    user = {'username': username}
    return render_template('index.html', title='Home', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/register', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == "POST":
        #as always, switch to token if needed
        firstName = form.firstName.data
        lastName = form.lastName.data
        username = form.userame.data
        middlename = form.middleName.data
        password = form.password.data
        city = form.city.data
        province = form.province.data
        email = form.email.data
        cur = mysql.connection.cursor()
        if firstName != '' and lastName != '' and username != '' and password != '' and city != '' and province != '' and email != '':
            #maybe we can use stored procedures instead of hardcoding each and every query. Let's explore that option once we've built the basics
            cur.execute("INSERT INTO userdatatb(firstname, lastname, username, middlename, pass, city, province, email) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)", (firstName, lastName,username, middlename, password, city, province, email))
            mysql.connection.commit()
        cur.close()
        return redirect('/login')
    return render_template('registration.html', title='Register')

    