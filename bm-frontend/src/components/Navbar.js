import React from "react";
import { Link } from "react-router-dom";

function Navbar({ isAuthenticated, onSignOut }) {
  return (
    <nav className="bg-gray-500 text-white p-3">
      <div className="mx-auto flex items-start justify-between">
        {/* Left: Title and Menu */}
        <div className="flex items-center space-x-10">
          {/* Title */}
          <div className="text-2xl font-bold">Brawl Manager</div>

          {/* Center: Menu */}
          <div className="space-x-6">
            <Link
              to="/dashboard"
              className="text-white no-underline hover:text-gray-400"
            >
              Dashboard
            </Link>
            <Link
              to="/matches"
              className="text-white no-underline hover:text-gray-400"
            >
              Matches
            </Link>
            <Link
              to="/leaderboards"
              className="text-white no-underline hover:text-gray-400"
            >
              Leaderboards
            </Link>
          </div>
        </div>

        {/* Right: User Profile */}
        {isAuthenticated && (
          <div className="flex items-center space-x-4">
            <Link
              to="/profile"
              className="text-white no-underline hover:text-gray-400"
            >
              Profile
            </Link>
            <button
              onClick={onSignOut}
              className="bg-gray-600 hover:bg-gray-800 text-white font-bold py-2 px-4 rounded"
            >
              Sign Out
            </button>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Navbar;
