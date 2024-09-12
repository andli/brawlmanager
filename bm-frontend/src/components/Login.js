import React, { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api, { checkUserSession } from "../api";

function Login() {
  const navigate = useNavigate();

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

  const handleLogin = () => {
    console.log(`${api.defaults.baseURL}/api/auth/login`);
    window.location.href = `${api.defaults.baseURL}/api/auth/login`;
  };

  return (
    <div className="p-5">
      <button
        onClick={handleLogin}
        className="bg-blue-500 text-white font-bold py-2 px-4 rounded"
      >
        Login with Google
      </button>
    </div>
  );
}

export default Login;
