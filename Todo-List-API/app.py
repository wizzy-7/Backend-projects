from flask import request, redirect, jsonify, make_response
from config import app, db, generate_token
from werkzeug.security import generate_password_hash, check_password_hash
from models import User, TodoList
from functools import wraps


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        print('Token recieved:', auth_header)
        if not auth_header:
            return jsonify({'message': 'Unauthorized.'})
        
        try:
            parts = auth_header.split(" ")
            if len(parts) != 2:
                return jsonify({'message': 'Token is invalid.'}), 401
            
            token = parts[1]   
            
            user = User.query.filter_by(token=token).first()
            print('Decoded user:', user)
            
            if not user:
                return jsonify({'message': 'Invalid token'})
            
        except Exception as e:
            return jsonify({'error': f'{e}'})
        
        if user is None:
            print("User is None!")
            return jsonify({"error": "User authentication failed"}), 401

        
        print('Token verification successful')
        return f(user=user, *args, **kwargs)
    return decorated


@app.route('/')
def index():
    return redirect('/register')


@app.route('/register', methods=["GET", 'POST'])
def register():
    if request.method == "POST":
        name = request.json.get('name')
        email = request.json.get('email')
        password = request.json.get('password')
        
        if not name:
            return jsonify({'message': 'Name required'})
        if not email:
            return jsonify({'message': 'Email required'})
        if not password:
            return jsonify({'message': 'Password required'})
        
        hash = generate_password_hash(password=password, method='scrypt', salt_length=16, )
        
        
        token = generate_token()
        try:
            new_user = User(name=name, email=email, hash=hash, token=token)
            new_user.token = token
            db.session.add(new_user)
            db.session.commit()
            return jsonify({'token': token})
        except Exception as e:
            return jsonify({'message': f'Registration failed: {e}'})
        
    else:
        return jsonify({'message': 'Please use POST to access registration'})
        

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')
        
        if not email:
            return jsonify({'message': 'Email required'})
        if not password:
            return jsonify({'message': 'Input password'})
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.hash, password):
            response = make_response(jsonify({'message': 'Success', 'token': user.token}))
            response.headers["Authorization"] = f'Token {user.token}'
            return response
        

        else:
            return jsonify({'message': 'Invalid email/password'})
        
    else:
        return jsonify({'message': 'Please use POST to access login'})
    

@app.route('/todos', methods=["GET", "POST"])
@token_required
def todos(user):
    if request.method == "POST":
        title = request.json.get('title')
        description = request.json.get('description')
        
        if not title:
            return jsonify({'message': 'Title is required'}), 400
        
        todo = TodoList(title=title, description=description, user_id=user.id)
        
        try:
            db.session.add(todo)
            db.session.commit()
            todo_json = todo.to_json()
            
            return jsonify(todo_json), 201
        except Exception as e:
            return jsonify({'message': f'{e}'}), 500
        
    elif request.method == 'GET':
        print('show todo list')
        page = request.args.get('page', 1, type=int)
        limit = request.args.get('limit', 10, type=int)
        
        todos = TodoList.query.filter_by(user_id=user.id).paginate(page=page, per_page=limit)
        todo_list = list(map(lambda x: x.to_json(), todos.items))
        
        response = {
            'data': todo_list,
            'page': todos.pages,
            'limit': limit,
            'total': todos.total,
        }
        
        print(response)
        
        return jsonify(response)
    

@app.route('/todos/<int:id>', methods=["PUT"])
@token_required
def update_item(user, id):
    title = request.json.get('title')
    description = request.json.get('description')
    
    todo = TodoList.query.filter_by(id=id, user_id=user.id).first()
    
    if not todo:
        return jsonify({'message': 'Todo item not found'}), 404
    
    if title:
        todo.title = title
    if description:
        todo.description = description
        
    try:
        db.session.commit()
        return jsonify(todo.to_json()), 204
    
    except Exception as e:
        return jsonify({'message': 'Forbidden'}), 403
    

@app.route('/todos/<int:id>', methods=["DELETE"])
@token_required
def delete_item(user, id):
    todo = TodoList.query.filter_by(id=id, user_id=user.id).first()
    
    if not todo:
        return jsonify({'message': 'Todo item not found'}), 404
    
    try:
        db.session.delete(todo)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({'message': f'Operation failed: {e}'}), 500
    
        
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
        
        
