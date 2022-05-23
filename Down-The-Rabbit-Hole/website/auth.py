from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Snippet, Info
from . import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__) 

#----------------------------------------------------------------------------------------------------------------------------#
#LOGIN

@auth.route('/sign-in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST': 
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                flash("You're in!", category='success') #TODO ask Belle to draw our own flashes instead of having to use basic Flask ones
                login_user(user, remember=True) 
                return redirect(url_for('views.welcome_user'))
            else:
                flash('Oopsie, wrong username or password, try again.', category='error')
        else:
            flash('Oopsie, wrong username or password, try again.', category='error')
    return render_template("sign_in.html", user=current_user)

#----------------------------------------------------------------------------------------------------------------------------#
#LOGOUT

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

#----------------------------------------------------------------------------------------------------------------------------#
#SIGN UP

@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password1')
        confirm_password = request.form.get('password2')
        #DOING SOME VALIDATION CHECKS
        user = User.query.filter_by(email=email).first()
        user2 = User.query.filter_by(username=username).first()
        if user or user2:
            flash('Hmm, it seems like this username or email is already taken!', category='error')
        else:
            if len(email) < 4:
                flash('Invalid email address', category='error')
            elif password != confirm_password:
                flash("Your passwords don't match! Try again.", category='error')
            elif len(password) < 7:
                flash('Nuh uh, you need a stronger password!', category='error')
            else:
                #add user to database
                new_user = User(username=username, email=email, password=generate_password_hash(password, method='sha256'))
                db.session.add(new_user)
                db.session.commit()
                flash('Account created successfully! Welcome to the rabbit hold <3', category='success')
                login_user(new_user, remember=True)
                return redirect(url_for('views.welcome_user'))
    return render_template("signup.html", user=current_user)

#----------------------------------------------------------------------------------------------------------------------------#