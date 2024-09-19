import React, { useEffect, useState } from "react";
import {
  Route,
  Routes,
  useNavigate,
  Navigate, // Import Navigate with a capital 'N'
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

  const navigate = useNavigate();

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
    return <div>Loading...</div>;
  }

  // Handle sign out logic
  const handleSignOut = async () => {
    await signOut();
    setIsAuthenticated(false);
    navigate("/login");
  };

  return (
    <div className="min-h-screen flex flex-col">
      <Navbar isAuthenticated={isAuthenticated} onSignOut={handleSignOut} />

      {/* Main Content */}
      <div className="flex-grow p-5">
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
  );
}

export default App;
