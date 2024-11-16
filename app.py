from flask import Flask, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from dotenv import load_dotenv
import os

# Import the extensions and models
from extensions import db, jwt, bcrypt

from model import User, ToDoItem

# Load environment variables from .env file
load_dotenv()


def create_app():
    app = Flask(__name__)

    # Configure app with values from environment variables
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
    app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Create tables
    with app.app_context():
        db.create_all()

    return app


app = create_app()


@app.route('/')
def home():
    return "Welcome to the To-Do API!"


@app.route('/register', methods=['POST'])
def register():
    data = request.json
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(name=data['name'], email=data['email'], password=hashed_password)
    db.session.add(user)
    db.session.commit()
    token = create_access_token(identity=user.id)
    return jsonify({"token": token}), 201


@app.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        token = create_access_token(identity=user.id)
        return jsonify({"token": token}), 200
    return jsonify({"message": "Invalid credentials"}), 401


@app.route('/todos', methods=['POST'])
@jwt_required()
def create_todo():
    user_id = get_jwt_identity()
    data = request.json
    todo = ToDoItem(
        title=data['title'],
        description=data.get('description'),
        status="To Do",  # Set default status to "To Do"
        user_id=user_id
    )
    db.session.add(todo)
    db.session.commit()
    return jsonify({
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "status": todo.status
    }), 201


@app.route('/todos', methods=['GET'])
@jwt_required()
def get_todos():
    user_id = get_jwt_identity()
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    todos = ToDoItem.query.filter_by(user_id=user_id).paginate(page=page, per_page=limit)
    return jsonify({
        "data": [{"id": t.id, "title": t.title, "description": t.description, "status": t.status} for t in todos.items],
        "page": todos.page,
        "limit": todos.per_page,
        "total": todos.total
    })


@app.route('/todos/<int:id>', methods=['PUT'])
@jwt_required()
def update_todo(id):
    user_id = get_jwt_identity()
    todo = ToDoItem.query.get(id)
    if not todo:
        return jsonify({"message": "To-Do item not found"}), 404
    if todo.user_id != user_id:
        return jsonify({"message": "You do not have permission to edit this To-Do item"}), 403

    data = request.json
    todo.title = data.get('title', todo.title)
    todo.description = data.get('description', todo.description)
    todo.status = data.get('status', todo.status)  # Update status if provided
    db.session.commit()

    return jsonify({
        "id": todo.id,
        "title": todo.title,
        "description": todo.description,
        "status": todo.status
    }), 200


@app.route('/todos/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_todo(id):
    user_id = get_jwt_identity()
    todo = ToDoItem.query.get(id)
    if not todo:
        return jsonify({"message": "To-Do item not found"}), 404
    if todo.user_id != user_id:
        return jsonify({"message": "You do not have permission to delete this To-Do item"}), 403

    db.session.delete(todo)
    db.session.commit()

    return jsonify({"message": "To-Do item deleted successfully"}), 200


if __name__ == '__main__':
    app.run(debug=True)
