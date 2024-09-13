import React, { useState, useEffect } from "react";
import { connectToMatchWebSocket, fetchAllTeams } from "../api";

const MatchSimulator = () => {
  const [teams, setTeams] = useState([]); // Store teams data
  const [homeTeamId, setHomeTeamId] = useState("");
  const [awayTeamId, setAwayTeamId] = useState("");
  const [tickSpeed, setTickSpeed] = useState(1);
  const [logs, setLogs] = useState([]);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Fetch all teams data when the component mounts
    const getTeams = async () => {
      try {
        const teamsData = await fetchAllTeams();
        setTeams(teamsData); // Populate teams state
      } catch (err) {
        console.error("Error fetching teams:", err);
        setError("Failed to load teams. Please try again.");
      }
    };

    getTeams();
  }, []);

  const startMatch = () => {
    const ws = connectToMatchWebSocket(
      homeTeamId,
      awayTeamId,
      tickSpeed,
      (message) => {
        setLogs((prevLogs) => [...prevLogs, message]); // Append message to logs
      },
      (err) => {
        setError("WebSocket connection failed. Please try again.");
      },
      () => {
        console.log("WebSocket connection closed");
      }
    );
  };

  return (
    <div>
      <h2>Match Simulator</h2>
      {error && <p style={{ color: "red" }}>{error}</p>}
      <div>
        <label>Home Team: </label>
        <select
          value={homeTeamId}
          onChange={(e) => setHomeTeamId(e.target.value)}
        >
          <option value="">Select Home Team</option>
          {teams.map((team) => (
            <option key={team.id} value={team.id}>
              {team.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label>Away Team: </label>
        <select
          value={awayTeamId}
          onChange={(e) => setAwayTeamId(e.target.value)}
        >
          <option value="">Select Away Team</option>
          {teams.map((team) => (
            <option key={team.id} value={team.id}>
              {team.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label>Tick Speed: </label>
        <input
          type="number"
          value={tickSpeed}
          onChange={(e) => setTickSpeed(e.target.value)}
          min="0.1"
          step="0.1"
        />
      </div>

      <button onClick={startMatch}>Start Match</button>

      <div>
        <h3>Match Logs</h3>
        <div
          style={{
            whiteSpace: "pre-line",
            maxHeight: "400px",
            overflowY: "scroll",
          }}
        >
          {logs.map((log, index) => (
            <div key={index}>{log}</div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default MatchSimulator;
