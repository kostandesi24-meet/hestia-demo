from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase
config = {
  "apiKey": "AIzaSyAiehDCNzpJrY6sQMgSPMBUmNCyYI0Z--Q",
  "authDomain": "fir-hestia.firebaseapp.com",
  "databaseURL": "https://fir-hestia-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "fir-hestia",
  "storageBucket": "fir-hestia.appspot.com",
  "messagingSenderId": "120813961265",
  "appId": "1:120813961265:web:e294575ef7b2732e999510",
  "measurementId": "G-N8SMLY7TFJ",
  "databaseURL": "https://fir-hestia-default-rtdb.europe-west1.firebasedatabase.app/"
}
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

#signin
@app.route('/' , methods=['POST','GET'])
def signin():
    error = ''
    volunteering = db.child("volunteering").get().val()
    if volunteering is None:
        volunteering = {}
    if request.method == 'POST':
        try:
            uid = login_session['user']['localId']
            email = request.form['email']
            password = request.form['password']
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            db.child('signedinemail').set(email)
            # return render_template('home.html', volunteering=volunteering, error=error , uid=uid)
            return redirect(url_for('homep'))
        except:
            error = "error"
    return render_template('sign_in_page.html' , error=error)

#signup
@app.route('/signup',methods=['POST','GET'])
def signup():
    error = ""
    if request.method == 'POST':
        usernameu = request.form['name']
        emailu = request.form['email']
        passwordu = request.form['password']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(emailu, passwordu)
            uid = login_session['user']['localId']
            user = {"email": emailu, "password": passwordu, "username": usernameu}
            db.child('Users').child(uid).set(user)
            return redirect(url_for('signin'))
        except:
            error = "error"
    return render_template('sign_up_page.html' , error = error)

# signout
@app.route('/signout' , methods=['GET','POST'])
def signout():
    db.child('signedinemail').set("")
    login_session['user']=""
    return redirect(url_for('signin'))
#homepage
@app.route('/home' , methods=['POST','GET'])
def homep():
    return render_template('home.html')

#admin
@app.route('/admin' , methods=['POST','GET'])
def admin():
    error = ""
    uid = login_session['user']['localId']
    if request.method == 'POST':
        try: 
            location = request.form['in2']
            hours = request.form['in4']
            name = request.form['in1']
            numberop = request.form['in3']

            info = {"name": name, "numberop": numberop, "location": location, "hours": hours, "uid": uid}
            db.child('volunteering').push(info)
            volunteering = db.child("volunteering").get().val()
            if volunteering is None:
                volunteering = {}
            return render_template('index.html' , volunteering = volunteering , uid = uid)
        except:
            error = "error"
    return render_template('admin.html' , error = error)
# Code goes above here
if __name__ == '__main__':
    app.run(debug=True)