// Leaderboards.js
import React, { useEffect, useState } from "react";
import { fetchAllTeams } from "../api";

function Leaderboards({ onSignOut }) {
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  // Load teams data when component mounts
  useEffect(() => {
    const loadTeamsData = async () => {
      try {
        const teamsData = await fetchAllTeams();
        setTeams(teamsData);
        setLoading(false); // Data loaded, stop loading
      } catch (error) {
        console.error("Error loading teams data:", error);
        setError("Failed to load teams.");
        setLoading(false); // Stop loading even on error
      }
    };

    loadTeamsData();
  }, []);

  // Loading state
  if (loading) {
    return <div>Loading teams...</div>;
  }

  // Error state
  if (error) {
    return <div>{error}</div>;
  }

  return (
    <div>
      <h2>All Teams</h2>
      {teams.length > 0 ? (
        <table className="table-auto w-full border-collapse">
          <thead>
            <tr className="border border-gray-500">
              <th className="border border-gray-500 px-4 py-2">Team Name</th>
              <th className="border border-gray-500 px-4 py-2">Race</th>
              <th className="border border-gray-500 px-4 py-2">Home wins</th>
              <th className="border border-gray-500 px-4 py-2">Away wins</th>
              <th className="border border-gray-500 px-4 py-2">Total wins</th>
            </tr>
          </thead>
          <tbody>
            {teams.map((team) => (
              <tr key={team.id} className="border border-gray-500">
                <td className="border border-gray-500 px-4 py-2">
                  {team.name}
                </td>
                <td className="border border-gray-500 px-4 py-2">
                  {team.race}
                </td>
                <td className="border border-gray-500 px-4 py-2">
                  {team.home_wins}
                </td>
                <td className="border border-gray-500 px-4 py-2">
                  {team.away_wins}
                </td>
                <td className="border border-gray-500 px-4 py-2">
                  {team.total_wins}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      ) : (
        <p>No teams available</p>
      )}
    </div>
  );
}

export default Leaderboards;
