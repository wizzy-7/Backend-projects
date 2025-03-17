from flask import Flask, request, jsonify
from models import Users, Expenses
from config import app, db, jwt
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta


@app.route('/signup', methods=["POST"])
def signup():
    name = request.json.get('name')
    email = request.json.get('email')
    password = request.json.get('password')

    user = Users.query.filter_by(email=email).first()
    if user:
        return jsonify({'message': 'User already exists'}), 400

    if not name:
        return jsonify({'message': 'Name is missing'}), 400

    if not email:
        return jsonify({'message': 'Email is missing'}), 400

    if not password:
        return jsonify({'message': 'Password is required'}), 400

    password_hash = generate_password_hash(password)

    try:
        new_user = Users(name=name, email=email, password_hash=password_hash)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'Registered successfully'}), 201
    except Exception as e:
        return jsonify({'Error': f'{e}'}), 400


@app.route('/signin', methods=["POST"])
def signin():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email:
        return jsonify({'message': 'Email is missing'}), 400

    if not password:
        return jsonify({'message': 'Password is required'}), 400

    user = Users.query.filter_by(email=email).first()
    if user and check_password_hash(user.password_hash, password):
        access_token = create_access_token(identity=str(user.id))
        return jsonify({'token': access_token}), 201

    return jsonify({'message': 'Invalid email or password'}), 401


@app.route('/expenses', methods=['GET', 'POST'])
@jwt_required()
def expenses():
    user_id = get_jwt_identity()
    user = Users.query.get(user_id)

    if not user:
        return jsonify({'message': 'Invalid user'}), 404

    if request.method == "POST":
        data = request.json
        title = data.get("title")
        category = data.get("category")
        amount = data.get("amount")

        if not title or not category or not amount:
            return jsonify({'message': "Please provide 'title', 'category', and 'amount'."}), 400

        try:
            expense = Expenses(title=title, category=category, amount=amount, user_id=user.id)
            db.session.add(expense)
            db.session.commit()
            return jsonify({'message': 'Expense added successfully'}), 201
        except Exception as e:
            return jsonify({'Error': f'{e}'}), 400

    elif request.method == "GET":
        filter_type = request.args.get('filter')
        query = Expenses.query.filter_by(user_id=user.id)

        if filter_type == 'past_week':
            query = query.filter(Expenses.updated_at >= datetime.now() - timedelta(days=7))
        elif filter_type == 'past_month':
            query = query.filter(Expenses.updated_at >= datetime.now() - timedelta(days=30))
        elif filter_type == 'past_3_months':
            query = query.filter(Expenses.updated_at >= datetime.now() - timedelta(days=90))
        elif filter_type == 'custom':
            start_date = request.args.get('start_date')
            end_date = request.args.get('end_date')
            if start_date and end_date:
                query = query.filter(Expenses.updated_at.between(start_date, end_date))

        expenses = query.all()
        json_expenses = [item.to_json() for item in expenses]
        return jsonify(json_expenses)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', debug=True)
