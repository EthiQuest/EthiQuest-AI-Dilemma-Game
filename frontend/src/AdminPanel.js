import React, { useState, useEffect } from 'react';
import axios from 'axios';

function AdminPanel({ token }) {
  const [scenarios, setScenarios] = useState([]);
  const [newScenario, setNewScenario] = useState({
    scenario: '',
    difficulty: 'medium',
    options: [{ text: '', consequence: '', score: 0 }],
    is_active: true
  });

  useEffect(() => {
    fetchScenarios();
  }, []);

  const fetchScenarios = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/admin/scenarios', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setScenarios(response.data);
    } catch (error) {
      console.error('Error fetching scenarios:', error);
    }
  };

  const handleCreateScenario = async () => {
    try {
      await axios.post('http://localhost:5000/api/admin/scenarios', newScenario, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchScenarios();
      setNewScenario({
        scenario: '',
        difficulty: 'medium',
        options: [{ text: '', consequence: '', score: 0 }],
        is_active: true
      });
    } catch (error) {
      console.error('Error creating scenario:', error);
    }
  };

  const handleUpdateScenario = async (id, updatedScenario) => {
    try {
      await axios.put(`http://localhost:5000/api/admin/scenarios/${id}`, updatedScenario, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchScenarios();
    } catch (error) {
      console.error('Error updating scenario:', error);
    }
  };

  const handleDeleteScenario = async (id) => {
    try {
      await axios.delete(`http://localhost:5000/api/admin/scenarios/${id}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchScenarios();
    } catch (error) {
      console.error('Error deleting scenario:', error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Admin Panel</h1>
      
      {/* Create new scenario form */}
      <div className="mb-8 p-4 border rounded">
        <h2 className="text-xl font-bold mb-2">Create New Scenario</h2>
        <input
          type="text"
          placeholder="Scenario"
          value={newScenario.scenario}
          onChange={(e) => setNewScenario({...newScenario, scenario: e.target.value})}
          className="w-full p-2 mb-2 border rounded"
        />
        <select
          value={newScenario.difficulty}
          onChange={(e) => setNewScenario({...newScenario, difficulty: e.target.value})}
          className="w-full p-2 mb-2 border rounded"
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
        {/* Add more inputs for options */}
        <button onClick={handleCreateScenario} className="p-2 bg-green-500 text-white rounded">
          Create Scenario
        </button>
      </div>

      {/* List of existing scenarios */}
      <div>
        <h2 className="text-xl font-bold mb-2">Existing Scenarios</h2>
        {scenarios.map((scenario) => (
          <div key={scenario.id} className="mb-4 p-4 border rounded">
            <p><strong>Scenario:</strong> {scenario.scenario}</p>
            <p><strong>Difficulty:</strong> {scenario.difficulty}</p>
            <p><strong>Active:</strong> {scenario.is_active ? 'Yes' : 'No'}</p>
            <button onClick={() => handleDeleteScenario(scenario.id)} className="p-2 bg-red-500 text-white rounded mt-2">
              Delete
            </button>
            {/* Add edit functionality here */}
          </div>
        ))}
      </div>
    </div>
  );
}

export default AdminPanel;