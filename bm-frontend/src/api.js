import axios from "axios";

// Axios instance for API calls
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  withCredentials: true,
});

export default api;

// WebSocket connection function
export const connectToMatchWebSocket = (
  homeTeamId,
  awayTeamId,
  tickSpeed,
  onMessage,
  onError,
  onClose
) => {
  const ws = new WebSocket(
    `ws://localhost:8000/api/ws/match?home_team_id=${homeTeamId}&away_team_id=${awayTeamId}&tick_speed=${tickSpeed}`
  );

  ws.onopen = () => {
    console.log("WebSocket connection opened");
  };

  ws.onmessage = (event) => {
    onMessage(event.data); // Pass the received message to the callback function
  };

  ws.onerror = (error) => {
    console.error("WebSocket error:", error);
    onError(error); // Pass the error to the callback function
  };

  ws.onclose = () => {
    console.log("WebSocket connection closed");
    onClose(); // Trigger callback on close
  };

  return ws; // Return the WebSocket instance to be used for sending messages or closing the connection if needed
};

// Fetch the authenticated user's data
export const fetchUser = async () => {
  try {
    const response = await api.get("/api/user");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch user:", error);
    throw error;
  }
};

// Fetch the user's teams and players
export const fetchTeams = async () => {
  try {
    const response = await api.get("/api/teams");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch teams:", error);
    throw error;
  }
};

// Fetch all teams and players
export const fetchAllTeams = async () => {
  try {
    const response = await api.get("/api/allteams");
    return response.data;
  } catch (error) {
    console.error("Failed to fetch teams:", error);
    throw error;
  }
};

// Sign out the user
export const signOut = async () => {
  try {
    await api.post("/api/auth/signout");
    localStorage.removeItem("user"); // Clear local storage
    sessionStorage.removeItem("user"); // Clear session storage
    window.location.href = "/"; // Redirect to home

    return true;
  } catch (error) {
    console.error("Error signing out", error);
    return false;
  }
};

// Function to check if the user is logged in
export const checkUserSession = async () => {
  console.log("baseURL:", process.env.REACT_APP_API_URL);
  try {
    const response = await api.get("/api/auth/check-session");
    if (response.status === 200) {
      return response.data;
    }
  } catch (error) {
    console.error("Error checking user session", error);
    if (error.response && error.response.status === 401) {
      return null; // User not authenticated
    }
    return null;
  }
};

// Create a new team
export const createTeam = async (teamData) => {
  try {
    const response = await api.post("/api/teams", teamData);
    return response.data;
  } catch (error) {
    console.error("Failed to create team:", error);
    throw error;
  }
};

// Create a new player
export const createPlayer = async (playerData) => {
  try {
    const response = await api.post("/api/players", playerData);
    return response.data;
  } catch (error) {
    console.error("Failed to create player:", error);
    throw error;
  }
};
