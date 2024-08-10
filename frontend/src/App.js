import React, { useState } from 'react';
import Game from './Game';
import Login from './Login';
import Register from './Register';
import Leaderboard from './Leaderboard';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [showLeaderboard, setShowLeaderboard] = useState(false);

  const handleLogin = (newToken) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
  };

  if (!token) {
    return (
      <div className="container mx-auto p-4">
        <h1 className="text-2xl font-bold mb-4">AI Ethics Dilemma Game</h1>
        <Login onLogin={handleLogin} />
        <Register />
        <Leaderboard />
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <div className="flex justify-between items-center mb-4">
        <button onClick={handleLogout} className="p-2 bg-red-500 text-white rounded">Logout</button>
        <button 
          onClick={() => setShowLeaderboard(!showLeaderboard)} 
          className="p-2 bg-blue-500 text-white rounded"
        >
          {showLeaderboard ? 'Hide Leaderboard' : 'Show Leaderboard'}
        </button>
      </div>
      {showLeaderboard ? <Leaderboard /> : <Game token={token} />}
    </div>
  );
}

export default App;