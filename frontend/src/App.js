import React, { useState } from 'react';
import Game from './Game';
import Login from './Login';
import Register from './Register';
import Leaderboard from './Leaderboard';
import SubscriptionManager from './SubscriptionManager';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [showSubscription, setShowSubscription] = useState(false);

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
        <div>
          <button 
            onClick={() => {setShowLeaderboard(false); setShowSubscription(!showSubscription)}} 
            className="p-2 bg-purple-500 text-white rounded mr-2"
          >
            {showSubscription ? 'Hide Subscription' : 'Show Subscription'}
          </button>
          <button 
            onClick={() => {setShowSubscription(false); setShowLeaderboard(!showLeaderboard)}} 
            className="p-2 bg-blue-500 text-white rounded"
          >
            {showLeaderboard ? 'Hide Leaderboard' : 'Show Leaderboard'}
          </button>
        </div>
      </div>
      {showSubscription ? <SubscriptionManager token={token} /> : 
       showLeaderboard ? <Leaderboard /> : 
       <Game token={token} />}
    </div>
  );
}

export default App;