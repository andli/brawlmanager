// bm-frontend/src/components/Player.js
import React from 'react';

function Player({ player }) {
  return (
    <div>
      <h4>{player.name}</h4>
      <p>Role: {player.role}</p>
      <p>Race: {player.race}</p>
      <p>Stats: {player.stats.join(', ')}</p>
    </div>
  );
}

export default Player;  // Ensure this line exists
