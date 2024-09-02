import React, { useEffect, useState } from 'react';
import { BrowserRouter as Router, Route, Routes, Navigate } from 'react-router-dom';
import Dashboard from './components/Dashboard';
import Home from './components/Home';
import axios from 'axios';

// Axios instance for API calls
const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    withCredentials: true,
});

// Function to check if the user is logged in
export const checkUserSession = async () => {
    try {
        const response = await api.get('/auth/check-session');
        if (response.status === 200) {
            return response.data;
        }
    } catch (error) {
        console.error("Error checking user session", error);
        if (error.response && error.response.status === 401) {
            // User is not authenticated
            return null;
        }
        // Other error cases
        return null;
    }
};

function App() {
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const checkSession = async () => {
            const session = await checkUserSession();
            if (session) {
                setIsAuthenticated(true);
            } else {
                setIsAuthenticated(false);
            }
            setLoading(false);
        };

        checkSession();
    }, []);

    if (loading) {
        return <div>Loading...</div>; // Or a spinner, while the session is being checked
    }

    return (
        <Router>
            <Routes>
                <Route path="/" element={isAuthenticated ? <Navigate to="/dashboard" /> : <Home />} />
                <Route path="/dashboard" element={isAuthenticated ? <Dashboard /> : <Navigate to="/" />} />
            </Routes>
        </Router>
    );
}

export default App;
