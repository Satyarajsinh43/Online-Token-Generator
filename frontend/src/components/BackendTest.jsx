import React, { useEffect, useState } from 'react';

const BackendTest = () => {
    const [message, setMessage] = useState('Waiting for backend...');
    const [error, setError] = useState(null);

    useEffect(() => {
        fetch('http://localhost:8000/api/offices/')
            .then(response => {
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                return response.json();
            })
            .then(data => {
                setMessage(`Connected! Found ${data.length} offices.`);
            })
            .catch(err => {
                console.error("Backend connection error:", err);
                setError(err.message);
                setMessage('Failed to connect to backend.');
            });
    }, []);

    return (
        <div style={{ padding: '20px', border: '1px solid #ccc', margin: '20px' }}>
            <h2>Backend Connection Test</h2>
            {error ? (
                <p style={{ color: 'red' }}>Error: {error}</p>
            ) : (
                <p style={{ color: 'green' }}>{message}</p>
            )}
        </div>
    );
};

export default BackendTest;
