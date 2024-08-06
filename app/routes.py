from flask import Blueprint, request, jsonify
from .models import db, User, Post
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


bp = Blueprint("routes", __name__)


@bp.route("/register", methods=["POST"])
def register():
    body = request.json
    username = body.get("username", None)
    password = body.get("password", None)
    name = body.get("name", None)
    surname = body.get("surname", None)
    avatar = body.get("avatar", "https://i.pravatar.cc/300")

    if username is None:
        return jsonify({"error": "Username is required"}), 400

    if password is None:
        return jsonify({"error": "password is required"}), 400

    if name is None:
        return jsonify({"error": "name is required"}), 400

    if surname is None:
        return jsonify({"error": "surname is required"}), 400

    hashed_password = generate_password_hash(password)
    new_user = User(
        avatar=avatar,
        username=username,
        password=hashed_password,
        name=name,
        surname=surname,
    )
    db.session.add(new_user)

    try:
        db.session.commit()
        return jsonify({"ok": True, "data": "user created"}), 201
    except Exception as error:
        db.session.rollback()
        print(f"Error: {error}")
        return (
            jsonify({"ok": False, "error": "Internal server error", "status": 500}),
            500,
        )


@bp.route("/", methods=["GET"])
def hello():
    return "route works"


@bp.route("/login", methods=["POST"])
def login():
    body = request.json
    username = body.get("username", None)
    password = body.get("password", None)
    if username is None or password is None:
        return jsonify({"error": "username and password is required"}), 400

    user = User.query.filter_by(username=username).one_or_none()
    if user is None:
        return jsonify({"ok": False, "error": "username does not exist"}), 404
    pass_match = check_password_hash(user.password, password)
    if not pass_match:
        return jsonify({"ok": False, "error": "invalid password"}), 401

    auth_token = create_access_token({"username": user.username, "id": user.id})
    return jsonify({"ok": True, "auth_token": auth_token}), 200


@bp.route("/posts", methods=["GET"])
@jwt_required()
def get_posts():

    user_id = request.args.get("user_id")

    if user_id is None:
        return jsonify({"error": "user_id is required"}), 400

    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    posts = (
        Post.query.filter_by(author_id=user.id).order_by(Post.created_at.desc()).all()
    )

    return (
        jsonify([post.to_dict() for post in posts]),
        200,
    )


@bp.route("/posts", methods=["POST"])
@jwt_required()
def create_post():
    data = request.get_json()
    user = User.query.get(data["author_id"])
    new_post = Post(
        image=data["image"],
        message=data["message"],
        author=user,
        location=data["location"],
        status=data["status"],
    )
    db.session.add(new_post)
    db.session.commit()
    return (jsonify(new_post.to_dict()), 201, {"ok": True})


@bp.route("/like/<int:post_id>", methods=["POST"])
@jwt_required()
def like_post(post_id):
    data = request.get_json()
    user = User.query.get(data["user_id"])
    post = Post.query.get(post_id)
    if user in post.likes:
        message = "Post already liked"
    else:
        post.likes.append(user)
        message = "Post liked"
    db.session.commit()
    return jsonify({"message": message}), 200


@bp.route("/user", methods=["GET"])
@jwt_required()
def get_current_user():
    current_user = get_jwt_identity()
    user = User.query.get(current_user["id"])

    if not user:
        return jsonify({"error": "User not found"}), 404

    return (
        jsonify(
            {
                "user": user.to_dict(),
                "ok": True,
            }
        ),
        200,
    )


@bp.route("/posts/<int:post_id>", methods=["DELETE"])
@jwt_required()
def delete_post(post_id):
    post = Post.query.get(post_id)
    if not post:
        return jsonify({"error": "Post not found"}), 404

    db.session.delete(post)
    db.session.commit()
    return jsonify({"message": "Post deleted successfully"}), 200
