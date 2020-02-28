from flask import Blueprint,render_template,request,flash,redirect,url_for
from starter.blueprints.users.forms import (RegistratotionForm,LoginForm,UpdateAccountForm,PasswordUpateForm)
from starter import bcrypt, db, login_manager
from starter.model import User
from flask_login import login_user,logout_user, current_user, login_required

import datetime

Users = Blueprint('Users',__name__)


@Users.route('/')
def index():
    return render_template('index.html')


#------------------------------ Signup ----------------------------------
@Users.route('/signup/',methods=['GET','POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('Main.index'))


    form = RegistratotionForm(request.form)
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        birthDate = datetime.datetime.strptime(form.birth_date.data, '%m/%d/%Y')
        #print(birthDate
        #print(birthDate.strftime('%Y-%m-%d'))

        user = User(firstname = form.firstname.data,lastname = form.lastname.data,password=hashed_password,email=form.email.data,birth_date=birthDate.strftime('%Y-%m-%d'),country=form.country.data,city=form.city.data,university=form.university.data,graduation_year=form.graduation_year.data,specialization=form.specialization.data,phone=form.phone.data,gender = form.gender.data)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome  { form.firstname.data}, Your account has been created successfully','success')

        return redirect(url_for('Main.index'))

    return render_template('signup.html',form =form,title = 'Sign Up' )


# ------------------------------ Login ----------------------------------
@Users.route('/login/', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('Main.index'))
    show_valid_message = True
    form = LoginForm(request.form)
    if form.validate_on_submit():
        show_valid_message = False
        user = User.query.filter_by(email = form.email.data).first()

        if user and bcrypt.check_password_hash(user.password,form.password.data):
            login_user(user,remember=form.remember.data)
            flash(f'Welcome {user.firstname}!', 'success')

            next_page = request.args.get('next')
            if current_user.role =='admin':
                return redirect(next_page) if next_page else redirect(url_for('Admin.dashboard'))
            if current_user.role !='admin':
                return redirect(next_page) if next_page else redirect(url_for('Main.index'))
        else:
            flash('Your email or password are not correct, try again!', 'danger')
    elif request.method == 'GET':
        show_valid_message = True

    return render_template('login.html', title='Login In', form=form,show_valid_message=show_valid_message)



# ------------------------------ Logout ----------------------------------
@Users.route('/logout/')
@login_required
def logout():
    logout_user()
    flash('You have been logged in successfully','success')
    return render_template('index.html')


# ------------------------------ Account ----------------------------------

@Users.route('/account/',methods=['GET','POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():


        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        current_user.email = form.email.data
        current_user.phone = form.phone.data
        print(type(current_user))
        if str(current_user.birth_date) == str(form.birth_date.data):
            current_user.birth_date = form.birth_date.data #birthDate.strftime('%Y-%m-%d')
        else:
            birthDate = datetime.datetime.strptime(form.birth_date.data, '%m/%d/%Y')
            current_user.birth_date = birthDate.strftime('%Y-%m-%d')

        current_user.country = form.country.data
        current_user.city = form.city.data
        current_user.university = form.university.data
        current_user.specialization = form.specialization.data
        current_user.graduation_year = form.graduation_year.data

        db.session.commit()

        flash("Your account has been updated",'success')

        return redirect(url_for('Users.account'))
    elif request.method == 'GET':
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
        form.email.data = current_user.email
        form.phone.data = current_user.phone
        form.birth_date.data = current_user.birth_date
        form.country.data = current_user.country
        form.city.data = current_user.city
        form.university.data = current_user.university
        form.specialization.data = current_user.specialization
        form.graduation_year.data = current_user.graduation_year

    return render_template('account.html',form=form)

# ------------------------------ Password ----------------------------------
@Users.route('/account/password/',methods=['GET','POST'])
@login_required
def password():
    form = PasswordUpateForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')

        current_user.password = hashed_password
        current_user.confirm_password = hashed_password
        db.session.commit()

        flash("Your password has been updated",'success')

        return redirect(url_for('Users.password'))

    return render_template('account_passwrod.html', form=form)