import React, { useState, useEffect } from 'react';
import './App.css';

// This is a minimal starter template for a React application
// You can use Windsurf to expand this into a full application

function App() {
  const [message, setMessage] = useState<string>('');
  const [loading, setLoading] = useState<boolean>(true);

  useEffect(() => {
    // Simulate API call
    setTimeout(() => {
      setMessage('Windsurf Demo Application');
      setLoading(false);
    }, 1000);
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        {loading ? (
          <p>Loading...</p>
        ) : (
          <>
            <h1>{message}</h1>
            <p>
              Edit <code>src/App.tsx</code> and save to reload.
            </p>
            <p>
              Or use Windsurf to help you build a complete application!
            </p>
          </>
        )}
      </header>
    </div>
  );
}

export default App;
