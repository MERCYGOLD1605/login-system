from flask import Flask, render_template, request, redirect, session
import json

app = Flask(__name__)
app.secret_key = "secret123"

def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except:
        return []

def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)

@app.route('/')
def home():
    if "user" in session:
        return f"Welcome {session['user']} <br><a href='/logout'>Logout</a>"
    return redirect('/login')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']

        users.append({"username": username, "password": password})
        save_users(users)

        return redirect('/login')

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user['username'] == username and user['password'] == password:
                session['user'] = username
                return redirect('/')

        return "Invalid credentials"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

app.run(debug=True)