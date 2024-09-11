// bm-frontend/src/components/Player.js
import React from "react";

function Player({ player }) {
  return (
    <div class="border-4 border-gray-700 p-5 w-80">
      <h4 class="text-lg font-bold text-brown-700">{player.name}</h4>
      <p>
        <strong>Role:</strong> {player.role}
      </p>
      <p>
        <strong>Race:</strong> {player.race}
      </p>

      <table class="table-auto w-full border-collapse mt-4">
        <thead>
          <tr class="">
            <th class="border border-gray-700 px-4 py-2">MA</th>
            <th class="border border-gray-700 px-4 py-2">ST</th>
            <th class="border border-gray-700 px-4 py-2">AG</th>
            <th class="border border-gray-700 px-4 py-2">PA</th>
            <th class="border border-gray-700 px-4 py-2">AV</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td class="border border-gray-700 px-4 py-2">{player.stats[0]}</td>
            <td class="border border-gray-700 px-4 py-2">{player.stats[1]}</td>
            <td class="border border-gray-700 px-4 py-2">{player.stats[2]}</td>
            <td class="border border-gray-700 px-4 py-2">{player.stats[3]}</td>
            <td class="border border-gray-700 px-4 py-2">{player.stats[4]}</td>
          </tr>
        </tbody>
      </table>
    </div>
  );
}

export default Player; // Ensure this line exists
