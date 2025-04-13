from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed  # Import for file uploads
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, EmailField, DateField, TimeField
from wtforms.validators import DataRequired, EqualTo, Length, Email, NumberRange, ValidationError
from app import app  # Import app for ALLOWED_EXTENSIONS
import re

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max=80, message="Username must be at least 3 characters.")
    ])
    email = EmailField('Email', validators=[
        DataRequired(), Email(message="Invalid email format.")
    ])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters."),
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match.")
    ])
    submit = SubmitField('Signup')

    def validate_password(self, field):
        password = field.data
        if not re.search(r'\d', password):
            raise ValidationError('Password must contain at least one number.')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            raise ValidationError('Password must contain at least one special character.')

class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Reset Password')

class AddEventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired()])
    date = DateField('Date', format='%Y-%m-%d', validators=[DataRequired()])
    time = TimeField('Time', format='%H:%M', validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    tickets_available = IntegerField('Tickets Available', validators=[DataRequired()])
    image = FileField('Image')
    submit = SubmitField('Add Event')

class EditEventForm(AddEventForm):
    image = FileField('Event Image (optional)', validators=[FileAllowed(app.config['ALLOWED_EXTENSIONS'], 'Images only!')])  # Optional for edit
    submit = SubmitField('Update Event')

class BuyTicketForm(FlaskForm):
    submit = SubmitField('Add to Cart')

class UpdateCartForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[NumberRange(min=0)])
    submit = SubmitField('Update Cart')

class DeleteEventForm(FlaskForm):
    submit = SubmitField('Delete')

class DeleteUserForm(FlaskForm):
    submit = SubmitField('Delete')