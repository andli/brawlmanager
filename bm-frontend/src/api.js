import axios from "axios";

// Axios instance for API calls
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
  withCredentials: true,
});

export default api;

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
    // Clear client-side state or local storage
    localStorage.removeItem("user"); // If you store user info in local storage
    sessionStorage.removeItem("user"); // If you use session storage

    // Optionally, redirect to a different page
    window.location.href = "/"; // or another appropriate URL

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
      // User is not authenticated
      return null;
    }
    // Other error cases
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
