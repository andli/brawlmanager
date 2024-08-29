import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard'; 


function Home() {
  /* const handleLogin = async () => {
    try {
      // Make a request to the backend to initiate the OAuth login
      const response = await axios.get('/api/auth/login');
      
      // Redirect the user to the URL returned by the backend
      window.location.href = response.data.redirectUrl || '/api/auth/login';
    } catch (error) {
      console.error('Login failed:', error);
    }
  }; */
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

export default App;