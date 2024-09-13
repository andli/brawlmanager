import React from "react";
import CreateTeamForm from "./CreateTeamForm";

function Team({ team, onTeamCreated }) {
  if (!team) {
    // If no team exists, show the CreateTeamForm
    return (
      <div>
        <p>You don't have a team yet. Create one!</p>
        <CreateTeamForm onTeamCreated={onTeamCreated} />
      </div>
    );
  }

  return (
    <div>
      <h3>{team.name}</h3>
      <p>Race: {team.race}</p>
      <div className="my-4">
        <table className="table-auto w-full border-collapse text-xs">
          <thead>
            <tr className="">
              <th className="border border-gray-700 px-4 py-2">Name</th>
              <th className="border border-gray-700 px-4 py-2">Race</th>
              <th className="border border-gray-700 px-4 py-2">MA</th>
              <th className="border border-gray-700 px-4 py-2">ST</th>
              <th className="border border-gray-700 px-4 py-2">AG</th>
              <th className="border border-gray-700 px-4 py-2">PA</th>
              <th className="border border-gray-700 px-4 py-2">AV</th>
            </tr>
          </thead>
          <tbody>
            {team.players && team.players.length > 0 ? (
              team.players.map((player) => (
                <tr key={player.id}>
                  <td className="border border-gray-700 px-4 py-2">
                    {player.name}
                  </td>
                  <td className="border border-gray-700 px-4 py-2">
                    {player.race}
                  </td>
                  <td className="border border-gray-700 px-4 py-2">
                    {player.stats[0]}
                  </td>
                  <td className="border border-gray-700 px-4 py-2">
                    {player.stats[1]}
                  </td>
                  <td className="border border-gray-700 px-4 py-2">
                    {player.stats[2]}
                  </td>
                  <td className="border border-gray-700 px-4 py-2">
                    {player.stats[3]}
                  </td>
                  <td className="border border-gray-700 px-4 py-2">
                    {player.stats[4]}
                  </td>
                </tr>
              ))
            ) : (
              <p>No players found.</p>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default Team;
