from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'dsslslslsldsa'

# Enter your database connection details below
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'footballkick00'
app.config['MYSQL_DB'] = 'pythonlogin'

# Intialize MySQL
mysql = MySQL(app)

# http://localhost:5000/pythonlogin/ - this will be the login page
@app.route('/pythonlogin/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        # Fetch one record and return result
        account = cursor.fetchone()
        # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            # Redirect to home page
            return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'
    return render_template('index.html', msg=msg)

# http://localhost:5000/python/logout - this will be the logout page
@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/pythonlogin/home', methods=['GET','POST'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/pharmacist', methods=['GET','POST'])
def pharmacist():
    # Check if user is loggedin
    if request.method == 'POST' and 'ssnid' in request.form:
        ssnid = request.form['ssnid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query_string = "SELECT * FROM patientreg WHERE ssnid = %s"
        cursor.execute(query_string, (ssnid,))
        data = cursor.fetchall()
        return render_template('pharmacist.html', value=data)

    return render_template('pharmacist.html')

@app.route('/pythonlogin/patientreg', methods=['GET','POST'])
def patientreg():
    msg=''
    msg = 'Welcome to Registration Page'
    if request.method == 'POST' and 'ssnid' in request.form and 'pname' in request.form:
        pssnid = request.form['ssnid']
        name = request.form['pname']
        p_age = request.form['age']
        #doa = request.form['adddate']
        padd = request.form['add']
        pcity = request.form['city']
        pstate = request.form['state']
        tob = request.form['bedtype']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO patientreg VALUES ( NULL,%s, %s, %s,%s, %s , %s , %s  )', (pssnid, name, p_age, padd, pcity, pstate, tob))
        mysql.connection.commit()
        msg = 'You have successfully registered!'

    elif request.method == 'post':
        msg = 'Please Fill the Form'
    return render_template('patientreg.html', msg=msg)

@app.route('/pythonlogin/patientrecord', methods=['GET','POST'])
def patientrecord():

    msg = 'Patient Record Page'
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM patientreg')
    data = cursor.fetchall()
    mysql.connection.commit()
    #for row in data:

    return render_template('patientrecord.html',msg=msg, value=cursor)

@app.route('/pythonlogin/update', methods=['GET','POST'])
def update():
    msg=''
    msg='Patient Update Page'
    if request.method == 'POST':
        ssnid = request.form['ssnid']
        uname = request.form['pname']
        uge = request.form['age']
        uadd = request.form['add']
        ucity = request.form['city']
        ustate = request.form['state']
        utob = request.form['bedtype']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        sql = 'UPDATE patientreg SET patientname=%s, age=%s, address=%s, city=%s, state=%s, typeofbed=%s WHERE ssnid=%s'
        data = (uname,uge,uadd,ucity,ustate,utob,ssnid)
        cursor.execute(sql,data)
        mysql.connection.commit()
        msg = 'You have updated Patients Information!'
    return render_template('update.html',msg=msg)

@app.route('/pythonlogin/delete', methods=['GET','POST'])
def delete():
    msg = 'Patient Delete Page'
    if request.method == 'POST':
        ssnid = request.form['ssnid']
        uname = request.form['pname']
        uge = request.form['age']
        uadd = request.form['add']
        ucity = request.form['city']
        ustate = request.form['state']
        utob = request.form['bedtype']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('DELETE FROM patientreg WHERE ssnid=%s',(ssnid,))
        mysql.connection.commit()
        msg = 'You have Deleted Patients Information!'
    return render_template('delete.html', msg=msg)

@app.route('/pythonlogin/search', methods=['GET','POST'])
def search():
    msg = ''
    msg = 'Search Patient'
    if request.method == 'POST' and 'ssnid' in request.form:
        ssnid = request.form['ssnid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query_string = "SELECT * FROM patientreg WHERE ssnid = %s"
        cursor.execute(query_string, (ssnid,))
        data = cursor.fetchall()

        return render_template('search.html',msg=msg, value=data)

    return render_template('search.html',msg=msg)

@app.route('/pythonlogin/billing', methods=['GET','POST'])
def billing():
    msg=''
    Bill = 0
    bill1=0
    bill2=0
    msg='Billing Screen'
    if request.method == 'POST':
        days = int(request.form['days'])
        tob = request.form['bedtype']
        print(days)
        print(tob)
        gn = 2000
        ss = 4000
        sr = 8000
        list = []
        if tob == "General Ward":
            bill1 = days * gn
            list.append(bill1)
            print(bill1)
        if tob == "Semi Sharing":
            bill2 = int(days * ss)
            list.append(bill2)
            print(bill2)
        if tob == "Single Room":
            Bill = int(days * sr)
            list.append(Bill)
            print(Bill)
        return render_template('bill.html',msg=msg,list=list)

    return render_template('bill.html' , msg=msg)

@app.route('/pythonlogin/issuemed', methods=['GET','POST'])
def issuemed():
    msg = ''
    msg = 'Issue Medicines Page'
    if request.method == 'POST' and 'medicine' in request.form:
        medname = request.form['medicine']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM table2 WHERE medicine_name = %s ', (medname,))
        data = cursor.fetchall()
        print(data)
        return render_template('issuemed.html',msg=msg,value=data)

    return render_template('issuemed.html',msg=msg)

@app.route('/pythonlogin/purchase', methods=['GET','POST'])
def purchase():
    msg = ''
    msg = 'Purchase Medicines Page'
    if 'medquan' in request.form and request.method == 'POST' and 'medicine' in request.form:
        quan = int(request.form['medquan'])
        medname = request.form['medicine']
        print(quan)
        print(medname)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT rate_of_medicine FROM table2 WHERE medicine_name = %s ', (medname,))
        data = cursor.fetchone()
        keys = []
        values = []
        items = data.items()
        for item in items:
            keys.append(item[0]), values.append(item[1])

        int_form = values[0]
        rate = int_form * quan
        msg = 'Purchased Successful'
        return render_template('purchase.html', msg=msg,rate=rate)

    return render_template('purchase.html',msg=msg)

@app.route('/pythonlogin/diagnostics', methods=['GET','POST'])
def diagnostics():
    msg=''
    msg='Diagnostics Page'
    if request.method == 'POST' and 'ssnid' in request.form:
        ssnid = request.form['ssnid']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query_string = "SELECT * FROM patientreg WHERE ssnid = %s"
        cursor.execute(query_string, (ssnid,))
        data = cursor.fetchall()
        return render_template('diagnostics.html',msg=msg, value=data)
    return render_template('diagnostics.html',msg=msg)

@app.route('/pythonlogin/add_diag', methods=['GET','POST'])
def add_diag():
    msg=''
    msg='Diagnostics Page'
    if request.method == 'POST' and 'test' in request.form:
        dia_test = request.form['test']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        query_string = "SELECT * FROM diagnostics WHERE test_name = %s"
        cursor.execute(query_string, (dia_test,))
        data = cursor.fetchall()
        return render_template('add_diag.html',msg=msg, value=data)

    return render_template('add_diag.html', msg=msg)
if __name__=='__main__':
    app.run(debug=True)