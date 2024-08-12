import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ScenarioDiscussion from './ScenarioDiscussion';

function Game({ token }) {
  const [scenario, setScenario] = useState(null);
  const [result, setResult] = useState(null);
  const [showDiscussion, setShowDiscussion] = useState(false);

  useEffect(() => {
    fetchScenario();
  }, []);

  const fetchScenario = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/scenario', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setScenario(response.data);
      setResult(null);
      setShowDiscussion(false);
    } catch (error) {
      console.error('Error fetching scenario:', error);
    }
  };

  const handleChoice = async (optionId) => {
    try {
      const response = await axios.post('http://localhost:5000/api/choice', {
        scenarioId: scenario.id,
        choiceId: optionId,
        decisionTime: 10 // You might want to actually measure this
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setResult(response.data);
      setShowDiscussion(true);
    } catch (error) {
      console.error('Error submitting choice:', error);
    }
  };

  if (!scenario) {
    return <div>Loading scenario...</div>;
  }

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">AI Ethics Dilemma</h2>
      <p className="mb-4">{scenario.scenario}</p>
      {!result && (
        <div className="space-y-2">
          {scenario.options.map((option) => (
            <button
              key={option.id}
              onClick={() => handleChoice(option.id)}
              className="w-full p-2 bg-blue-500 text-white rounded hover:bg-blue-600"
            >
              {option.text}
            </button>
          ))}
        </div>
      )}
      {result && (
        <div className="mt-4">
          <p className="font-bold">Consequence:</p>
          <p>{result.consequence}</p>
          <p className="mt-2">Points earned: {result.score}</p>
          <p>Ethical impact: {result.ethical_impact.toFixed(2)}</p>
          <button
            onClick={fetchScenario}
            className="mt-4 p-2 bg-green-500 text-white rounded hover:bg-green-600"
          >
            Next Scenario
          </button>
        </div>
      )}
      {showDiscussion && (
        <ScenarioDiscussion token={token} scenarioId={scenario.id} />
      )}
    </div>
  );
}

export default Game;