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

from app import socketio

@socketio.on('join_room')
def handle_join_room(data):
    print(f"{data['username']} joining room {data['room']}")
    join_room(data['room'])
    emit('status', {
        'msg': f"{data['username']} has joined the room."
    }, room=data['room'])


@socketio.on('send_message')
def handle_send_message(data):
    try:
        print(f"Received message data: {data}")
        if current_user.is_authenticated:
            print(f"User authenticated: {current_user.username}")
            msg = Message(
                room=data['room'],
                user_id=current_user.id,
                username=current_user.username,
                content=data['message']
            )
            db.session.add(msg)
            db.session.commit()
            print("Message saved to database")
            emit('receive_message', {
                'username': data['username'],
                'message': data['message']
            }, room=data['room'])
            print("Message emitted to room")
        else:
            print("User not authenticated")
    except Exception as e:
        print(f"Error in handle_send_message: {e}")

@socketio.on('leave_room')
def handle_leave_room(data):
    leave_room(data['room'])
    emit('status', {
        'msg': f"{data['username']} has left the room."
    }, room=data['room'])
