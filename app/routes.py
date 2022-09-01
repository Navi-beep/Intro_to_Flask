from app import app
from flask import render_template, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import SignupForm, PostForm, LoginForm
from app.models import User, Post


@app.route('/')
def index():
    posts = Post.query.all()
    print(posts)
    return render_template('index.html', posts=posts)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    form = SignupForm()
    # if the form is submitted and all the data is valid
    if form.validate_on_submit():
        print('Form has been validated! Hooray!!!!')
        email = form.email.data
        username = form.username.data
        password = form.password.data
        # Before we add the user to the database, check to see if there is already a user with username or email
        existing_user = User.query.filter((User.email == email) | (User.username == username)).first()
        if existing_user:
            flash('A user with that username or email already exists.', 'danger')
            return redirect(url_for('signup'))
            
        new_user = User(email=email, username=username, password=password)
        flash(f"{new_user.username} has been created.", "success")
        return redirect(url_for('index'))
    return render_template('signup.html', form=form)


@app.route('/create', methods=["GET", "POST"])
@login_required
def create():
    form = PostForm()
    if form.validate_on_submit():
        # Get the data from the form
        title = form.title.data
        body = form.body.data
        # Create a new instance of Post with the form data
        new_post = Post(title=title, body=body, user_id=current_user.id)
        # flash a message saying the post was created
        flash(f'{new_post.title} has been created.', 'secondary')
        # Redirect back to home page
        return redirect(url_for('index'))

    return render_template('createpost.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = User.query.filter_by(username=username).first()
        if user is not None and user.check_password(password):
            login_user(user)
            flash(f'Welcome back {user.username}!', 'success')
            return redirect(url_for('index'))
        
        else:
            flash('Incorrect username and/or password. Please try again', 'danger')
            return redirect(url_for('login'))

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    logout_user()
    flash('You have asuccessfully logged out', 'primary')
    return redirect(url_for('index'))



@app.route('/posts/<post_id>')
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)

    
@app.route('/posts/<post_id>/edit', methods=["GET", "POST"])
@login_required
def edit_post(post_id):
    post_to_edit = Post.query.get_or_404(post_id)
    if post_to_edit.author != current_user:
        flash('You do not have permission to edit this post', 'danger')
        return redirect(url_for('view_post', post_id=post_id))
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data 
        post_to_edit.update(title=title, body=body)
        flash(f'{post_to_edit.title} has been updated', 'success')
        return redirect(url_for('view_post', post_id=post_id))

    return render_template('edit_post.html', post=post_to_edit, form=form)
    
@app.route('/posts/<post_id>/delete')
@login_required
def delete_post(post_id):
    post_to_delete = Post.query.get_or_404(post_id)
    if post_to_delete.author != current_user:
        flash('You do not have permission to delete this post', 'danger')
        return redirect(url_for('index'))
    post_to_delete.delete()
    flash(f'{post_to_delete.title} has been deleted', 'info')
    return redirect(url_for('index')) 