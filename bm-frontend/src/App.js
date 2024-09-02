import React, { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import Dashboard from "./components/Dashboard";
import Home from "./components/Home";
import Login from "./components/Login";
import { checkUserSession, signOut } from "./api";

function App() {
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkSession = async () => {
      try {
        const session = await checkUserSession();
        setIsAuthenticated(session ? true : false);
      } catch (error) {
        setIsAuthenticated(false);
      }
      setLoading(false);
    };

    checkSession();
  }, []);

  const handleSignOut = async () => {
    await signOut();
    setIsAuthenticated(false);
  };

  if (loading) {
    return <div>Loading...</div>; // Or a spinner, while the session is being checked
  }

  return (
    <Router>
      <Routes>
        <Route
          path="/"
          element={isAuthenticated ? <Navigate to="/dashboard" /> : <Home />}
        />
        <Route
          path="/dashboard"
          element={
            isAuthenticated ? (
              <Dashboard onSignOut={handleSignOut} />
            ) : (
              <Navigate to="/" />
            )
          }
        />
        <Route path="/login" element={<Login />} />
      </Routes>
    </Router>
  );
}

export default App;
