from flask import Blueprint,render_template,request,flash,redirect,url_for
from .models import User
from werkzeug.security import generate_password_hash,check_password_hash
from . import db
from flask_login import login_user,login_required,logout_user,current_user

auth=Blueprint('auth',__name__)

@auth.route('/login',methods=['GET','POST'])
def login():

    # data=request.form
    # print(data)

    if request.method == 'POST':
        email=request.form.get('email')
        # print(email)
        password=request.form.get('password')
        # print(password)

        user =User.query.filter_by(email=email).first()

        # print(user.password)
        # print(password)
        if user:
            if check_password_hash(user.password,password):
                flash("Logged in successfully!",category='success')
                login_user(user,remember=False)
                return redirect(url_for('views.home'))
            else:
                 flash('Incorrect password,try again',category='error') 
        else:
            flash('Email does not exist',category='error')



    return render_template("login.html",user=current_user)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    
    return redirect(url_for('auth.login'))   

@auth.route('/sign-up',methods=['GET','POST'])
def sign_up():
    if request.method=='POST':
        email=request.form.get('email')
        firstName=request.form.get('firstName')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        
        # user =User.query.filter_by(email=email).first()
        # if user:
        #     flash('Email already exists',category='error')
        if len(email)<5:
            flash("Email must be greater than 4 character",category="error")
        elif len(firstName)<3:
            flash("First Name must be greater than 2 character",category="error")
        elif password1 !=password2:
            flash("Password does not match",category="error")
        elif len(password1)<6:
            flash("Password must be greater than 6 character",category="error")
        else:
            new_user=User(email=email,first_name=firstName,password=generate_password_hash(password1,method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            # login_user(user,remember=True)
            flash("Account created",category="success")
            return redirect(url_for('views.home'))



    return render_template("sign_up.html",user=current_user)    
