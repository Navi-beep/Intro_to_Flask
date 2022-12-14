from . import api
from flask import jsonify, request
from app.models import User, Post


@api.route('/')
def index():
    names = ['Brian', 'Tatyana', 'Nate', 'Sam']
    return jsonify(names)


@api.route('/posts', methods=["GET"])
def get_posts():
    posts = Post.query.all()
    return jsonify([p.to_dict() for p in posts])


@api.route('/posts/<post_id>')
def get_post(post_id):
    post = Post.query.get_or_404(post_id)
    return jsonify(post.to_dict())


@api.route('/posts', methods=["POST"])
def create_post():
    if not request.is_json:
        return jsonify({'error': 'Your request content-type must be application/json'}), 400
    # Get the data from the request body
    data = request.json
    print(data, type(data))
    # Validate the data
    for field in ['title', 'body', 'user_id']:
        if field not in data:
            # if field not in request body, respond with a 400 error
            return jsonify({'error': f"'{field}' must be in request body"}), 400
    
    # Get fields from data dict
    title = data.get('title')
    body = data.get('body')
    user_id = data.get('user_id')
    # Create new instance of post with data
    new_post = Post(title=title, body=body, user_id=user_id)
    return jsonify(new_post.to_dict()), 201

@api.route('api/create_user', method=['POST'])
def create_user():
    if not request.is_json:
        return jsonify({'error': 'Your request user-type must be application/json'}), 400
    data = request.json
    print(data)
    for field in ['email', 'username', 'password']:
        if field not in data:
            return jsonify({'error': f"'{field}' must be in request body"}), 400

    email = data.get('email')
    username = data.get('username')
    password = data.get('password')
    new_user = User(email=email, username=username, password=password)
    return jsonify(new_user.to_dict()), 201


@api.route('api/create_user/<id>', method=['GET'])
def get_user():
    users = User.query_all()
    return jsonify([u.to_dict() for u in users])
    
