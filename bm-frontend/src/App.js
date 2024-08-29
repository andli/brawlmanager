import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Dashboard from './components/Dashboard'; 

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