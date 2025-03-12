from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests

#app = Flask(__name__)

# Import the app and login_manager from the app package
from app import app, login_manager

# Dummy user for authentication
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# Hardcoded user credentials (for testing purposes)
users = {'test': {'password': 'test'}}

@login_manager.user_loader 
def load_user(user_id):
    return User(user_id)

# Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('home'))
        else:
            flash('Invalid credentials')
    return render_template('login.html')

# Logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Home Page (Authenticated)
@app.route('/home')
@login_required
def home():
    return render_template('home.html')

# User Page (Authenticated)
@app.route('/user')
@login_required
def user():
    response = requests.get('https://jsonplaceholder.typicode.com/users')
    users_data = response.json()
    return render_template('user.html', users=users_data)

# Album Page (Authenticated)
@app.route('/album')
@login_required
def album():
    response = requests.get('https://jsonplaceholder.typicode.com/albums')
    albums_data = response.json()
    return render_template('album.html', albums=albums_data)

# Photo Page (Authenticated)
@app.route('/photo')
@login_required
def photo():
    response = requests.get('https://jsonplaceholder.typicode.com/photos')
    photos_data = response.json()
    return render_template('photo.html', photos=photos_data)

# Search bar functionality 
