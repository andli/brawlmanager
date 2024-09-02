// bm-frontend/src/components/Dashboard.js
import React, { useEffect, useState } from 'react';
import { fetchUser, fetchTeams, signOut } from '../api';  // Assuming you have these API functions defined
import User from './User';  // Assuming you have a User component to display user info
import Team from './Team';  // Assuming you have a Team component to display team info
import { useNavigate } from 'react-router-dom';

function Dashboard() {
  const [user, setUser] = useState(null);
  const [teams, setTeams] = useState([]);
  const navigate = useNavigate();  // Hook for programmatic navigation

  useEffect(() => {
    const loadData = async () => {
      try {
        const userData = await fetchUser();
        const teamsData = await fetchTeams();
        
        setUser(userData);
        setTeams(teamsData);
      } catch (error) {
        console.error('Error loading data:', error);
      }
    };

    loadData();
  }, []);

  const handleTeamCreated = (newTeam) => {
    setTeams([newTeam]);  // Update state with the newly created team
  };

  const handleSignOut = async () => {
    const success = await signOut();
    if (success) {
      navigate('/');  // Redirect to home or login page after signing out
    }
  };

  return (
    <div>
      <h2>Your Dashboard</h2>
      {user && <User user={user} />}
      {teams.length > 0 && <Team team={teams[0]} onTeamCreated={handleTeamCreated} />}
      <button onClick={handleSignOut} className="confirm_button">Sign Out</button>  {/* Sign out button */}
    </div>
  );
}

export default Dashboard;
