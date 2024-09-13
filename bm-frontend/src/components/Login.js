import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api, { checkUserSession } from "../api";

function Login() {
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState(null);

  useEffect(() => {
    const attemptAutoLogin = async () => {
      try {
        const session = await checkUserSession();
        if (session) {
          navigate("/dashboard"); // Redirect to dashboard if session is valid
        }
      } catch (error) {
        console.error("No active session found, please log in.");
      }
    };

    attemptAutoLogin();
  }, [navigate]);

  // Handle login via Google
  const handleGoogleLogin = () => {
    window.location.href = `${api.defaults.baseURL}/api/auth/login`;
  };

  // Handle login via username and password
  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post("/api/auth/login", {
        username,
        password,
      });
      if (response.status === 200) {
        navigate("/dashboard"); // Redirect to dashboard after successful login
      } else {
        setError("Invalid credentials, please try again.");
      }
    } catch (err) {
      setError("Login failed. Please check your username and password.");
      console.error("Login error:", err);
    }
  };

  return (
    <div className="p-5">
      <h2 className="text-2xl mb-4">Login</h2>

      {/* Google Login Button */}
      <button onClick={handleGoogleLogin} className="mb-4">
        Login with Google
      </button>

      {/* OR separator */}
      <div className="my-4 text-gray-500">or</div>

      {/* Username and Password Login Form */}
      <form onSubmit={handleLogin} className="space-y-4">
        <div>
          <label className="block text-sm font-bold mb-1" htmlFor="username">
            Username
          </label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            className="w-full p-2 border rounded"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-bold mb-1" htmlFor="password">
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full p-2 border rounded"
            required
          />
        </div>

        {error && <p className="text-red-500">{error}</p>}

        <button type="submit" className="">
          Login with Username
        </button>
      </form>
    </div>
  );
}

export default Login;
