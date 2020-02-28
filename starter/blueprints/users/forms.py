from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField, SelectField, BooleanField, DateField, RadioField
from wtforms.validators import Length,InputRequired,AnyOf,Required,Email,Optional,DataRequired,EqualTo,ValidationError, NumberRange, Regexp
from wtforms.fields.html5 import TelField
from starter import db
from starter.model import User
from flask_login import current_user
from langdetect import detect
from emoji import UNICODE_EMOJI

class RegistratotionForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(message='Please enter you first name')])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(),EqualTo('password',message='Passwords does not match')])
    phone = TelField('Phone', validators=[DataRequired(),Length(min=10,max=10,message="Phone number must consists of 10 digits"),Regexp('^[0-9]*$',message="Phone number should only contain numbers")])
    birth_date = StringField('Date of birth', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('Female','Female'),('Male','Male')])
    submit = SubmitField('Register')

    def validate_firstname(self, firstname):
        firstname = firstname.data

        count = 0
        for emoji in UNICODE_EMOJI:
            count += firstname.count(emoji)

        if (count > 0):
            print(count)
            raise ValidationError('a name cannot contain any emojis')

    def validate_phone_digit(self,phone):
        phone = phone.data
        if len(phone) < 10:
            raise ValidationError('Digits must not exceed 10 digits')
        elif len(phone) > 10:
            raise ValidationError('Digits must not be less than 10 digits')

    def validate_email(self,email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('There exists an account with the same email')


    def validate_phone(self,phone):
        user = User.query.filter_by(phone=phone.data).first()
        if user:
            raise ValidationError('There exists an account with the same phone number')

class LoginForm(FlaskForm):
    email = StringField('Email',validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Rember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    firstname = StringField('First Name', validators=[DataRequired(message='Please enter you first name')])
    lastname = StringField('Last Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password',
                                                                                             message='Passwords does not match')])
    phone = TelField('Phone', validators=[DataRequired(),
                                          Length(min=10, max=10, message="Phone number must consists of 10 digits"),
                                          Regexp('^[0-9]*$', message="Phone number should only contain numbers")])
    birth_date = StringField('Date of birth', validators=[DataRequired()])
    submit = SubmitField('Update Account')


    def validate_email(self,email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Th')

    def validate_phone_digit(self, phone):
        phone = phone.data
        if len(phone) < 10:
            raise ValidationError('Digits must not exceed 10 digits')
        elif len(phone) > 10:
            raise ValidationError('Digits must not be less than 10 digits')

    def validate_phone(self,phone):
        if phone.data != current_user.phone:
            user = User.query.filter_by(phone=phone.data).first()
            if user:
                raise ValidationError('There exists an account with the same phone number')

class PasswordUpateForm(FlaskForm):
    password = PasswordField('Passwordر', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password',
                                     validators=[DataRequired(), EqualTo('password', message='Passwords does not match')])
    submit = SubmitField('Update Password')

    def validate_password(self,password):
        if password.data == current_user.password:
            raise ValidationError('You cannot use the the current password')
