import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Game() {
  const [scenario, setScenario] = useState('');
  const [scenarioId, setScenarioId] = useState(null);
  const [options, setOptions] = useState([]);
  const [result, setResult] = useState('');

  useEffect(() => {
    fetchScenario();
  }, []);

  const fetchScenario = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/scenario');
      setScenario(response.data.scenario);
      setScenarioId(response.data.id);
      setOptions(response.data.options);
      setResult('');
    } catch (error) {
      console.error('Error fetching scenario:', error);
    }
  };

  const handleChoice = async (option) => {
    try {
      const response = await axios.post('http://localhost:5000/api/choice', {
        scenarioId: scenarioId,
        choice: option
      });
      setResult(response.data.consequence);
    } catch (error) {
      console.error('Error submitting choice:', error);
    }
  };

  return (
    <div className='container mx-auto p-4'>
      <h1 className='text-2xl font-bold mb-4'>AI Ethics Dilemma Game</h1>
      <p className='mb-4'>{scenario}</p>
      <div className='space-y-2'>
        {options.map((option, index) => (
          <button
            key={index}
            className='w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600'
            onClick={() => handleChoice(option)}
          >
            {option}
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