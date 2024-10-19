import { Container, AppBar, Toolbar, Typography, Box } from '@mui/material';

function App() {
  return (
    <div>
      <AppBar position="static">
        <Toolbar>
          <Box component="img" src={`${process.env.PUBLIC_URL}/logo-ab.png`} alt="A&B Logo" sx={{ height:100, marginRight: 2}} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1}}>
            Drone Delivery Dashboard
          </Typography>
        </Toolbar>
      </AppBar>
      <Container>
        <Typography variant="h4" gutterBottom style={{ marginTop: '20px'}}>
          Welcome to the Drone Delivery System
        </Typography>
        <Typography variant="body1">
          This is the homepage for managing drone deliveries. Use the navigation to view ongoing deliveries or statistics.
        </Typography>
      </Container>
    </div>
  );
}

export default App;
