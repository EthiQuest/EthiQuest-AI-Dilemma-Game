from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from flask_sqlalchemy import SQLAlchemy
import random
from werkzeug.security import generate_password_hash, check_password_hash
from game_data import scenarios
from sqlalchemy import desc
from flask import request

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
    subscription_tier = db.Column(db.String(20), default='free')
    addons = db.Column(db.String(200), default='')  # Store as comma-separated string
    preferred_difficulty = db.Column(db.String(20), default='medium')

# Add this function to the User class
def has_addon(self, addon):
    return addon in self.addons.split(',')

# Add these new routes
@app.route('/api/upgrade', methods=['POST'])
@jwt_required()
def upgrade_subscription():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    new_tier = request.json.get('tier', None)
    if new_tier in ['free', 'premium', 'enterprise']:
        user.subscription_tier = new_tier
        db.session.commit()
        return jsonify({"msg": "Subscription upgraded successfully"}), 200
    return jsonify({"msg": "Invalid subscription tier"}), 400

@app.route('/api/add_addon', methods=['POST'])
@jwt_required()
def add_addon():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    new_addon = request.json.get('addon', None)
    if new_addon:
        addons = user.addons.split(',') if user.addons else []
        if new_addon not in addons:
            addons.append(new_addon)
            user.addons = ','.join(addons)
            db.session.commit()
            return jsonify({"msg": "Add-on added successfully"}), 200
    return jsonify({"msg": "Invalid add-on"}), 400

# Add a new route to set preferred difficulty
@app.route('/api/set_difficulty', methods=['POST'])
@jwt_required()
def set_difficulty():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    new_difficulty = request.json.get('difficulty', None)
    if new_difficulty in ['easy', 'medium', 'hard']:
        user.preferred_difficulty = new_difficulty
        db.session.commit()
        return jsonify({"msg": "Difficulty set successfully"}), 200
    return jsonify({"msg": "Invalid difficulty level"}), 400

# Update the get_scenario route to account for difficulty
@app.route('/api/scenario', methods=['GET'])
@jwt_required()
def get_scenario():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    available_scenarios = [s for s in scenarios if s['difficulty'] == user.preferred_difficulty]
    if not available_scenarios:
        available_scenarios = scenarios  # Fallback to all scenarios if none match the preferred difficulty
    scenario = random.choice(available_scenarios)
    user.current_scenario = scenario['id']
    db.session.commit()
    return jsonify({
        'id': scenario['id'],
        'scenario': scenario['scenario'],
        'difficulty': scenario['difficulty'],
        'options': [{'text': option['text'], 'id': option['id']} for option in scenario['options']]
    })

# Update the make_choice route to adjust scoring based on difficulty
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
    
    # Adjust score based on difficulty
    difficulty_multiplier = {'easy': 0.5, 'medium': 1, 'hard': 1.5}
    adjusted_score = chosen_option['score'] * difficulty_multiplier[scenario['difficulty']]
    
    user.score += adjusted_score
    db.session.commit()
    
    return jsonify({
        'consequence': chosen_option['consequence'],
        'score': user.score,
        'points_earned': adjusted_score
    })





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