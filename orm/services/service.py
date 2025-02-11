from werkzeug.security import generate_password_hash, check_password_hash
from orm.models.model import db, User, Post, Comment

def create_user(username, email, password):
    hashed_password = generate_password_hash(password)
    user = User(username=username, email=email, password=hashed_password)
    db.session.add(user)
    db.session.commit()

def authenticate_user(email, password):
    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        return user
    return None

def get_all_posts():
    return Post.query.order_by(Post.timestamp.desc()).all()

def get_post_by_id(post_id):
    return Post.query.get(post_id)

def create_post(title, content, user_id):
    post = Post(title=title, content=content, user_id=user_id)
    db.session.add(post)
    db.session.commit()

def create_comment(content, post_id, user_id):
    comment = Comment(content=content, post_id=post_id, user_id=user_id)
    db.session.add(comment)
    db.session.commit()
