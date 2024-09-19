// Login.js
import React, { useState } from "react";
import api from "../api";

function Login() {
  const [error, setError] = useState(null);

  const handleGoogleLogin = () => {
    api
      .get("/api/auth/login")
      .then((response) => {
        console.log("OAuth URL response:", response.data);
        const oauthUrl = response.data.oauth_url;
        if (typeof oauthUrl === "string") {
          window.location.href = oauthUrl;
        } else {
          console.error("Invalid OAuth URL:", oauthUrl);
          setError("Failed to initiate login with Google.");
        }
      })
      .catch((error) => {
        console.error("Error initiating Google login:", error);
        setError("Failed to initiate login with Google.");
      });
  };

  return (
    <div className="p-5">
      <h2 className="text-2xl mb-4">Login</h2>

      {/* Google Login Button */}
      <button onClick={handleGoogleLogin} className="mb-4">
        Login with Google
      </button>

      {error && <p className="text-red-500">{error}</p>}
    </div>
  );
}

export default Login;
