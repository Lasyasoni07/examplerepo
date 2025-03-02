from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from models.models import Message, db
from flask_socketio import emit, join_room, leave_room

chat = Blueprint('chat', __name__)

@chat.route('/')
@login_required
def chat_rooms():
    return render_template('index.html', username=current_user.username)

@chat.route('/chat/<room>')
@login_required
def chat_room(room):
    messages = Message.query.filter_by(room=room).order_by(Message.timestamp).all()
    return render_template('chat.html', username=current_user.username, room=room, messages=messages)

# SocketIO Events
from app import socketio

@socketio.on('join_room')
def handle_join_room(data):
    join_room(data['room'])
    emit('status', {
        'msg': f"{data['username']} has joined the room."
    }, room=data['room'])

@socketio.on('send_message')
def handle_send_message(data):
    msg = Message(
        room=data['room'],
        user_id=current_user.id,
        username=current_user.username,
        content=data['message']
    )
    db.session.add(msg)
    db.session.commit()
    emit('receive_message', {
        'username': data['username'],
        'message': data['message']
    }, room=data['room'])

@socketio.on('leave_room')
def handle_leave_room(data):
    leave_room(data['room'])
    emit('status', {
        'msg': f"{data['username']} has left the room."
    }, room=data['room'])
