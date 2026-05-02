import React, { useEffect, useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import AuthContext from '../context/AuthContext';

const RoleRedirect = () => {
    const { user, loading, clerkUser } = useContext(AuthContext);
    const navigate = useNavigate();

    useEffect(() => {
        if (!loading) {
            if (user) {
                if (user.role === 'SUPERADMIN' || user.role === 'OFFICEADMIN') {
                    navigate('/admin-dashboard', { replace: true });
                } else if (user.role === 'EMPLOYEE') {
                    navigate('/staff-dashboard', { replace: true });
                } else {
                    navigate('/', { replace: true });
                }
            } else if (clerkUser===null) {
                // Not signed in
                navigate('/login', { replace: true });
            }
        }
    }, [user, loading, clerkUser, navigate]);

    return (
        <div style={{ display: 'flex', justifyContent: 'center', marginTop: '100px', minHeight: '60vh' }}>
            <h3>Routing to your dashboard...</h3>
        </div>
    );
};

export default RoleRedirect;
