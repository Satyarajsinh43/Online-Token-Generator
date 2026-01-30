import React from "react";
import "./AdminDashboard.css";

const AdminDashboard = () => {
  return (
    <div className="admin-dashboard">
      <div className="container">

        <header className="page-header">
          <h2>Admin Dashboard</h2>
          <p>System Overview & Configuration</p>
        </header>

        <div className="admin-stats-grid">
          <div className="gov-card stat-card">
            <h3>Total Offices</h3>
            <p className="stat-value">42</p>
          </div>

          <div className="gov-card stat-card">
            <h3>Total Tokens</h3>
            <p className="stat-value">1,245</p>
          </div>

          <div className="gov-card stat-card">
            <h3>Active Counters</h3>
            <p className="stat-value">128</p>
          </div>

          <div className="gov-card stat-card">
            <h3>Pending</h3>
            <p className="stat-value">96</p>
          </div>
        </div>

        <h3 className="section-heading">Quick Actions</h3>

        <div className="admin-actions-grid">
          <div className="gov-card action-card">
            <h4>Manage Offices</h4>
            <p>Add or update government offices</p>
            <button className="gov-btn gov-btn-primary">Manage</button>
          </div>

          <div className="gov-card action-card">
            <h4>Manage Services</h4>
            <p>Configure services and time limits</p>
            <button className="gov-btn gov-btn-primary">Manage</button>
          </div>

          <div className="gov-card action-card">
            <h4>View Reports</h4>
            <p>Daily and monthly statistics</p>
            <button className="gov-btn gov-btn-primary">View</button>
          </div>

          <div className="gov-card action-card">
            <h4>User Management</h4>
            <p>Staff and admin access control</p>
            <button className="gov-btn gov-btn-primary">Manage</button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default AdminDashboard;
