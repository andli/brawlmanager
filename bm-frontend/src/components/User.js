// bm-frontend/src/components/User.js
import React from 'react';

function User({ user }) {
  return (
    <div>
      <h2>{user.name}</h2>
      <img src={user.picture} alt={`${user.name}'s profile`} width="100" />
      <p>Email: {user.email}</p>
    </div>
  );
}

export default User;
