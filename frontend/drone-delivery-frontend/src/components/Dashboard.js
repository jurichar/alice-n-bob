// Dashboard.js

import { Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';
import { useCallback, useEffect, useState } from 'react';

const Dashboard = () => {
  const [deliveries, setDeliveries] = useState([]);
  const [loading, setLoading] = useState(true);
  
  const fetchDeliveries = useCallback(async () => {
    try {
      const response = await fetch("http://localhost:8000/deliveries");
      if (!response.ok) {
        throw new Error("Failed to fetch deliveries");
      }
      const data = await response.json();
      setDeliveries(data);
    } catch (error) {
      console.error("Error fetching deliveries", error);
    } finally {
      setLoading(false)
    }
  }, []);

  useEffect(() => {
    fetchDeliveries();
  }, [fetchDeliveries]);

  return (
    <div>
      <Typography variant="h4" gutterBottom>
        Ongoing Deliveries
      </Typography>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell><strong>Status</strong></TableCell>
              <TableCell><strong>Delivery ID</strong></TableCell>
              <TableCell><strong>Actions</strong></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            <TableRow>
              <TableCell colSpan={5} align="center">
                No deliveries
              </TableCell>
            </TableRow>
          </TableBody>
        </Table>
      </TableContainer>
      )}
    </div>
  );
};

export default Dashboard;