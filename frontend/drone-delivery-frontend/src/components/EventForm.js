import { Button, MenuItem, Select, Typography } from "@mui/material";
import React, { useState } from "react";

const EventForm = ({ deliveryId, onEventAdded }) => {
  const [eventType, setEventType] = useState("");
  const [error, setError] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch(`http://localhost:8000/deliveries/${deliveryId}/events`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ type: eventType }),
      });

      if (!response.ok) {
        throw new Error("Failed to add event");
      }

      const data = await response.json();
      console.log("Event added successfully", data);
      onEventAdded();
    } catch (error) {
      setError("Failed to add event");
      console.error("Error adding event", error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <Typography variant="h6">Add Event</Typography>
      <Select
        value={eventType}
        onChange={(e) => setEventType(e.target.value)}
        displayEmpty
        fullWidth
      >
        <MenuItem value="" disabled>
          Select Event Type
        </MenuItem>
        <MenuItem value="TAKEN_OFF">TAKEN_OFF</MenuItem>
        <MenuItem value="LANDED">LANDED</MenuItem>
        <MenuItem value="CRASHED">CRASHED</MenuItem>
        <MenuItem value="PARCEL_DELIVERED">PARCEL_DELIVERED</MenuItem>
      </Select>
      <Button type="submit" variant="contained" color="primary" style={{ marginTop: "10px" }}>
        Submit
      </Button>
      {error && <Typography color="error">{error}</Typography>}
    </form>
  );
};

export default EventForm;