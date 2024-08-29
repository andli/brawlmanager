import React from 'react';
import Player from './Player';
import CreateTeamForm from './CreateTeamForm';

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
      <div>
        <h4>Players:</h4>
        {team.players && team.players.length > 0 ? (
          team.players.map(player => (
            <Player key={player.id} player={player} />
          ))
        ) : (
          <p>No players found.</p>
        )}
      </div>
    </div>
  );
}

export default Team;
