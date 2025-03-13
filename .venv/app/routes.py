from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import requests
from app import app, db, bcrypt
from app.forms import RegistrationForm, LoginForm
from app.models import User

#app = Flask(__name__)

# Import the app and login_manager from the app package
from app import app, login_manager

# Hardcoded user credentials (for testing purposes)
users = {'test': {'password': 'test'}}

@login_manager.user_loader 
def load_user(user_id):
    return User.query.get(int(user_id))

# Landing Page
@app.route('/')
def index():
    return render_template('index.html')

# Registration Page
@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password_hash=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Login Page
from flask_login import login_user, current_user, logout_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            flash('Login successful!', 'success') 
            return redirect(url_for('home'))
        else:
            flash('Login failed. Please check your email and password.', 'danger')
    return render_template('login.html', form=form)

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
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 10

    response = requests.get('https://jsonplaceholder.typicode.com/albums')
    albums_data = response.json()
    
    if search_query:
        albums_data = [album for album in albums_data if search_query.lower() in album['title'].lower()]
    
    total = len(albums_data)
    start = (page - 1) * per_page
    end = start + per_page
    albums_data = albums_data[start:end]
    
    has_next = end < total

    return render_template('album.html', albums=albums_data, page=page, has_next=has_next)

# Photo Page (Authenticated)
@app.route('/photo')
@login_required
def photo():
    search_query = request.args.get('search', '')
    page = request.args.get('page', 1, type=int)
    per_page = 15

    response = requests.get('https://jsonplaceholder.typicode.com/photos')
    photos_data = response.json()
    
    if search_query:
        photos_data = [photo for photo in photos_data if search_query.lower() in photo['title'].lower()]
    
    total = len(photos_data)
    start = (page - 1) * per_page
    end = start + per_page
    photos_data = photos_data[start:end]
    
    has_next = end < total

    return render_template('photo.html', photos=photos_data, page=page, has_next=has_next)

