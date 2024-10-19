// Dashboard.js

import { useEffect, useState } from 'react';

const Dashboard = () => {
  const [deliveries, setDeliveries] = useState([]);
  const [loading, setLoading] = useState(true);
  
  useEffect(() => {
    const fetchDeliveries = async () => {
      const response = await fetch('http://localhost:8000/deliveries');
      const data = await response.json();
      setDeliveries(data);
      setLoading(false);
    };
    fetchDeliveries();
  }, []);

  return (
    <div>
      <h1>Dashboard</h1>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <ul>
          {deliveries.map((delivery) => (
            <li key={delivery.id}>{delivery.address}</li>
          ))}
        </ul>
      )}
    </div>
  );
};

export default Dashboard;