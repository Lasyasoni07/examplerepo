from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from models.models import Message, User, db
from flask_socketio import emit, join_room, leave_room
from socketio_instance import socketio

chat = Blueprint('chat', __name__)

@chat.route('/')
@login_required
def user_list():
    users = User.query.filter(User.id != current_user.id).all()
    return render_template('user_list.html', username=current_user.username, users=users)

@chat.route('/chat/<int:recipient_id>')
@login_required
def chat_with_user(recipient_id):
    recipient = User.query.get_or_404(recipient_id)
    messages = Message.query.filter(
        ((Message.sender_id == current_user.id) & (Message.recipient_id == recipient.id)) |
        ((Message.sender_id == recipient.id) & (Message.recipient_id == current_user.id))
    ).order_by(Message.timestamp).all()

    room = get_private_room(current_user.id, recipient.id)

    return render_template('chat.html', username=current_user.username, recipient=recipient, room=room, messages=messages)

def get_private_room(user1_id, user2_id):
    return f'private_{min(user1_id, user2_id)}_{max(user1_id, user2_id)}'

@socketio.on('join_private_room')
def handle_join_private_room(data):
    room = data['room']
    join_room(room)
    print(f"User {data['username']} joined private room {room}")

@socketio.on('send_private_message')
def handle_send_private_message(data):
    recipient_id = data['recipient_id']
    room = data['room']
    try:
        if current_user.is_authenticated:
            msg = Message(
                sender_id=current_user.id,
                recipient_id=recipient_id,
                content=data['message']
            )
            db.session.add(msg)
            db.session.commit()

            emit('receive_private_message', {
                'username': current_user.username,
                'message': data['message']
            }, room=room)
            print(f"Message from {current_user.username} to {recipient_id}: {data['message']}")
        else:
            print("User not authenticated")
    except Exception as e:
        print(f"Error in handle_send_private_message: {e}")

@socketio.on('leave_private_room')
def handle_leave_private_room(data):
    room = data['room']
    leave_room(room)
    print(f"User {data['username']} left private room {room}")
