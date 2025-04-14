# backend/app/controllers/events.py
from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from app import db
from app.models.event import Event
from app.models.cart import Cart
from app.models.order import Order
from app.models.user import User
from app.forms import BuyTicketForm, UpdateCartForm

events_bp = Blueprint('events', __name__)

@events_bp.route('/events')
def event_list():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    events = Event.query.all()
    form = BuyTicketForm()
    return render_template('events.html', events=events, form=form)

@events_bp.route('/add_to_cart/<int:event_id>', methods=['POST'])
def add_to_cart(event_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    form = BuyTicketForm()
    if form.validate_on_submit():
        event = Event.query.get_or_404(event_id)
        if event.tickets_available < 1: 
            flash('No tickets available.')
            return redirect(url_for('events.event_list'))
        cart_item = Cart.query.filter_by(user_id=session['user_id'], event_id=event_id).first()
        if cart_item:
            if cart_item.quantity + 1 > event.tickets_available:
                flash('Not enough tickets available to add more.')
            else:
                cart_item.quantity += 1 
        else:
            cart_item = Cart(user_id=session['user_id'], event_id=event_id, quantity=1) 
            db.session.add(cart_item)
        db.session.commit()
        flash('Added to cart!')
    return redirect(url_for('events.event_list'))

@events_bp.route('/cart')
def view_cart():
    if 'user_id' not in session:
        flash('Please log in to view your cart.')
        return redirect(url_for('auth.login'))
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    form = UpdateCartForm()
    total = sum(item.event.price * item.quantity for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, form=form, total=total)

@events_bp.route('/update_cart/<int:cart_id>', methods=['POST'])
def update_cart(cart_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != session['user_id']:
        flash('You can only update your own cart!')
        return redirect(url_for('events.view_cart'))

    form = UpdateCartForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        event = Event.query.get(cart_item.event_id)

        if quantity == 0:
            db.session.delete(cart_item)
            flash('Item removed from cart!')
        elif quantity > event.tickets_available:
            flash('Not enough tickets available!')
        else:
            cart_item.quantity = quantity
            flash('Cart updated!')

        db.session.commit()
    return redirect(url_for('events.view_cart'))

@events_bp.route('/remove_from_cart/<int:cart_id>')
def remove_from_cart(cart_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    cart_item = Cart.query.get_or_404(cart_id)
    if cart_item.user_id != session['user_id']:
        flash('Unauthorized action.')
        return redirect(url_for('events.view_cart'))
    db.session.delete(cart_item)
    db.session.commit()
    flash('Item removed from cart.')
    return redirect(url_for('events.view_cart'))

@events_bp.route('/place_order', methods=['POST'])
def place_order():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    user_id = session['user_id']
    cart_items = Cart.query.filter_by(user_id=user_id).all()

    if not cart_items:
        flash('Your cart is empty!')
        return redirect(url_for('events.view_cart'))

    orders = []
    total_amount = 0
    for item in cart_items:
        event = Event.query.get(item.event_id)
        if item.quantity > event.tickets_available:
            flash(f'Not enough tickets left for {event.name}!')
            return redirect(url_for('events.view_cart'))

        event.tickets_available -= item.quantity
        subtotal = event.price * item.quantity
        total_amount += subtotal

        order = Order(
            user_id=user_id,
            event_id=event.id,
            quantity=item.quantity,
            total_amount=subtotal
        )
        orders.append(order)
        db.session.delete(item)

    db.session.add_all(orders)
    db.session.commit()

    user = User.query.get(user_id)
    flash('Order placed successfully!')
    return render_template('order_confirmation.html', orders=orders, total_amount=total_amount, user=user)

@events_bp.route('/order_history')
def order_history():
    if 'user_id' not in session:
        flash('Please log in to view your order history.', 'danger')
        return redirect(url_for('auth.login'))
    orders = Order.query.filter_by(user_id=session['user_id']).all()
    return render_template('order_history.html', orders=orders)

@events_bp.route('/checkout')
def checkout():
    if 'user_id' not in session:
        flash('Please log in to checkout.', 'danger')
        return redirect(url_for('auth.login'))
    
    cart_items = Cart.query.filter_by(user_id=session['user_id']).all()
    if not cart_items:
        flash('Your cart is empty.', 'danger')
        return redirect(url_for('events.view_cart'))
    
    try:
        order_ids = []
        for item in cart_items:
            event = Event.query.get(item.event_id)
            if event.tickets_available < item.quantity:
                flash(f'Not enough tickets for {event.name}.', 'danger')
                return redirect(url_for('events.view_cart'))
            event.tickets_available -= item.quantity
            total_amount = event.price * item.quantity
            order = Order(
                user_id=item.user_id,
                event_id=item.event_id,
                quantity=item.quantity,
                total_amount=total_amount
            )
            db.session.add(order)
            db.session.flush()
            order_ids.append(order.id)
            db.session.delete(item)
        db.session.commit()
        flash('Order placed successfully!', 'success')
        return redirect(url_for('events.order_success', order_ids=','.join(map(str, order_ids))))
    except Exception as e:
        db.session.rollback()
        flash(f'Checkout failed: {str(e)}', 'danger')
        return redirect(url_for('events.view_cart'))

@events_bp.route('/order_success')
def order_success():
    if 'user_id' not in session:
        flash('Please log in to view your order.', 'danger')
        return redirect(url_for('auth.login'))
    order_ids = request.args.get('order_ids', '').split(',')
    order_ids = [int(id) for id in order_ids if id.isdigit()]
    orders = Order.query.filter(Order.id.in_(order_ids), Order.user_id == session['user_id']).all()
    return render_template('order_success.html', orders=orders)