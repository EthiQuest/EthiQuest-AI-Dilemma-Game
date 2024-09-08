import React, { useState } from 'react';
import Game from './Game';
import Login from './Login';
import Register from './Register';
import Leaderboard from './Leaderboard';
import SubscriptionManager from './SubscriptionManager';
import AdminPanel from './AdminPanel';
import UserStatistics from './UserStatistics';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));
  const [isAdmin, setIsAdmin] = useState(false);
  const [showLeaderboard, setShowLeaderboard] = useState(false);
  const [showSubscription, setShowSubscription] = useState(false);
  const [showAdminPanel, setShowAdminPanel] = useState(false);
  const [showStatistics, setShowStatistics] = useState(false);

  const handleLogin = (newToken, admin = false) => {
    localStorage.setItem('token', newToken);
    setToken(newToken);
    setIsAdmin(admin);
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    setToken(null);
    setIsAdmin(false);
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
          {isAdmin && (
            <button 
              onClick={() => setShowAdminPanel(!showAdminPanel)} 
              className="p-2 bg-purple-500 text-white rounded mr-2"
            >
              {showAdminPanel ? 'Hide Admin Panel' : 'Show Admin Panel'}
            </button>
          )}
          <button 
            onClick={() => {setShowLeaderboard(false); setShowSubscription(!showSubscription); setShowAdminPanel(false); setShowStatistics(false);}} 
            className="p-2 bg-blue-500 text-white rounded mr-2"
          >
            {showSubscription ? 'Hide Subscription' : 'Show Subscription'}
          </button>
          <button 
            onClick={() => {setShowSubscription(false); setShowLeaderboard(!showLeaderboard); setShowAdminPanel(false); setShowStatistics(false);}} 
            className="p-2 bg-green-500 text-white rounded mr-2"
          >
            {showLeaderboard ? 'Hide Leaderboard' : 'Show Leaderboard'}
          </button>
          <button 
            onClick={() => {setShowSubscription(false); setShowLeaderboard(false); setShowAdminPanel(false); setShowStatistics(!showStatistics);}} 
            className="p-2 bg-yellow-500 text-white rounded"
          >
            {showStatistics ? 'Hide Statistics' : 'Show Statistics'}
          </button>
        </div>
      </div>
      {showAdminPanel ? <AdminPanel token={token} /> :
       showSubscription ? <SubscriptionManager token={token} /> : 
       showLeaderboard ? <Leaderboard /> : 
       showStatistics ? <UserStatistics token={token} /> :
       <Game token={token} />}
    </div>
  );
}

export default App;