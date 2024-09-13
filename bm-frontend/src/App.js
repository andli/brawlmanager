import React, { useEffect, useState } from "react";
import {
  BrowserRouter as Router,
  Route,
  Routes,
  Navigate,
} from "react-router-dom";
import { checkUserSession, signOut } from "./api";
import Dashboard from "./components/Dashboard";
import Home from "./components/Home";
import Login from "./components/Login";
import Profile from "./components/Profile";
import Leaderboards from "./components/Leaderboards";
import Navbar from "./components/Navbar";
import MatchSimulator from "./components/MatchSimulator";

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
    document.title = "Brawl Manager";

    checkSession();
  }, []);

  if (loading) {
    return <div>Loading...</div>; // Or a spinner, while the session is being checked
  }

  // Handle sign out logic
  const handleSignOut = async () => {
    await signOut();
    setIsAuthenticated(false);
    Navigate("/login");
  };

  return (
    <Router>
      <div className="min-h-screen flex flex-col">
        {/* Navbar */}
        <Navbar isAuthenticated={isAuthenticated} onSignOut={handleSignOut} />

        {/* Main Content */}
        <div className="flex-grow p-5">
          <Routes>
            <Route
              path="/"
              element={
                isAuthenticated ? <Navigate to="/dashboard" /> : <Home />
              }
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
            <Route
              path="/profile"
              element={
                isAuthenticated ? (
                  <Profile onSignOut={handleSignOut} />
                ) : (
                  <Navigate to="/" />
                )
              }
            />
            <Route
              path="/leaderboards"
              element={
                isAuthenticated ? (
                  <Leaderboards onSignOut={handleSignOut} />
                ) : (
                  <Navigate to="/" />
                )
              }
            />
            <Route
              path="/matches"
              element={
                isAuthenticated ? (
                  <MatchSimulator onSignOut={handleSignOut} />
                ) : (
                  <Navigate to="/" />
                )
              }
            />
            <Route path="/login" element={<Login />} />
          </Routes>
        </div>
      </div>
    </Router>
  );
}

export default App;
