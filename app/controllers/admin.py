from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app import db, app, allowed_file
import os
from werkzeug.utils import secure_filename
from app.models.event import Event
from app.models.user import User
from app.models.cart import Cart
from app.models.order import Order
from app.models.contact_query import ContactQuery
from app.forms import AddEventForm, EditEventForm, DeleteEventForm, DeleteUserForm, DeleteOrderForm

admin_bp = Blueprint('admin', __name__)

def admin_required():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user = User.query.get(session['user_id'])
    if not user.is_admin:  # Assumes User model has is_admin attribute
        flash('You must be an admin to access this page!', 'danger')
        return redirect(url_for('events.event_list'))
    return None

@admin_bp.route('/dashboard')
def dashboard():
    check = admin_required()
    if check:
        return check
    
    # Stats
    total_events = Event.query.count()
    total_users = User.query.count()
    total_orders = Order.query.count()
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(6).all()
    
    # Event list with delete form
    events = Event.query.all()
    form = DeleteEventForm()
    
    return render_template('admin_dashboard.html', 
                         total_events=total_events, 
                         total_users=total_users, 
                         total_orders=total_orders, 
                         recent_orders=recent_orders, 
                         events=events, 
                         form=form)

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
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)
        
        event = Event(
            name=form.name.data,
            date=form.date.data,
            time=form.time.data,
            location=form.location.data,
            price=form.price.data,
            tickets_available=form.tickets_available.data,
            image_url=image_filename
        )
        db.session.add(event)
        db.session.commit()
        flash('Event added successfully!', 'success')
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
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_path)
            event.image_url = image_filename
        
        db.session.commit()
        flash('Event updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
    return render_template('edit_event.html', form=form, event=event)

@admin_bp.route('/delete_event/<int:event_id>', methods=['POST'])
def delete_event(event_id):
    check = admin_required()
    event = Event.query.get_or_404(event_id)
    
    # Check if there are any orders linked to this event
    if Order.query.filter_by(event_id=event.id).count() > 0:
        flash("Can't delete the event. Because there are few orders with this event.", "warning")
        return redirect(url_for('admin.dashboard'))  # Adjust to your actual redirect path

    try:
        db.session.delete(event)
        db.session.commit()
        flash("Event deleted successfully.", "success")
    except Exception as e:
        db.session.rollback()
        flash("Something went wrong while deleting the event.", "danger")

    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/manage_users')
def manage_users():
    check = admin_required()
    if check:
        return check
    users = User.query.all()
    form = DeleteUserForm()  # Instantiate the form
    return render_template('manage_users.html', users=users, form=form)

@admin_bp.route('/delete_user/<int:user_id>', methods=['POST'])
def delete_user(user_id):
    check = admin_required()
    if check:
        return check
    
    form = DeleteUserForm()
    if form.validate_on_submit():
        user = User.query.get_or_404(user_id)
        if user.id == session['user_id']:  # Prevent self-deletion
            flash('you cant delete your own account.')
            return redirect(url_for('admin.manage_users'))
        db.session.delete(user)
        db.session.commit()
    return redirect(url_for('admin.manage_users'))

@admin_bp.route('/manage_orders')
def manage_orders():
    check = admin_required()
    if check:
        return check
    orders = Order.query.all()
    form = DeleteOrderForm()  # Instantiate the form
    return render_template('manage_orders.html', orders=orders, form=form)

@admin_bp.route('/delete_order/<int:order_id>', methods=['POST'])
def delete_order(order_id):
    check = admin_required()
    if check:
        return check
    
    form = DeleteOrderForm()
    if form.validate_on_submit():
        order = Order.query.get_or_404(order_id)
        try:
            # Update event tickets_available
            if order.event:
                order.event.tickets_available += order.quantity
            db.session.delete(order)
            db.session.commit()
            flash('Order deleted successfully.', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Something went wrong while deleting the order.', 'danger')
    return redirect(url_for('admin.manage_orders'))

@admin_bp.route('/manage_queries')
def manage_queries():
    check = admin_required()
    if check:
        return check
    queries = ContactQuery.query.order_by(ContactQuery.submitted_at.desc()).all()
    return render_template('manage_queries.html', queries=queries)