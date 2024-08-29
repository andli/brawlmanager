// bm-frontend/src/components/CreateTeamForm.js
import React, { useState } from 'react';
import axios from 'axios';

function CreateTeamForm({ onTeamCreated }) {
  const [name, setName] = useState('');
  const [race, setRace] = useState('');

  const handleSubmit = async (event) => {
    event.preventDefault();
    
    try {
      const response = await axios.post('/api/teams', { name, race });
      onTeamCreated(response.data);  // Pass the new team back to the parent
    } catch (error) {
      console.error('Error creating team:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Team Name:</label>
        <input type="text" value={name} onChange={(e) => setName(e.target.value)} required />
      </div>
      <div>
        <label>Race:</label>
        <input type="text" value={race} onChange={(e) => setRace(e.target.value)} required />
      </div>
      <button type="submit">Create Team</button>
    </form>
  );
}

export default CreateTeamForm;
