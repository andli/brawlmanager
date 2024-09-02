import React from 'react';

function Home() {
    const handleLogin = () => {
        window.location.href = "http://localhost:8000/api/auth/login";  // Adjust the URL if necessary
    };

    return (
        <div>
            <h1>Welcome to BrawlManager</h1>
            <p>Login with your Google account to get started.</p>
            <button onClick={handleLogin}>Login with Google</button>
        </div>
    );
}

export default Home;
