from back import create_app, db
from back.models.user_model import User
from back.models.todo_model import TodoItem

app = create_app()

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
