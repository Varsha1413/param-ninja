from flask import Blueprint,  render_template, redirect, url_for, request, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import User
from starter import db

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
     # login code goes here
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user)
    return redirect(url_for('main.index'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

@auth.route("/profile")
@login_required
def profile():
    return render_template("profile.html", current_user = current_user)

@auth.route("/profile", methods = ["POST"])
@login_required
def profile_update():
    # Code to update profile
    old_password = request.form.get('old_password')
    new_password = request.form.get("new_password")
    
    if new_password == '':
        flash("The new password should be filled!", 'error')
        return render_template("profile.html", current_user = current_user)

    user = User.query.filter_by(email=current_user.email).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, old_password):
        flash('Please check your password and try again.', 'error')
        return redirect(url_for('auth.profile')) # if password is wrong, reload the page

    # Update user password and name
    user.email = request.form.get("email")
    user.password = generate_password_hash(new_password, method='sha256')
    db.session.commit()
    
    flash("Your data was updated!", 'success')
    return render_template("profile.html", current_user = current_user)
