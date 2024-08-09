import React, { useState } from 'react';
import Game from './Game';
import Login from './Login';
import Register from './Register';

function App() {
  const [token, setToken] = useState(localStorage.getItem('token'));

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
      </div>
    );
  }

  return (
    <div className="container mx-auto p-4">
      <button onClick={handleLogout} className="mb-4 p-2 bg-red-500 text-white rounded">Logout</button>
      <Game token={token} />
    </div>
  );
}

export default App;