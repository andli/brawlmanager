// bm-frontend/src/components/Dashboard.js
import React, { useEffect, useState } from 'react';
import { fetchUser, fetchTeams } from '../api';
import User from './User';
import Team from './Team';

function Dashboard() {
  const [user, setUser] = useState(null);
  const [teams, setTeams] = useState([]);

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

  return (
    <div>
      <h2>Your Dashboard</h2>
      {user && <User user={user} />}
      <Team team={teams[0]} onTeamCreated={handleTeamCreated} />
    </div>
  );
}

export default Dashboard;
