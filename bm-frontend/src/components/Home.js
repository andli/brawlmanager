import React from 'react';

function Home() {
    const handleLogin = () => {
        window.location.href = "http://localhost:8000/api/auth/login";  // Adjust the URL if necessary
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100 p-6">
            <h1 className="text-4xl font-bold mb-4 text-center text-gray-800">Welcome to BrawlManager</h1>
            <p className="text-lg mb-6 text-center text-gray-600">Login with your Google account to get started.</p>
            <button 
                onClick={handleLogin} 
                className="bg-blue-500 text-white px-6 py-3 rounded-lg shadow-lg hover:bg-blue-600 transition-colors duration-300"
            >
                Login with Google
            </button>
        </div>
    );
}

export default Home;
