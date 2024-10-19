// Dashboard.js

import { Button, Paper, Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Typography } from '@mui/material';
import { useCallback, useEffect, useState } from 'react';
import DeliveryRow from './DeliveryRow';

const DeliveryTable = () => {
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
      <Typography variant="h5" padding={1}>
        Ongoing Deliveries
      </Typography>
      {loading ? (
        <p>Loading...</p>
      ) : (
        <TableContainer component={Paper}>
          <Table>

            <TableHead>
              <TableRow>
                <TableCell align='center'><strong>Status</strong></TableCell>
                <TableCell align='center'><strong>Delivery ID</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody >
              {deliveries.length > 0 ? (
                deliveries.map((delivery) => (
                  <DeliveryRow key={delivery.id} delivery={delivery} />
                ))
              ) : (
                <TableRow>
                  <TableCell colSpan={5} align="center">
                    No deliveries
                  </TableCell>
                </TableRow>
              )}
            </TableBody>
          </Table>
          <Button
            variant="contained"
            color="primary"
            onClick={fetchDeliveries}
            style={{ margin: "1rem" }}
          >
            Refresh
          </Button>
        </TableContainer>
      )}
    </div>
  );
};

export default DeliveryTable;