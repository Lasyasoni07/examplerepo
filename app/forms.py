from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed  # Import for file uploads
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, EmailField
from wtforms.validators import DataRequired, EqualTo, Length, Email, NumberRange
from app import app  # Import app for ALLOWED_EXTENSIONS

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Signup')

class ForgotPasswordForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Send Reset Link')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    submit = SubmitField('Reset Password')

class AddEventForm(FlaskForm):
    name = StringField('Event Name', validators=[DataRequired(), Length(max=100)])
    date = StringField('Date', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    tickets_available = IntegerField('Tickets Available', validators=[DataRequired(), NumberRange(min=0)])
    image = FileField('Event Image', validators=[FileAllowed(app.config['ALLOWED_EXTENSIONS'], 'Images only!')])  # New field
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