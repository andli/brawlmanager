import React, { useEffect, useState } from "react";
import { fetchTeams, createTeam, createPlayer } from "../api";
import Team from "./Team";
import Profile from "./Profile";
import { useNavigate } from "react-router-dom";

function Dashboard({ onSignOut }) {
  const [teams, setTeams] = useState([]);
  const navigate = useNavigate();

  // Load teams data when component mounts
  useEffect(() => {
    const loadData = async () => {
      try {
        const teamsData = await fetchTeams();
        setTeams(teamsData);
      } catch (error) {
        console.error("Error loading data:", error);
      }
    };

    loadData();
  }, []);

  // Function to reload the teams data
  const reloadTeams = async () => {
    try {
      const updatedTeams = await fetchTeams();
      setTeams(updatedTeams);
    } catch (error) {
      console.error("Error reloading teams:", error);
    }
  };

  const handleCreateTeam = async () => {
    try {
      const teamData = {
        name: "New Team",
        race: "Dwarfs",
        owner_id: null, // Assuming the Profile component handles the user and provides owner_id if needed
      };
      const newTeam = await createTeam(teamData);
      setTeams((prevTeams) => [...prevTeams, newTeam]);
    } catch (error) {
      console.error("Error creating team:", error);
    }
  };

  const getTeamByUser = async () => {
    try {
      const teamsData = await fetchTeams();
      if (teamsData.length > 0) {
        return teamsData[0].id; // Return the ID of the user's only team
      } else {
        throw new Error("No team found for the current user.");
      }
    } catch (error) {
      console.error("Error fetching team by user:", error);
      throw error;
    }
  };

  const handleCreatePlayer = async () => {
    try {
      const playerData = {
        name: "Test Testson",
        role: "Runner",
        race: "Dwarf",
        stats: [8, 5, 5, 7, 2, 9],
        team_id: await getTeamByUser(), // Get the team ID dynamically
      };

      const newPlayer = await createPlayer(playerData);
      console.log("Player created:", newPlayer);

      // After the player is created, reload the team data to reflect the changes
      await reloadTeams();
    } catch (error) {
      console.error("Error creating player:", error);
    }
  };

  const handleTeamCreated = (newTeam) => {
    setTeams([newTeam]);
  };

  return (
    <div>
      <p>
        Welcome to Brawl Manager! Manage your team and players, sign up for
        leagues, or play exhibition matches with your friends.
      </p>
      <p>Coming soon:</p>
      <ul>
        <li>Buy and sell players</li>
        <li>Player gear</li>
        <li>Not so accurate football field simulation</li>
        <li>Player injuries and death</li>
      </ul>
      <div>
        {teams.length > 0 && (
          <Team team={teams[0]} onTeamCreated={handleTeamCreated} />
        )}
        <button onClick={handleCreateTeam} className="confirm_button">
          Create Team
        </button>
        <button onClick={handleCreatePlayer} className="confirm_button">
          Create Player
        </button>
      </div>
    </div>
  );
}

export default Dashboard;
