import React, { useState, useEffect } from 'react';
import axios from 'axios';

function SubscriptionManager({ token }) {
  const [subscription, setSubscription] = useState('free');
  const [addons, setAddons] = useState([]);

  useEffect(() => {
    fetchSubscriptionInfo();
  }, []);

  const fetchSubscriptionInfo = async () => {
    try {
      const response = await axios.get('http://localhost:5000/api/user_info', {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSubscription(response.data.subscription_tier);
      setAddons(response.data.addons.split(',').filter(Boolean));
    } catch (error) {
      console.error('Error fetching subscription info:', error);
    }
  };

  const upgradeTier = async (newTier) => {
    try {
      await axios.post('http://localhost:5000/api/upgrade', { tier: newTier }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setSubscription(newTier);
    } catch (error) {
      console.error('Error upgrading subscription:', error);
    }
  };

  const addAddon = async (newAddon) => {
    try {
      await axios.post('http://localhost:5000/api/add_addon', { addon: newAddon }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      setAddons([...addons, newAddon]);
    } catch (error) {
      console.error('Error adding add-on:', error);
    }
  };

  return (
    <div className="mt-8">
      <h2 className="text-xl font-bold mb-4">Subscription Management</h2>
      <p>Current Tier: {subscription}</p>
      <div className="mt-4">
        <button onClick={() => upgradeTier('premium')} className="mr-2 p-2 bg-blue-500 text-white rounded">Upgrade to Premium</button>
        <button onClick={() => upgradeTier('enterprise')} className="p-2 bg-purple-500 text-white rounded">Upgrade to Enterprise</button>
      </div>
      <h3 className="text-lg font-bold mt-4 mb-2">Add-ons:</h3>
      <ul>
        {addons.map((addon, index) => (
          <li key={index}>{addon}</li>
        ))}
      </ul>
      <div className="mt-4">
        <button onClick={() => addAddon('expert_analysis')} className="mr-2 p-2 bg-green-500 text-white rounded">Add Expert Analysis</button>
        <button onClick={() => addAddon('scenario_pack')} className="mr-2 p-2 bg-yellow-500 text-white rounded">Add Scenario Pack</button>
        <button onClick={() => addAddon('coaching')} className="p-2 bg-red-500 text-white rounded">Add Coaching Session</button>
      </div>
    </div>
  );
}

export default SubscriptionManager;