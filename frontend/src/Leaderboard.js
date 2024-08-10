import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Leaderboard() {
  const [leaderboard, setLeaderboard] = useState([]);

  useEffect(() => {
    fetchLeaderboard();
  }, []);

  const fetchLeaderboard = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/leaderboard');
      setLeaderboard(response.data);
    } catch (error) {
      console.error('Error fetching leaderboard:', error);
    }
  };

  return (
    <div className="mt-8">
      <h2 className="text-xl font-bold mb-4">Leaderboard</h2>
      <table className="w-full">
        <thead>
          <tr>
            <th className="text-left">Rank</th>
            <th className="text-left">Username</th>
            <th className="text-left">Score</th>
          </tr>
        </thead>
        <tbody>
          {leaderboard.map((user, index) => (
            <tr key={index} className={index % 2 === 0 ? 'bg-gray-100' : ''}>
              <td className="py-2">{index + 1}</td>
              <td className="py-2">{user.username}</td>
              <td className="py-2">{user.score}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

export default Leaderboard;