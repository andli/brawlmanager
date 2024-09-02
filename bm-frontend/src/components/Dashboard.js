import React, { useEffect, useState } from "react";
import { fetchUser, fetchTeams } from "../api";
import User from "./User";
import Team from "./Team";
import { useNavigate } from "react-router-dom";

function Dashboard({ onSignOut }) {
  const [user, setUser] = useState(null);
  const [teams, setTeams] = useState([]);
  const navigate = useNavigate();

  useEffect(() => {
    const loadData = async () => {
      try {
        const userData = await fetchUser();
        const teamsData = await fetchTeams();

        setUser(userData);
        setTeams(teamsData);
      } catch (error) {
        console.error("Error loading data:", error);
      }
    };

    loadData();
  }, []);

  const handleTeamCreated = (newTeam) => {
    setTeams([newTeam]);
  };

  const handleSignOut = async () => {
    await onSignOut();
    navigate("/login");
  };

  return (
    <div>
      <h2>Your Dashboard</h2>
      {user && <User user={user} />}
      {teams.length > 0 && (
        <Team team={teams[0]} onTeamCreated={handleTeamCreated} />
      )}
      <button onClick={handleSignOut} className="confirm_button">
        Sign Out
      </button>
    </div>
  );
}

export default Dashboard;
