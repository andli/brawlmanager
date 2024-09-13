// bm-frontend/src/components/Player.js
import React from "react";

function Player({ player }) {
  return (
    <div className="p-5 w-80">
      <h4 className="text-lg font-bold text-brown-700">{player.name}</h4>
      <div className="md:block">
        <div className="mr-10 flex items-baseline space-x-4">
          <p className="rounded-md text-md font-medium">{player.race}</p>
          <p className="rounded-md text-md font-medium">{player.role}</p>
        </div>
      </div>

      <table className="table-auto w-full border-collapse text-xs">
        <thead>
          <tr className="">
            <th className="border border-gray-700 px-4 py-2">MA</th>
            <th className="border border-gray-700 px-4 py-2">ST</th>
            <th className="border border-gray-700 px-4 py-2">AG</th>
            <th className="border border-gray-700 px-4 py-2">PA</th>
            <th className="border border-gray-700 px-4 py-2">AV</th>
          </tr>
        </thead>
        <tbody>
          <tr>
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
        </tbody>
      </table>
    </div>
  );
}

export default Player; // Ensure this line exists
