import React, { useContext } from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import AuthContext from '../context/AuthContext';

const ProtectedRoute = ({ children, allowedRoles }) => {
    const { user } = useContext(AuthContext);
    const location = useLocation();

    if (!user) {
        // Redirect to login if not logged in
        return <Navigate to="/login" state={{ from: location }} replace />;
    }

    if (allowedRoles && !allowedRoles.includes(user.role)) {
        // If role is not allowed, redirect to home or unauthorized page
        // For now, redirecting to home with an alert (in a real app, show 403)
        return <Navigate to="/" replace />;
    }

    return children;
};

export default ProtectedRoute;
