from app import app, requests, db, bcrypt
from flask import render_template, url_for, flash, redirect, request, abort
from app.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, CommentForm
from app.models import User, Post, Comment
from flask_login import login_user, current_user, logout_user, login_required


@app.route('/')
@app.route("/home")
def home():
    quote = requests.get_quote()
    posts = Post.query.all()
    return render_template('home.html', posts=posts, quote=quote)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode('utf-8')
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created', 'primary')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
        else:
            flash('Error. Please check your email and password', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('your account is updated', 'success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data == current_user.username
        form.email.data == current_user.email
    return render_template('account.html', title='Account', form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data,
                    content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'primary')
        return redirect(url_for('home'))
    return render_template('create_blog.html', title='New Post',
                           form=form, legend='New Post')


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    comments = Comment.query.all()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'primary')
        return redirect(url_for('home'))
    return render_template('update.html', title=post.title, post=post, form=form, comments=comments)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
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
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_blog.html', title='Update Blog',
                           form=form, legend='Update Blog')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Blog deleted!', 'primary')
    return redirect(url_for('home'))


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_comment(comment_id):
    comment = Comment.query.get_or_404(post_id)
    db.session.delete(comment)
    db.session.commit()
    flash('Comment deleted!', 'primary')
    return redirect(url_for('home'))
