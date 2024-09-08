import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { Line, Bar } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend,
} from 'chart.js';

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  BarElement,
  Title,
  Tooltip,
  Legend
);

function PremiumFeatures({ token }) {
  const [analytics, setAnalytics] = useState(null);
  const [exclusiveScenarios, setExclusiveScenarios] = useState([]);

  useEffect(() => {
    fetchAdvancedAnalytics();
    fetchExclusiveScenarios();
  }, []);

  const fetchAdvancedAnalytics = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/advanced-analytics', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAnalytics(response.data);
    } catch (error) {
      console.error('Error fetching advanced analytics:', error);
    }
  };

  const fetchExclusiveScenarios = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/exclusive-scenarios', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setExclusiveScenarios(response.data);
    } catch (error) {
      console.error('Error fetching exclusive scenarios:', error);
    }
  };

  if (!analytics) {
    return <div>Loading premium features...</div>;
  }

  const timeTrendData = {
    labels: analytics.time_trend.map(tt => tt.date),
    datasets: [
      {
        label: 'Average Score Over Time',
        data: analytics.time_trend.map(tt => tt.avg_score),
        borderColor: 'rgb(75, 192, 192)',
        tension: 0.1
      }
    ]
  };

  const categoryPerformanceData = {
    labels: analytics.category_performance.map(cp => cp.category),
    datasets: [
      {
        label: 'Average Score by Category',
        data: analytics.category_performance.map(cp => cp.avg_score),
        backgroundColor: 'rgba(53, 162, 235, 0.5)',
      }
    ]
  };

  return (
    <div className="container mx-auto p-4">
      <h2 className="text-2xl font-bold mb-4">Premium Features</h2>
      
      <div className="mb-8">
        <h3 className="text-xl font-bold mb-2">Advanced Analytics</h3>
        <p>Total Scenarios Played: {analytics.total_scenarios}</p>
        <p>Overall Average Score: {analytics.average_score.toFixed(2)}</p>
        <p>Ethical Tendency: {analytics.ethical_tendency.toFixed(2)}</p>
        
        <div className="mt-4">
          <h4 className="text-lg font-bold mb-2">Score Trend Over Time</h4>
          <Line data={timeTrendData} />
        </div>
        
        <div className="mt-4">
          <h4 className="text-lg font-bold mb-2">Performance by Category</h4>
          <Bar data={categoryPerformanceData} />
        </div>
      </div>
      
      <div>
        <h3 className="text-xl font-bold mb-2">Exclusive Scenarios</h3>
        {exclusiveScenarios.map(scenario => (
          <div key={scenario.id} className="mb-4 p-4 border rounded">
            <h4 className="text-lg font-bold">{scenario.title}</h4>
            <p>{scenario.description}</p>
            <p>Difficulty: {scenario.difficulty}</p>
            <p>Category: {scenario.category}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default PremiumFeatures;