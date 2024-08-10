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

# ==≈=======================
# Models
# ≈=========================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    score = db.Column(db.Integer, default=0)
    scenarios_played = db.Column(db.Integer, default=0)
    ethical_tendency = db.Column(db.Float, default=0)  # Range from -1 (unethical) to 1 (ethical)
    decision_speed = db.Column(db.Float, default=0)  # Average decision time in seconds
    difficulty_preference = db.Column(db.String(20), default='medium')
    category_performance = db.Column(db.JSON, default=lambda: json.dumps({}))

class UserDecision(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scenario_id = db.Column(db.Integer, db.ForeignKey('scenario.id'), nullable=False)
    choice_id = db.Column(db.Integer, nullable=False)
    ethical_impact = db.Column(db.Float, nullable=False)  # Range from -1 to 1
    decision_time = db.Column(db.Float, nullable=False)  # Time taken to make the decision
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Add this new model for scenarios
class Scenario(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    scenario = db.Column(db.String(500), nullable=False)
    difficulty = db.Column(db.String(20), nullable=False)
    options = db.Column(db.JSON, nullable=False)
    is_active = db.Column(db.Boolean, default=True)

# Add this new model for admin users
class AdminUser(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

# ==========================
# Functions and Routes 
# ==========================

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


@app.route('/api/choice', methods=['POST'])
@jwt_required()
def make_choice():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    data = request.json
    scenario_id = data['scenarioId']
    choice_id = data['choiceId']
    decision_time = data['decisionTime']
    
    scenario = Scenario.query.get(scenario_id)
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404
    
    chosen_option = next((o for o in scenario.options if o['id'] == choice_id), None)
    if not chosen_option:
        return jsonify({'error': 'Invalid choice'}), 400
    
    # Calculate ethical impact (this is a simplified example)
    ethical_impact = chosen_option['score'] / 10  # Assuming score ranges from -10 to 10
    
    # Record the user's decision
    user_decision = UserDecision(
        user_id=user.id,
        scenario_id=scenario_id,
        choice_id=choice_id,
        ethical_impact=ethical_impact,
        decision_time=decision_time
    )
    db.session.add(user_decision)
    
    # Update user statistics
    user.score += chosen_option['score']
    user.scenarios_played += 1
    user.ethical_tendency = (user.ethical_tendency * (user.scenarios_played - 1) + ethical_impact) / user.scenarios_played
    user.decision_speed = (user.decision_speed * (user.scenarios_played - 1) + decision_time) / user.scenarios_played
    
    # Update category performance
    category_performance = json.loads(user.category_performance)
    category = scenario.category
    if category not in category_performance:
        category_performance[category] = {'score': 0, 'count': 0}
    category_performance[category]['score'] += chosen_option['score']
    category_performance[category]['count'] += 1
    user.category_performance = json.dumps(category_performance)
    
    db.session.commit()
    
    return jsonify({
        'consequence': chosen_option['consequence'],
        'score': user.score,
        'ethical_impact': ethical_impact
    })

@app.route('/api/user_statistics', methods=['GET'])
@jwt_required()
def get_user_statistics():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    
    category_performance = json.loads(user.category_performance)
    for category in category_performance:
        if category_performance[category]['count'] > 0:
            category_performance[category]['average'] = category_performance[category]['score'] / category_performance[category]['count']
        else:
            category_performance[category]['average'] = 0
    
    return jsonify({
        'username': user.username,
        'score': user.score,
        'scenarios_played': user.scenarios_played,
        'ethical_tendency': user.ethical_tendency,
        'decision_speed': user.decision_speed,
        'difficulty_preference': user.difficulty_preference,
        'category_performance': category_performance
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

# Admin authentication
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    username = request.json.get('username', None)
    password = request.json.get('password', None)
    admin = AdminUser.query.filter_by(username=username).first()
    if admin and admin.password == password:  # In a real app, use proper password hashing
        access_token = create_access_token(identity=username)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401

# CRUD operations for scenarios
@app.route('/api/admin/scenarios', methods=['GET'])
@jwt_required()
def get_all_scenarios():
    scenarios = Scenario.query.all()
    return jsonify([{
        'id': s.id,
        'scenario': s.scenario,
        'difficulty': s.difficulty,
        'options': s.options,
        'is_active': s.is_active
    } for s in scenarios]), 200

@app.route('/api/admin/scenarios', methods=['POST'])
@jwt_required()
def create_scenario():
    data = request.json
    new_scenario = Scenario(
        scenario=data['scenario'],
        difficulty=data['difficulty'],
        options=data['options'],
        is_active=data.get('is_active', True)
    )
    db.session.add(new_scenario)
    db.session.commit()
    return jsonify({
        'id': new_scenario.id,
        'scenario': new_scenario.scenario,
        'difficulty': new_scenario.difficulty,
        'options': new_scenario.options,
        'is_active': new_scenario.is_active
    }), 201

@app.route('/api/admin/scenarios/<int:id>', methods=['PUT'])
@jwt_required()
def update_scenario(id):
    scenario = Scenario.query.get(id)
    if not scenario:
        return jsonify({"msg": "Scenario not found"}), 404
    data = request.json
    scenario.scenario = data.get('scenario', scenario.scenario)
    scenario.difficulty = data.get('difficulty', scenario.difficulty)
    scenario.options = data.get('options', scenario.options)
    scenario.is_active = data.get('is_active', scenario.is_active)
    db.session.commit()
    return jsonify({
        'id': scenario.id,
        'scenario': scenario.scenario,
        'difficulty': scenario.difficulty,
        'options': scenario.options,
        'is_active': scenario.is_active
    }), 200

@app.route('/api/admin/scenarios/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_scenario(id):
    scenario = Scenario.query.get(id)
    if not scenario:
        return jsonify({"msg": "Scenario not found"}), 404
    db.session.delete(scenario)
    db.session.commit()
    return jsonify({"msg": "Scenario deleted"}), 200

# Update the get_scenario route to use the database
@app.route('/api/scenario', methods=['GET'])
@jwt_required()
def get_scenario():
    username = get_jwt_identity()
    user = User.query.filter_by(username=username).first()
    available_scenarios = Scenario.query.filter_by(difficulty=user.preferred_difficulty, is_active=True).all()
    if not available_scenarios:
        available_scenarios = Scenario.query.filter_by(is_active=True).all()
    scenario = random.choice(available_scenarios)
    return jsonify({
        'id': scenario.id,
        'scenario': scenario.scenario,
        'difficulty': scenario.difficulty,
        'options': scenario.options
    })




# Don't forget to create the database tables
@app.before_first_request
def create_tables():
    db.create_all()





if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)