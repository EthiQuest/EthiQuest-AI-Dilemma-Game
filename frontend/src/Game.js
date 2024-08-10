import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Game({ token }) {
  const [scenario, setScenario] = useState('');
  const [scenarioId, setScenarioId] = useState(null);
  const [options, setOptions] = useState([]);
  const [result, setResult] = useState('');
  const [score, setScore] = useState(0);
  const [difficulty, setDifficulty] = useState('medium');

  useEffect(() => {
    fetchScenario();
  }, [difficulty]);

  const fetchScenario = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/scenario', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setScenario(response.data.scenario);
      setScenarioId(response.data.id);
      setOptions(response.data.options);
      setResult('');
    } catch (error) {
      console.error('Error fetching scenario:', error);
    }
  };

  const handleChoice = async (optionId) => {
    try {
      const response = await axios.post('http://localhost:5000/api/choice', {
        scenarioId: scenarioId,
        choiceId: optionId
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setResult(response.data.consequence);
      setScore(response.data.score);
    } catch (error) {
      console.error('Error submitting choice:', error);
    }
  };

  const handleDifficultyChange = async (newDifficulty) => {
    try {
      await axios.post('http://localhost:5000/api/set_difficulty', {
        difficulty: newDifficulty
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setDifficulty(newDifficulty);
    } catch (error) {
      console.error('Error setting difficulty:', error);
    }
  };

  return (
    <div className='container mx-auto p-4'>
      <h1 className='text-2xl font-bold mb-4'>AI Ethics Dilemma Game</h1>
      <div className='mb-4'>
        <p className='text-xl'>Score: {score}</p>
        <p>Difficulty: {difficulty}</p>
        <select 
          value={difficulty} 
          onChange={(e) => handleDifficultyChange(e.target.value)}
          className='mt-2 p-2 border rounded'
        >
          <option value="easy">Easy</option>
          <option value="medium">Medium</option>
          <option value="hard">Hard</option>
        </select>
      </div>
      <p className='mb-4'>{scenario}</p>
      <div className='space-y-2'>
        {options.map((option) => (
          <button
            key={option.id}
            className='w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600'
            onClick={() => handleChoice(option.id)}
          >
            {option.text}
          </button>
        ))}
      </div>
      {result && (
        <div className='mt-4'>
          <p className='font-bold'>Consequence:</p>
          <p>{result}</p>
          <button
            className='mt-2 p-2 bg-green-500 text-white rounded hover:bg-green-600'
            onClick={fetchScenario}
          >
            Next Scenario
          </button>
        </div>
      )}
    </div>
  );
}

export default Game;