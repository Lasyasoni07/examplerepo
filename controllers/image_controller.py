from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory
from flask_login import login_required, current_user
from services.image_service import save_image, get_user_images, delete_image
from forms.upload_form import UploadForm
from config import Config
import os

image_bp = Blueprint('image', __name__)

@image_bp.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    form = UploadForm()
    if form.validate_on_submit():
        file = form.image.data
        image = save_image(file, current_user)
        if image:
            flash('Image uploaded successfully.', 'success')
            return redirect(url_for('image.gallery'))
        else:
            flash('Failed to upload image.', 'danger')
    return render_template('upload.html', form=form)

@image_bp.route('/gallery')
@login_required
def gallery():
    images = get_user_images(current_user)
    return render_template('gallery.html', images=images)

@image_bp.route('/delete/<int:image_id>', methods=['POST'])
@login_required
def delete(image_id):
    success = delete_image(image_id, current_user)
    if success:
        flash('Image deleted successfully.', 'success')
    else:
        flash('Failed to delete image.', 'danger')
    return redirect(url_for('image.gallery'))

@image_bp.route('/uploads/<filename>')
@login_required
def uploaded_file(filename):
    user_folder = os.path.join(Config.UPLOAD_FOLDER, str(current_user.id))
    return send_from_directory(user_folder, filename)
