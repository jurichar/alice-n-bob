import { Box } from "@mui/material";
import React, { useEffect, useState } from "react";
import { CartesianGrid, Legend, Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from "recharts";

const StatisticsMore = () => {
  const [chartData, setChartData] = useState([]);

  useEffect(() => {
    const fetchStatistics = async () => {
      try {
        const response = await fetch("http://localhost:8000/counts_all");
        if (!response.ok) {
          throw new Error("Failed to fetch statistics");
        }
        const data = await response.json();
        const currentTime = new Date().toLocaleTimeString();
        setChartData(prevData => [
          ...prevData,
          {
            time: currentTime,
            crashed: data.crashed_deliveries || 0,
            delivered: data.delivered_deliveries || 0,
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
    };
  }, []);

  return (
    <Box sx={{ marginBottom: "20px", padding: "20px", backgroundColor: "#f5f5f5", borderRadius: "8px" }}>
      <ResponsiveContainer width="100%" height={300}>
        <LineChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="time" />
          <YAxis />
          <Tooltip />
          <Legend />
          <Line type="monotone" dataKey="crashed" stroke="red" activeDot={{ r: 8 }} />
          <Line type="monotone" dataKey="delivered" stroke="green" />
        </LineChart>
      </ResponsiveContainer>
    </Box>
  );
};

export default StatisticsMore;