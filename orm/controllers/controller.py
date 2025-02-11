from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from orm.services.service import (
    create_user, authenticate_user, get_all_posts,
    create_post, create_comment, get_post_by_id
)
from orm.models.model import User
from orm.forms import RegistrationForm, LoginForm, PostForm, CommentForm
from flask_login import current_user

controller = Blueprint('controller', __name__)

@controller.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('controller.posts'))
    form = RegistrationForm()
    if form.validate_on_submit():
        create_user(form.username.data, form.email.data, form.password.data)
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('controller.login'))
    return render_template('register.html', form=form)

@controller.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('controller.posts'))
    form = LoginForm()
    if form.validate_on_submit():
        user = authenticate_user(form.email.data, form.password.data)
        if user:
            login_user(user, remember=form.remember.data)
            return redirect(url_for('controller.posts'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', form=form)

@controller.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('controller.login'))

@controller.route('/')
def base():
    return render_template('base.html')


@controller.route('/posts', methods=['GET', 'POST'])
@login_required
def posts():
    form = PostForm()
    if form.validate_on_submit():
        create_post(form.title.data, form.content.data, current_user.id)
        flash('Your post has been created!', 'success')
        return redirect(url_for('controller.posts'))
    posts = get_all_posts()
    return render_template('posts.html', posts=posts, form=form)

@controller.route('/posts/<int:post_id>', methods=['GET', 'POST'])
@login_required
def post_detail(post_id):
    post = get_post_by_id(post_id)
    if post.author.id != current_user.id:
        flash('You do not have permission to view this post.', 'danger')
        return redirect(url_for('controller.posts'))

    form = CommentForm()
    if form.validate_on_submit():
        create_comment(form.content.data, post_id, current_user.id)
        flash('Your comment has been added!', 'success')
        return redirect(url_for('controller.post_detail', post_id=post_id))
    return render_template('comments.html', post=post, form=form)

