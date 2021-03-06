from operator import imod
from flask.globals import request
from flask_wtf.recaptcha.widgets import JSONEncoder
from tribe.models import User, Post
from flask import json, render_template, url_for, flash, redirect, abort
from tribe.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from tribe import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
import secrets
import os
import requests



@app.route('/', methods = ['GET', 'POST'])
@app.route('/one', methods = ['GET', 'POST'])
def one():
    page = request.args.get('page', 1, type = int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page = page, per_page=5)
    return render_template('one.html', posts = posts)


@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash(f'Already logged in! lmao', 'success')
        return redirect(url_for("home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username = form.username.data, email = form.email.data, password = hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created! You can now log in!', 'success')
        return redirect(url_for('login'))

    return render_template('register.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash(f'Already logged in! lmao', 'success')
        return redirect(url_for("home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            flash(f'Succesfully logged in!', 'success')
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash(f'Please check the credentials!', 'danger')
    return render_template('login.html', form = form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash(f'Successfully logged out!', 'success')
    return redirect(url_for('one'))

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static', picture_fn)
    form_picture.save(picture_path)

    output_size = (256, 256)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    return picture_fn

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash(f'Your account info has been updated!', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email


    image_file = url_for('static', filename = current_user.image_file)
    return render_template('account.html', image_file = image_file, form = form)

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/two')
@login_required
def two():
    j = requests.get(url = "https://codeforces.com/api/contest.standings", params= {'contestId' : 1003, 'from' : 1, 'count' : 10, })
    j = j.json()
    return render_template('two.html', info = j)

@app.route('/three')
@login_required
def three():
    return render_template('three.html')



@app.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title = form.title.data, content = form.content.data, author = current_user)
        db.session.add(post)
        db.session.commit()
        flash(f'Your post has been created!', 'success')
        return redirect(url_for('one'))
    return render_template('create_post.html', form = form, legend = 'Create Post')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post = post)

@app.route('/post/<int:post_id>/update', methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated', 'success')
        return redirect(url_for('post', post_id = post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content

    return render_template('create_post.html', form = form, legend = 'Update Post')

@app.route('/post/<int:post_id>/delete', methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted', 'success')  
    return redirect(url_for('one'))

@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username = username).first_or_404()
    posts = Post.query.filter_by(author = user).order_by(Post.date_posted.desc()).paginate(page = page, per_page = 5)
    return render_template('user_post.html', posts = posts, user = user)