from flask import Flask, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash
import json

app = Flask(__name__)
app.secret_key = "secret123"


# 📂 Load users
def load_users():
    try:
        with open("users.json", "r") as file:
            return json.load(file)
    except:
        return []


# 💾 Save users
def save_users(users):
    with open("users.json", "w") as file:
        json.dump(users, file)


# 🏠 Home route
@app.route('/')
def home():
    if "user" in session:
        return f"Welcome {session['user']} <br><a href='/logout'>Logout</a>"
    return redirect('/login')


# 📝 Register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = generate_password_hash(request.form['password'])
        print("REGISTER CALLED")

        # 🚫 Prevent duplicate users
        for user in users:
            if user['username'] == username:
                return "User already exists!"

        users.append({
            "username": username,
            "password": password
        })

        save_users(users)

        return redirect('/login')

    return render_template('register.html')


# 🔐 Login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        users = load_users()
        username = request.form['username']
        password = request.form['password']

        for user in users:
            if user['username'] == username and check_password_hash(user['password'], password):
                session['user'] = username
                return redirect('/')

        return "Welcome Usser!"

    return render_template('login.html')


# 🚪 Logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')


# ▶️ Run app
if __name__ == "__main__":
    app.run(debug=True)