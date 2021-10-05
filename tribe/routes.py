from tribe.models import User, Post
from flask import render_template, url_for, flash, redirect
from tribe.forms import RegistrationForm, LoginForm
from tribe import app

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/', methods = ['GET', 'POST'])
@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()

    if form.validate_on_submit():
        flash(f'Account Created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    for key, val in form.errors.items():
        print(key)
        for s in val:
            print(s)
    flash(f'Account NOT Created for {form.username.data}!', 'warning')
    return render_template('Register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if(form.username.data == 'admin' and form.password.data == 'password'):
            flash(f'You have been Logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash(f'Please Check the credentials!', 'danger')
            return redirect(url_for('login'))

    return render_template('Login.html', form = form)

@app.route('/one')
def one():
    return render_template('one.html')