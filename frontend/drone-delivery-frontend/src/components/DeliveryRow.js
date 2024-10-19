import {
  TableCell,
  TableRow,
  Typography
} from "@mui/material";
import React from "react";

const DeliveryRow = ({ delivery }) => {

  return (
    <>
      <TableRow>
        <TableCell colSpan={5}>
              <Typography sx={{ flex: 1 }}>{delivery.id}</Typography>
              <Typography sx={{ flex: 1 }}>{delivery.state}</Typography>
              <Typography sx={{ flex: 1 }}>{new Date(delivery.created_at).toLocaleString()}</Typography>
              <Typography sx={{ flex: 1 }}>{new Date(delivery.updated_at).toLocaleString()}</Typography>
        </TableCell>
      </TableRow>
    </>
  );
};

export default DeliveryRow;