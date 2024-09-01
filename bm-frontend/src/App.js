import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard'; 
import axios from 'axios';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  );
}


const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    withCredentials: true,
});

// Function to check if the user is logged in
export const checkUserSession = async () => {
    try {
        const response = await api.get('/auth/check-session');
        if (response.status === 200) {
            // User is logged in
            return response.data;
        } else {
            // Redirect to login
            window.location.href = '/auth/login';
        }
    } catch (error) {
        console.error("Error checking user session", error);
        window.location.href = '/auth/login';
    }
};

function Home() {
  const handleLogin = () => {
  window.location.href = "http://localhost:8000/api/auth/login";
};

  return (
    <div>
      <h1>Welcome to BrawlManager</h1>
      <p>Login with your Google account to get started.</p>
      <button onClick={handleLogin}>Login with Google</button>
    </div>
  );
}

export default App;