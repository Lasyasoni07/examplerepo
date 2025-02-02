from flask import Blueprint, request, jsonify, render_template, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from back.models.todo_model import TodoItem
from back import db
from flask_jwt_extended import jwt_required, get_jwt_identity
from back import csrf

todo_bp = Blueprint('todo_bp', __name__)

@todo_bp.route('/todo', methods=['POST'])
@csrf.exempt
@jwt_required()
def create_todo():
    user_id = get_jwt_identity()
    data = request.get_json()
    new_todo = TodoItem(task=data['task'], completed=False, user_id=user_id)
    db.session.add(new_todo)
    db.session.commit()
    return jsonify({'message': 'Todo item created successfully'}), 201

@todo_bp.route('/todo', methods=['GET'])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    todos = TodoItem.query.filter_by(user_id=user_id).all()
    result = [{'id': todo.id, 'task': todo.task, 'completed': todo.completed} for todo in todos]
    return jsonify(result), 200


@todo_bp.route('/todo/<int:id>', methods=['PUT'])
@csrf.exempt  # Exempt this route if using Option 1 from earlier
@jwt_required()
def update_todo_status(id):
    user_id = get_jwt_identity()
    data = request.get_json()
    todo = TodoItem.query.filter_by(id=id, user_id=user_id).first()
    if not todo:
        return jsonify({'message': 'Todo item not found'}), 404
    todo.completed = data.get('completed', todo.completed)
    db.session.commit()
    return jsonify({'message': 'Todo item updated successfully'}), 200

@todo_bp.route('/todo/<int:id>', methods=['DELETE'])
@csrf.exempt  # Exempt this route as well
@jwt_required()
def delete_todo(id):
    user_id = get_jwt_identity()
    todo = TodoItem.query.filter_by(id=id, user_id=user_id).first()
    if not todo:
        return jsonify({'message': 'Todo item not found'}), 404
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'message': 'Todo item deleted successfully'}), 200

@todo_bp.route('/todo-page', methods=['GET'])
def todo_page():
    return render_template('todo.html')


