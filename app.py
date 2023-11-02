from flask import Flask, render_template, request
import mysql.connector

app = Flask(__name__)

myconn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='',
    database='dbstores'
)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/registration')
def registration():
    return render_template('registration.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/verify', methods=['POST', 'GET'])
def verify():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        mycursor = myconn.cursor()
        sql = "SELECT * FROM tblusers WHERE userid=%s AND password=%s AND status=1"
        data = (userid, password)
        mycursor.execute(sql, data)
        myresult = mycursor.fetchall()

        if myresult:
            row = myresult[0]
            name = row[3]
            accesslevel = row[4]
            return render_template('admin_dashboard.html', userid=userid, name=name, accesslevel=accesslevel)
    return render_template('login.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        userid = request.form['userid']
        password = request.form['password']
        name = request.form['name']
        mycursor = myconn.cursor()
        sql = "INSERT INTO tblusers (userid,password,name) VALUES (%s,%s,%s)"
        data = (userid, password, name)
        mycursor.execute(sql, data)
        myconn.commit()

        mycursor1 = myconn.cursor()
        sql = "SELECT * FROM tblusers"
        mycursor1.execute(sql)
        myresult = mycursor1.fetchall()
        if myresult:
            return render_template('users.html', users=myresult)

@app.route('/users', methods=['POST', 'GET'])
def users():
    mycursor = myconn.cursor()
    sql = "SELECT * FROM tblusers"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    if myresult:
        return render_template('users.html', users=myresult)
    else:
        return render_template('admin_dashboard.html')

@app.route('/update/<id>', methods=['POST', 'GET'])
def update(id):
    if request.method == 'GET':
        mycursor = myconn.cursor()
        sql = "SELECT * FROM tblusers WHERE id=%s"
        data = (id,)
        mycursor.execute(sql, data)
        myresult = mycursor.fetchall()
        if myresult:
            return render_template('update_user.html', myresult=myresult)

@app.route('/updateuser', methods=['POST', 'GET'])
def updateuser():
    if request.method == 'POST':
        id = request.form['id']
        userid = request.form['userid']
        password = request.form['password']
        name = request.form['name']
        accesslevel = request.form['accesslevel']
        status = request.form['status']
        mycursor = myconn.cursor()
        sql = "UPDATE tblusers SET userid=%s,password=%s,name=%s,accesslevel=%s,status=%s WHERE id=%s"
        data = (userid, password, name, accesslevel, status, id)
        mycursor.execute(sql, data)
        myconn.commit()

        mycursor1 = myconn.cursor()
        sql = "SELECT * FROM tblusers"
        mycursor1.execute(sql)
        myresult = mycursor1.fetchall()
        if myresult:
            return render_template('users.html', users=myresult)

@app.route('/deleteuser/<id>')
def deleteuser(id):
    mycursor = myconn.cursor()
    sql = "DELETE FROM tblusers WHERE id=%s"
    data = (id,)
    mycursor.execute(sql, data)
    myconn.commit()
    mycursor1 = myconn.cursor()
    sql = "SELECT * FROM tblusers"
    mycursor1.execute(sql)
    myresult = mycursor1.fetchall()
    if myresult:
        return render_template('users.html', users=myresult)

if __name__ == '__main__':
    app.run(debug=True)
