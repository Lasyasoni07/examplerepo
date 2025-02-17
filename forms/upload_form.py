from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from config import Config
from wtforms import SubmitField

class UploadForm(FlaskForm):
    image = FileField('Image', validators=[
        FileRequired(),
        FileAllowed(Config.ALLOWED_EXTENSIONS, 'Allowed file types are png, jpg, jpeg, gif.')
    ])
    submit = SubmitField('Upload')
