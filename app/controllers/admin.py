# backend/app/controllers/admin.py
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app import db, app, allowed_file  # Import app here
import os
from werkzeug.utils import secure_filename
from app.models.event import Event
from app.models.user import User
from app.models.cart import Cart
from app.forms import AddEventForm, EditEventForm, DeleteEventForm

admin_bp = Blueprint('admin', __name__)

def admin_required():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    if not user.is_admin:
        flash('You must be an admin to access this page!')
        return redirect(url_for('events.event_list'))
    return None

@admin_bp.route('/dashboard')
def dashboard():
    check = admin_required()
    if check:
        return check
    
    events = Event.query.all()
    form = DeleteEventForm()
    return render_template('admin_dashboard.html', events=events, form=form)

@admin_bp.route('/add_event', methods=['GET', 'POST'])
def add_event():
    check = admin_required()
    if check:
        return check
    
    form = AddEventForm()
    if form.validate_on_submit():
        image_file = form.image.data
        image_filename = None
        if image_file and allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)  # Use app here
            image_file.save(image_path)
        
        event = Event(
            name=form.name.data,
            date=form.date.data,
            price=form.price.data,
            tickets_available=form.tickets_available.data,
            image_url=image_filename
        )
        db.session.add(event)
        db.session.commit()
        flash('Event added successfully!')
        return redirect(url_for('admin.dashboard'))
    return render_template('add_event.html', form=form)

@admin_bp.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
def edit_event(event_id):
    check = admin_required()
    if check:
        return check
    
    event = Event.query.get_or_404(event_id)
    form = EditEventForm(obj=event)
    if form.validate_on_submit():
        event.name = form.name.data
        event.date = form.date.data
        event.price = form.price.data
        event.tickets_available = form.tickets_available.data
        
        image_file = form.image.data
        if image_file and allowed_file(image_file.filename):
            image_filename = secure_filename(image_file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)  # Use app here
            image_file.save(image_path)
            event.image_url = image_filename
        
        db.session.commit()
        flash('Event updated successfully!')
        return redirect(url_for('admin.dashboard'))
    return render_template('edit_event.html', form=form, event=event)

@admin_bp.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    check = admin_required()
    if check:
        return check
    
    form = DeleteEventForm()
    if form.validate_on_submit():
        event = Event.query.get_or_404(event_id)
        cart_items = Cart.query.filter_by(event_id=event_id).all()
        if cart_items:
            flash('Cannot delete event: Tickets are present in one or more carts. Please remove them first.')
        else:
            db.session.delete(event)
            db.session.commit()
            flash('Event deleted successfully!')
    else:
        flash('Failed to delete event due to invalid request.')
    return redirect(url_for('admin.dashboard'))