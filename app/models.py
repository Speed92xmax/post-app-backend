from . import db
from datetime import datetime


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(255), nullable=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(20), nullable=False)
    surname = db.Column(db.String(20), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "avatar": self.avatar,
            "username": self.username,
            "name": self.name,
            "surname": self.surname,
            "posts": [post.to_dict() for post in self.posts],
        }


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    image = db.Column(db.String(255), nullable=False)
    message = db.Column(db.String(500), nullable=False)
    likes = db.relationship(
        "User",
        secondary="post_likes",
        lazy="subquery",
        backref=db.backref("liked_posts", lazy=True),
    )
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    location = db.Column(db.String(30), nullable=False)
    status = db.Column(db.String(10), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "image": self.image,
            "message": self.message,
            "likes": [like.username for like in self.likes],
            "author_id": self.author_id,
            "created_at": self.created_at.isoformat(),
            "location": self.location,
            "status": self.status,
        }


post_likes = db.Table(
    "post_likes",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("post_id", db.Integer, db.ForeignKey("post.id"), primary_key=True),
)
