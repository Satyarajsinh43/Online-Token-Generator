import React, { createContext, useState, useEffect } from 'react';
import { jwtDecode } from "jwt-decode";
import axios from 'axios';
import config from '../config';

const AuthContext = createContext();

export default AuthContext;

export const AuthProvider = ({ children }) => {
    let [user, setUser] = useState(() => localStorage.getItem('authTokens') ? jwtDecode(localStorage.getItem('authTokens')) : null);
    let [authTokens, setAuthTokens] = useState(() => localStorage.getItem('authTokens') ? JSON.parse(localStorage.getItem('authTokens')) : null);
    let [loading, setLoading] = useState(true);

    const loginUser = async (username, password) => {
        try {
            const response = await axios.post(`${config.API_URL}token/`, {
                username: username,
                password: password
            });

            if (response.status === 200) {
                setAuthTokens(response.data);
                setUser(jwtDecode(response.data.access));
                localStorage.setItem('authTokens', JSON.stringify(response.data));
                return true;
            } else {
                alert('Something went wrong!');
                return false;
            }
        } catch (error) {
            console.error("Login failed", error);
            alert("Invalid Credentials");
            return false;
        }
    };

    const logoutUser = () => {
        setAuthTokens(null);
        setUser(null);
        localStorage.removeItem('authTokens');
    };

    const registerUser = async (userData) => {
        try {
            const response = await axios.post(`${config.API_URL}register/`, userData);
            if (response.status === 201) {
                return true;
            }
        } catch (error) {
            console.error("Registration failed", error);
            alert("Registration Failed: " + (error.response?.data?.detail || JSON.stringify(error.response?.data)));
            return false;
        }
    };

    // Axios interceptor to attach token to requests
    useEffect(() => {
        const updateToken = async () => {
            // Implement token refresh logic here if needed
            // For now, we just ensure loading is false
            if (loading) {
                setLoading(false);
            }
        }
        updateToken();
    }, [authTokens, loading]);

    // Customize Axios instance or set default headers
    if (authTokens) {
        axios.defaults.headers.common['Authorization'] = `Bearer ${authTokens.access}`;
    } else {
        delete axios.defaults.headers.common['Authorization'];
    }

    let contextData = {
        user: user,
        authTokens: authTokens,
        loginUser: loginUser,
        logoutUser: logoutUser,
        registerUser: registerUser,
    };

    return (
        <AuthContext.Provider value={contextData}>
            {loading ? <p>Loading...</p> : children}
        </AuthContext.Provider>
    );
};
