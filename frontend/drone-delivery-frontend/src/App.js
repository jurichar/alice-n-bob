import { AppBar, Box, Container, Toolbar, Typography } from '@mui/material';
import DeliveryTable from './components/DeliveryTable';
import TrackDelivery from './components/TrackDelivery';

function App() {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Box component="img" src={`${process.env.PUBLIC_URL}/logo-ab.png`} alt="A&B Logo" sx={{ height: 100, marginRight: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            Drone Delivery Dashboard
          </Typography>
        </Toolbar>
      </AppBar>
      <Container>
        <Typography variant="h4" gutterBottom style={{ marginTop: '20px' }}>
          Welcome to the Drone Delivery System
        </Typography>
        <TrackDelivery />
        <DeliveryTable />
      </Container>
    </div>
  );
}

export default App;
