from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SubmitField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError
import re

class RegistrationForm(FlaskForm):
    def validate_name(self, field):
        if not re.match(r"^[A-Za-z]+$", field.data):
            raise ValidationError("This field can only contain alphabets (no numbers or special characters).")

    first_name = StringField('First Name', validators=[
        DataRequired(),
        Length(min=2, message='First name must be at least 2 characters long.'),
        validate_name
    ])
    last_name = StringField('Last Name', validators=[
        DataRequired(),
        Length(min=2, message='Last name must be at least 2 characters long.'),
        validate_name
    ])
    email = EmailField('Email', validators=[
        DataRequired(),
        Email(message='Invalid email address.')
    ])
    password1 = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=8, message='Password must be at least 8 characters long.')
    ])
    password2 = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password1', message='Passwords must match.')
    ])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
