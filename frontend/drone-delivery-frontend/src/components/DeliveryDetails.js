import { Divider, List, ListItem, Typography } from "@mui/material";
import React, { useCallback, useEffect, useState } from "react";

const DeliveryDetails = ({ delivery, refreshEvents }) => {
  const [events, setEvents] = useState([]);

  const fetchDeliveryEvents = useCallback(async () => {
    try {
      const response = await fetch(`http://localhost:8000/deliveries/${delivery.id}/events`);
      if (!response.ok) {
        throw new Error("Failed to fetch delivery events");
      }

      const data = await response.json();
      console.log("Delivery events fetched successfully", data);
      setEvents(data); 
    } catch (error) {
      console.error("Error fetching delivery events", error);
    }
  }, [delivery]);

  useEffect(() => {
    fetchDeliveryEvents();
    if (refreshEvents) {
      refreshEvents.current = fetchDeliveryEvents;
    }
  }, [fetchDeliveryEvents, refreshEvents]);

  return (
    <div>
      <Typography>
        <strong>Created At:</strong> {new Date(delivery.created_at).toLocaleString()}
      </Typography>
      <Typography>
        <strong>Updated At:</strong> {new Date(delivery.updated_at).toLocaleString()}
      </Typography>
      <Typography>
        <strong>Status:</strong> {delivery.state}
      </Typography>

      <Typography variant="h6" gutterBottom style={{ marginTop: '20px' }}>
        Event History:
      </Typography>
      
      {events.length > 0 ? (
        <List>
          {events.map((event) => (
            <div key={event.id}>
              <ListItem>
                <Typography>
                  {event.type} - <strong>Date:</strong> {new Date(event.created_at).toLocaleString()}
                </Typography>
              </ListItem>
              <Divider />
            </div>
          ))}
        </List>
      ) : (
        <Typography>No events for this delivery</Typography>
      )}
    </div>
  );
};

export default DeliveryDetails;