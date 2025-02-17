import os
from werkzeug.utils import secure_filename
from models.image import Image
from models import db
from config import Config

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

def save_image(file, user):
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        user_folder = os.path.join(Config.UPLOAD_FOLDER, str(user.id))
        if not os.path.exists(user_folder):
            os.makedirs(user_folder)
        filepath = os.path.join(user_folder, filename)
        file.save(filepath)
        image = Image(filename=filename, mimetype=file.mimetype, owner=user)
        db.session.add(image)
        db.session.commit()
        return image
    return None

def get_user_images(user):
    return user.images.all()

def delete_image(image_id, user):
    image = Image.query.filter_by(id=image_id, user_id=user.id).first()
    if image:
        filepath = os.path.join(Config.UPLOAD_FOLDER, str(user.id), image.filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        db.session.delete(image)
        db.session.commit()
        return True
    return False
