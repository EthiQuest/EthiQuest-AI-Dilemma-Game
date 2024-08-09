from flask import Flask, jsonify, request
from flask_cors import CORS
import random
from game_data import scenarios

app = Flask(__name__)
CORS(app)

@app.route('/api/scenario', methods=['GET'])
def get_scenario():
    scenario = random.choice(scenarios)
    return jsonify({
        'id': scenario['id'],
        'scenario': scenario['scenario'],
        'options': [option['text'] for option in scenario['options']]
    })

@app.route('/api/choice', methods=['POST'])
def make_choice():
    data = request.json
    scenario_id = data['scenarioId']
    choice = data['choice']
    
    scenario = next((s for s in scenarios if s['id'] == scenario_id), None)
    if not scenario:
        return jsonify({'error': 'Scenario not found'}), 404
    
    chosen_option = next((o for o in scenario['options'] if o['text'] == choice), None)
    if not chosen_option:
        return jsonify({'error': 'Invalid choice'}), 400
    
    return jsonify({
        'consequence': chosen_option['consequence']
    })

if __name__ == '__main__':
    app.run(debug=True)