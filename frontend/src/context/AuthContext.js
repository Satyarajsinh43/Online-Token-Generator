import React, { createContext, useState, useEffect } from 'react';
import { useUser, useAuth, useClerk } from '@clerk/clerk-react';
import axios from 'axios';
import config from '../config';

const AuthContext = createContext();
export default AuthContext;

export const AuthProvider = ({ children }) => {
    const { user: clerkUser, isLoaded: isClerkLoaded, isSignedIn } = useUser();
    const { getToken } = useAuth();
    const { signOut } = useClerk();
    
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(true);
    const [syncError, setSyncError] = useState(null);

    useEffect(() => {
        const syncUserWithBackend = async () => {
            if (!isClerkLoaded) return;
            
            if (isSignedIn && clerkUser) {
                try {
                    const token = await getToken();
                    axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
                    
                    const response = await axios.post(`${config.API_URL}clerk-sync-user/`, {
                        email: clerkUser.primaryEmailAddress?.emailAddress,
                        name: clerkUser.fullName,
                        first_name: clerkUser.firstName,
                        last_name: clerkUser.lastName,
                    });
                    
                    if (response.status === 200 || response.status === 201) {
                        setUser(response.data.user);
                    }
                } catch (error) {
                    console.error("Backend sync failed", error);
                    const errorDetail = error.response?.data?.detail || error.response?.data?.error || error.message;
                    setSyncError(`Backend Error: ${errorDetail}`);
                } finally {
                    setLoading(false);
                }
            } else {
                delete axios.defaults.headers.common['Authorization'];
                setUser(null);
                setSyncError(null);
                setLoading(false);
            }
        };

        syncUserWithBackend();
    }, [isClerkLoaded, isSignedIn, clerkUser, getToken]);

    // Keep dummy methods to prevent breaking existing components
    const loginUser = async () => {
        return true;
    };

    const logoutUser = () => {
        signOut();
    };

    const registerUser = async () => {
        return true;
    };

    let contextData = {
        user: user,
        clerkUser: clerkUser,
        loginUser: loginUser,
        logoutUser: logoutUser,
        registerUser: registerUser,
    };

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? (
                <div style={{ display: 'flex', justifyContent: 'center', marginTop: '100px' }}><p>Loading...</p></div>
            ) : syncError ? (
                <div style={{ textAlign: 'center', marginTop: '100px' }}>
                    <h2 style={{ color: 'red' }}>Authentication Sync Error</h2>
                    <p>{syncError}</p>
                    <p>Please ensure the backend server is running and reachable.</p>
                    <button onClick={() => window.location.reload()} style={{ padding: '10px 20px', cursor: 'pointer' }}>Retry</button>
                    <button onClick={() => signOut()} style={{ padding: '10px 20px', cursor: 'pointer', marginLeft: '10px' }}>Sign Out</button>
                </div>
            ) : children}
        </AuthContext.Provider>
    );
};
