// bm-frontend/src/components/Player.js
import React from "react";

function Player({ player }) {
  return (
    <div class="p-5 w-80">
      <h4 class="text-lg font-bold text-brown-700">{player.name}</h4>
      <div class="md:block">
        <div class="mr-10 flex items-baseline space-x-4">
          <p class="rounded-md text-md font-medium">{player.race}</p>
          <p class="rounded-md text-md font-medium">{player.role}</p>
        </div>
      </div>

      <table class="table-auto w-full border-collapse text-sm">
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
