from extensions import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200))


class ToDoItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    description = db.Column(db.String(255))
    status = db.Column(db.String(20), default="To Do")  # Default status to "To Do"
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
