import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { checkUserSession } from '../api';

function Home() {
  const navigate = useNavigate();

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const isAuthenticated = await checkUserSession();
        if (isAuthenticated) {
          navigate('/dashboard');
        } else {
          navigate('/login');
        }
      } catch (error) {
        console.error('Error checking user session:', error);
        navigate('/login');
      }
    };

    checkAuth();
  }, [navigate]);

  return <div>Loading...</div>;
}

export default Home;
