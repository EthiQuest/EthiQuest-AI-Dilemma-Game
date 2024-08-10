from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import random
from werkzeug.security import generate_password_hash, check_password_hash
from game_data import scenarios
from sqlalchemy import desc

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # Change this!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///game.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

CORS(app)
jwt = JWTManager(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer, default=0)
    current_scenario = db.Column(db.Integer, default=0)

@app.route('/api/register', methods=['POST'])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if not username or not password:
        return jsonify({"msg": "Missing username or password"}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"msg": "Username already exists"}), 400
    user = User(username=username, password=generate_password_hash(password))
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User created successfully"}), 201

@app.route('/api/login', methods=['POST'])
def login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

@app.route('/api/scenario', methods=['GET'])
@jwt_required()
def get_scenario():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    scenario = random.choice(scenarios)
    user.current_scenario = scenario['id']
    db.session.commit()
    return jsonify({
        'id': scenario['id'],
        'scenario': scenario['scenario'],
        'options': [{'text': option['text'], 'id': option['id']} for option in scenario['options']]
    })

@app.route('/api/choice', methods=['POST'])
@jwt_required()
def make_choice():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    data = request.json
    scenario_id = data['scenarioId']
    choice_id = data['choiceId']
    
    scenario = next((s for s in scenarios if s['id'] == scenario_id), None)
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404
    
    chosen_option = next((o for o in scenario['options'] if o['id'] == choice_id), None)
    if not chosen_option:
        return jsonify({'error': 'Invalid choice'}), 400
    
    user.score += chosen_option['score']
    db.session.commit()
    
    return jsonify({
        'consequence': chosen_option['consequence'],
        'score': user.score
    })

@app.route('/api/progress', methods=['GET'])
@jwt_required()
def get_progress():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    return jsonify({
        'score': user.score,
        'current_scenario': user.current_scenario
    })

@app.route('/api/leaderboard', methods=['GET'])
def get_leaderboard():
    top_users = User.query.order_by(desc(User.score)).limit(10).all()
    leaderboard = [{'username': user.username, 'score': user.score} for user in top_users]
    return jsonify(leaderboard)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)