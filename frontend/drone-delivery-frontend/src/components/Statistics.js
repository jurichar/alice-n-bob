import { Box, Typography } from "@mui/material";
import React, { useEffect, useState } from "react";
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const Statistics = () => {
  const [stats, setStats] = useState({ ongoing_deliveries: 0, total_deliveries: 0 });
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const fetchStatistics = async () => {
      try {
        const response = await fetch("http://localhost:8000/counts");
        if (!response.ok) {
          throw new Error("Failed to fetch statistics");
        }
        const data = await response.json();
        setStats(data);
        const currentTime = new Date().toLocaleTimeString();
        setChartData(prevData => [
          ...prevData,
          {
            time: currentTime,
            total: data.total_deliveries,
            ongoing: data.ongoing_deliveries || 0,
          },
        ].slice(-10));
      } catch (error) {
        console.error("Error fetching statistics", error);
      }
    };

    fetchStatistics();
    const intervalId = setInterval(fetchStatistics, 5000);

    return () => {
      setChartData([]);
      clearInterval(intervalId)
      setStats({ ongoing_deliveries: 0, total_deliveries: 0 });
    };
  }, []);

  return (
    <Box sx={{ marginBottom: "20px", padding: "20px", backgroundColor: "#f5f5f5", borderRadius: "8px" }}>
      <Typography variant="h5" gutterBottom>Delivery Statistics</Typography>
      <Typography variant="body1">
        Ongoing Deliveries: {stats.ongoing_deliveries}
      </Typography>
      <Typography variant="body1">
        Total Deliveries Since Start: {stats.total_deliveries}
      </Typography>

      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="total" stroke="#8884d8" activeDot={{ r: 8 }} />
          <Line type="monotone" dataKey="ongoing" stroke="#FFBB28" />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default Statistics;