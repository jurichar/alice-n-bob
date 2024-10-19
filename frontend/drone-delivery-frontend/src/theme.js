import { createTheme } from '@mui/material/styles';

const theme = createTheme({
    palette: {
        primary: {
            main: '#fed731',
        },
        secondary: {
            main: '#00b5c8',
        },
        background: {
            default: '#f7f8f9',
        },
    },
    typography: {
        fontFamily: "'Rubik', sans-serif",
        body1: {
            fontWeight: 400
        }
    },
});

export default theme;