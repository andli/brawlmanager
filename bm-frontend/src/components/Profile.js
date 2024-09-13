// Profile.js
import React, { useEffect, useState } from "react";
import { fetchUser } from "../api";

function Profile({ onSignOut }) {
  const [user, setUser] = useState(null);

  // Load user data when component mounts
  useEffect(() => {
    const loadUserData = async () => {
      try {
        const userData = await fetchUser();
        setUser(userData);
      } catch (error) {
        console.error("Error loading user data:", error);
      }
    };

    loadUserData();
  }, []);

  return (
    <div>
      <h2>Your Profile</h2>
      {user ? (
        <div>
          <img src={user.picture} alt={`${user.name}'s profile`} width="100" />
          <p>Name: {user.name}</p>
          <p>Email: {user.email}</p>
        </div>
      ) : (
        <p>Loading user info...</p>
      )}
    </div>
  );
}

export default Profile;
