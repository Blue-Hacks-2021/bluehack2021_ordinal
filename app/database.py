#these can be initialized in a different py file if you want
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'ordinaldb'
 
mysql = MySQL(app)


@app.route('/home', methods=['GET', 'POST'])
def home():
    """Renders the home page."""
    message=''

    if request.method == "POST" and 'username' in request.form and 'password' in request.form:
        details = request.form
        username = details['username']
        password = details['password']
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM userdatatb WHERE username = %s AND pass = %s", (username, password))
        mysql.connection.commit()
        account = cur.fetchone()

        
        if account:
            #change to token if needed
            session['username'] = account['username']
            session['email'] = account['email']
            session['loggedin'] = True
            session['city'] = account['city']
            session['province'] = account['province']
            session['id'] = account['id']


            return render_template('index.html', title='Home Page',
        usernametext=session['username'], isLoggedIn = True, year=datetime.now().year
        )
        else:
            message = 'Incorrect username/password!'

            return render_template('index.html', title='Home Page',
        usernametext=session['username'], isLoggedIn = False, year=datetime.now().year, message=message
        )
        cur.close()

@app.route('/register', methods=['GET', 'POST'])
def register():

    #you can relocate the textfield validations to here instead.
    if request.method == "POST":
        details = request.form
        #as always, switch to token if needed
        firstName = details['fname']
        lastName = details['lname']
        username = details['uname']
        middlename = details['mname']
        password = details['pass']
        city = details['city']
        province = details['province']
        email = details['email']
        cur = mysql.connection.cursor()

        if firstName != '' and lastName != '' and username != '' and password != '' and city != '' and province != '' and email != '':

            #maybe we can use stored procedures instead of hardcoding each and every query. Let's explore that option once we've built the basics
            cur.execute("INSERT INTO userdatatb(firstname, lastname, username, middlename, pass, city, province, email) VALUES (%s, %s,%s, %s,%s, %s,%s, %s)", (firstName, lastName,username, middlename, password, city, province, email))
            mysql.connection.commit()
        cur.close()

        return render_template(
        'index.html',
        title='Home Page')

    return render_template(
        'registration.html',
        title='Register')
