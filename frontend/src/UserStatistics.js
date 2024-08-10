import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line, Bar } from 'react-chartjs-2';
import { Chart as ChartJS, CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend } from 'chart.js';

ChartJS.register(CategoryScale, LinearScale, PointElement, LineElement, BarElement, Title, Tooltip, Legend);

function UserStatistics({ token }) {
  const [statistics, setStatistics] = useState(null);

  useEffect(() => {
    fetchStatistics();
  }, []);

  const fetchStatistics = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/user_statistics', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setStatistics(response.data);
    } catch (error) {
      console.error('Error fetching user statistics:', error);
    }
  };

  if (!statistics) {
    return <div>Loading statistics...</div>;
  }

  const ethicalTendencyData = {
    labels: ['Unethical', 'Neutral', 'Ethical'],
    datasets: [
      {
        label: 'Your Ethical Tendency',
        data: [0, 0, 0],
        backgroundColor: 'rgba(75, 192, 192, 0.6)',
      },
    ],
  };
  ethicalTendencyData.datasets[0].data[Math.floor((statistics.ethical_tendency + 1) * 1.5)] = 1;

  const categoryPerformanceData = {
    labels: Object.keys(statistics.category_performance),
    datasets: [
      {
        label: 'Average Score',
        data: Object.values(statistics.category_performance).map(cat => cat.average),
        backgroundColor: 'rgba(54, 162, 235, 0.6)',
      },
    ],
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Your Game Statistics</h2>
      <div className="grid grid-cols-2 gap-4 mb-8">
        <div>
          <p><strong>Total Score:</strong> {statistics.score}</p>
          <p><strong>Scenarios Played:</strong> {statistics.scenarios_played}</p>
          <p><strong>Average Decision Speed:</strong> {statistics.decision_speed.toFixed(2)} seconds</p>
          <p><strong>Preferred Difficulty:</strong> {statistics.difficulty_preference}</p>
        </div>
        <div>
          <h3 className="text-xl font-bold mb-2">Ethical Tendency</h3>
          <Bar data={ethicalTendencyData} options={{ indexAxis: 'y', scales: { x: { max: 1 } } }} />
        </div>
      </div>
      <div>
        <h3 className="text-xl font-bold mb-2">Category Performance</h3>
        <Bar data={categoryPerformanceData} />
      </div>
    </div>
  );
}

export default UserStatistics;