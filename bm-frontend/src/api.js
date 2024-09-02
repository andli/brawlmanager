import axios from 'axios';

// Axios instance for API calls
const api = axios.create({
    baseURL: 'http://localhost:8000/api',
    withCredentials: true,
});

// Fetch the authenticated user's data
export const fetchUser = async () => {
  try {
    const response = await axios.get('/api/user');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch user:', error);
    throw error;
  }
};

// Fetch the user's teams and players
export const fetchTeams = async () => {
  try {
    const response = await axios.get('/api/teams');
    return response.data;
  } catch (error) {
    console.error('Failed to fetch teams:', error);
    throw error;
  }
};

export const signOut = async () => {
    try {
        await api.post('/auth/signout');
        // You can clear any additional client-side state here if necessary
        return true;
    } catch (error) {
        console.error("Error signing out", error);
        return false;
    }
};

// Function to check if the user is logged in
export const checkUserSession = async () => {
    try {
        const response = await api.get('/auth/check-session');
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
