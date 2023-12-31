from datetime import datetime
from flask import current_app
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_login import UserMixin
from simple import db, login_manager


# essintial decorator for the login ext
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    fname = db.Column(db.String(25), nullable=False)
    lname = db.Column(db.String(25), nullable=False)
    username = db.Column(db.String(25), unique=True, nullable=False)
    email = db.Column(db.String(125), unique=True, nullable=False)
    img_file = db.Column(db.String(20), nullable=False, default="default.png")
    password = db.Column(db.String(60), nullable=False)
    lesson = db.relationship("Lesson", backref="author", lazy=True)
    bio = db.Column(db.Text, nullable=True)
    comments = db.relationship("Comment", backref="author", lazy=True)

    def get_reset_token(self):
        s = Serializer(current_app.config["SECRET_KEY"], salt="pw-reset")
        return s.dumps({"user_id": self.id})

    @staticmethod
    def verify_reset_token(token, age=3600):
        s = Serializer(current_app.config["SECRET_KEY"], salt="pw-reset")
        try:
            user_id = s.loads(token, max_age=age)["user_id"]
        except :
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"'{self.id}','{self.fname}','{self.lname}','{self.username}','{self.email}','{self.img_file}'"


class Lesson(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    thumbnail = db.Column(db.String(20), nullable=False, default="default_lesson.png")
    slug = db.Column(db.String(32), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
    comments = db.relationship("Comment", backref="lesson", lazy=True)

    def __repr__(self):
        return f"'{self.id}','{self.title}','{self.date_posted}','{self.content}','{self.thumbnail}','{self.slug}'"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.String(150), nullable=False)
    icon = db.Column(db.String(20), nullable=False, default="default_icon.png")
    lessons = db.relationship("Lesson", backref="course_name", lazy=True)

    def __repr__(self):
        return f"'{self.id}','{self.title}','{self.description}','{self.icon}'"
    
    
class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    lesson_id = db.Column(db.Integer, db.ForeignKey("lesson.id"), nullable=False)
    user_img_file = db.Column(db.String(20), nullable=False)
    user_name = db.Column(db.String(68), nullable=True)
    def __repr__(self):
        return f"'{self.id}', '{self.text}', '{self.date_posted}', '{self.user_img_file}'"

    