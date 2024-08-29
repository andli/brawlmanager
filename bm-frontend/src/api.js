import axios from 'axios';

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
