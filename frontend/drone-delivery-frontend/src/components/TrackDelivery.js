import { Button, TextField, Typography } from "@mui/material";
import { useState } from "react";
import DeliveryDetails from "./DeliveryDetails";

const TrackDelivery = () => {
  const [deliveryId, setDeliveryId] = useState("");
  const [delivery, setDelivery] = useState(null);
  const [error, setError] = useState(null);

  const handleTrackDelivery = async (event) => {
    event.preventDefault();
    try {
      const response = await fetch(`http://localhost:8000/deliveries/${deliveryId}/`);
      if (!response.ok) {
        throw new Error("Delivery not found");
      }

      const data = await response.json();
      console.log("Delivery details fetched from tracker", data);
      setDelivery({
        id: deliveryId,
      });
      setError(null);
    } catch (error) {
      setDelivery(null);
      setError("Delivery not found");
    }
  };

  return (
    <div>
      <Typography variant="h6" gutterBottom>
        Track a Delivery
      </Typography>
      <form onSubmit={handleTrackDelivery} style={{ marginBottom: '20px' }}>
        <TextField
          label="Enter Delivery ID"
          value={deliveryId}
          onChange={(e) => setDeliveryId(e.target.value)}
          variant="outlined"
          fullWidth
          style={{ marginBottom: '10px' }}
        />
        <Button type="submit" variant="contained" color="primary" fullWidth>
          Track Delivery
        </Button>
      </form>

      {error && <Typography color="error">{error}</Typography>}

      {delivery && (
        <div style={{ marginTop: "20px" }}>
          <DeliveryDetails delivery={delivery} />
        </div>
      )}
    </div>
  );
};

export default TrackDelivery;