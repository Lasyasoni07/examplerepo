from flask import Blueprint, request, jsonify, render_template
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import User, TodoItem
from app import db
from app.decorators import role_required

todo_bp = Blueprint('todo', __name__)

@todo_bp.route('/todo', methods=['POST'])
@jwt_required()
def create_todo():
    current_user = get_jwt_identity()
    user_id = current_user['id']
    data = request.get_json()
    new_todo = TodoItem(task=data['task'], completed=False, user_id=user_id)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo item created successfully'}), 201

@todo_bp.route('/todo', methods=['GET'])
@jwt_required()
def get_todos():
    current_user = get_jwt_identity()
    user_id = current_user['id']
    todos = TodoItem.query.filter_by(user_id=user_id).all()
    result = [{'id': todo.id, 'task': todo.task, 'completed': todo.completed} for todo in todos]
    print('Fetched todos:', result)
    return jsonify(result), 200

@todo_bp.route('/todo/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo_status(id):
    current_user = get_jwt_identity()
    user_id = current_user['id']
    data = request.get_json()
    todo = TodoItem.query.filter_by(id=id, user_id=user_id).first()
    if not todo:
        return jsonify({'message': 'Todo item not found'}), 404
    todo.task = data.get('task', todo.task)
    todo.completed = data.get('completed', todo.completed)
    db.session.commit()
    return jsonify({'message': 'Todo item updated successfully'}), 200

@todo_bp.route('/todo/<int:id>', methods=['DELETE'])
@jwt_required()
@role_required('admin')
def delete_todo_item(id):
    todo = TodoItem.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo item deleted successfully'}), 200


@todo_bp.route('/todo-page', methods=['GET'])
def todo_page():
    return render_template('todo.html')
