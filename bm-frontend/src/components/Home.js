import React from "react";
import { useNavigate } from "react-router-dom";

function Home() {
  const navigate = useNavigate();

  const handleLogin = () => {
    navigate("/login");
  };

  return (
    <div>
      <h1>Welcome to Brawl Manager</h1>
      <p>Please log in to continue.</p>
      <button onClick={handleLogin}>Login</button>
    </div>
  );
}

export default Home;
