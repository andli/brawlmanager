// bm-frontend/src/components/Team.js
import React from 'react';
import Player from './Player';  // Correctly importing Player

function Team({ team }) {
  return (
    <div>
      <h3>{team.name}</h3>
      <p>Race: {team.race}</p>
      <div>
        <h4>Players:</h4>
        {team.players.length > 0 ? (
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
