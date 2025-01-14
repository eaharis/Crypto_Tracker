// src/components/Navbar.js
import React from 'react';
import AppBar from '@mui/material/AppBar';
import Box from '@mui/material/Box';
import Toolbar from '@mui/material/Toolbar';
import Typography from '@mui/material/Typography';
import { Button, TextField } from '@mui/material';

function Navbar() {
    return (
        <Box sx={{ flexGrow: 1 }}>
            <AppBar position="static" sx={{ bgcolor: '#1976d2' }}>
                <Toolbar>
                    {/* Left side links */}
                    <Typography variant="h6" component="a" href="/" sx={{ mr: 2, textDecoration: 'none', color: '#fff' }}>
                        Home
                    </Typography>
                    <Typography variant="h6" component="a" href="#" sx={{ mr: 2, textDecoration: 'none', color: '#fff' }}>
                        Placeholder 1
                    </Typography>
                    <Typography variant="h6" component="a" href="#" sx={{ mr: 2, textDecoration: 'none', color: '#fff' }}>
                        Placeholder 2
                    </Typography>

                    {/* Push the search bar + login button to the right */}
                    <Box sx={{ flexGrow: 1 }} />

                    {/* Search bar */}
                    <TextField
                        variant="outlined"
                        size="small"
                        placeholder="Search..."
                        sx={{ backgroundColor: '#fff', borderRadius: 1, mr: 2 }}
                    />

                    {/* Log in button */}
                    <Button variant="contained" color="secondary">
                        Log In
                    </Button>
                </Toolbar>
            </AppBar>
        </Box>
    );
}

export default Navbar;