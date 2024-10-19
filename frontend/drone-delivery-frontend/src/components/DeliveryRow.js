import ExpandMoreIcon from "@mui/icons-material/ExpandMore";
import {
  Accordion,
  AccordionDetails,
  AccordionSummary,
  TableCell,
  TableRow,
  Typography,
  useMediaQuery,
  useTheme
} from "@mui/material";
import { useState } from "react";
import DeliveryDetails from "./DeliveryDetails";

const DeliveryRow = ({ delivery }) => {
  const [open, setOpen] = useState(false);

  const handleToggleDetails = () => {
    setOpen(!open);
  };

  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("sm"));
  const displayedId = isMobile ? delivery.id.substring(0, 6) + "..." : delivery.id;

  
  return (
    <>
      <TableRow>
        <TableCell colSpan={5} >
          <Accordion expanded={open} onChange={handleToggleDetails} elevation={0}>
          <AccordionSummary
              expandIcon={<ExpandMoreIcon />}
              aria-controls="panel1a-content"
            >
              <Typography sx={{textAlign: 'center', flex: 1, fontSize: isMobile ? "0.75rem" : "1rem" }}>{delivery.state}</Typography>
              <Typography sx={{textAlign: 'center', flex: 1, fontSize: isMobile ? "0.75rem" : "1rem" }}>{displayedId}</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <DeliveryDetails delivery={delivery} />
            </AccordionDetails>
          </Accordion>
        </TableCell>
      </TableRow>
    </>
  );
};

export default DeliveryRow;