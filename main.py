from flask import Flask, render_template,request,session,redirect,url_for
import mysql.connector
import re

app=Flask(__name__)
app.secret_key='53b4aed4b4c09e32b5e09b0b91c43cff'
conn=mysql.connector.connect(user="root",
                            host="127.0.0.1",
                            database='register')
@app.route('/')
@app.route('/login', methods=["GET","POST"])
def login():
        msg=' '
        if request.method=="POST" and 'username' in request.form and 'password' in request.form:
          username=request.form['username']
          password=request.form['password']
          cursor=conn.cursor(dictionary=True)
          cursor.execute("select * from account where username=%s and password=%s",(username,password))
          account=cursor.fetchone()

          if account:
            session["loggedin"]=True
            session['id'] = account['id']
            session['username']=account['username']
            msg="Loggedin successfully"
            return render_template("index.html",msg=msg)
          else:
            msg="Invalid usernmae/password"
        return render_template("login.html",msg=msg)
@app.route('/logout',methods=["GET","POST"])
def logout():
        if request.method=="post":
            session.pop('loggedin',None)
            session.pop('id',None)
            session.pop('username',None)
        return redirect(url_for('login'))
@app.route('/register',methods=["GEt","POST"])
def register():
    word=''
    if request.method=="POST" and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        username=request.form['username']
        password=request.form['password']
        email=request.form['email']
        cursor=conn.cursor()
        cursor.execute("select * from account where username='%s'" ,username)
        account=cursor.fetchone()
        if account:
            word="username already exists"
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            word= 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            word = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            word="please fill out the form"
        else:
            val=(username,password,email)
            sql="insert into account (username,password,email) values('%s','%s','%s')" % val

            cursor.execute(sql)
            conn.commit()
            word="You have succefully registered"
    elif request.method=="POST":
        word="please fill out the form"
    return render_template("register.html",word=word)


if __name__==("__main__"):
    app.run(debug=True)