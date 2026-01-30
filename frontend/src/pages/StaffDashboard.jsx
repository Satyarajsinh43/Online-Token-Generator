import React from "react";
import "./StaffDashboard.css";

const StaffDashboard = () => {
  return (
    <div className="staff-dashboard">
      <div className="container">

        <header className="page-header">
          <h2>Staff Dashboard</h2>
          <p>Government Office Token Management</p>
        </header>

        <div className="staff-stats-grid">
          <div className="gov-card highlight-card">
            <h3>Current Token</h3>
            <p className="token-number">A-023</p>
          </div>

          <div className="gov-card">
            <h3>Next Token</h3>
            <p className="token-number">A-024</p>
          </div>

          <div className="gov-card">
            <h3>Tokens Today</h3>
            <p className="token-number">56</p>
          </div>
        </div>

        <div className="gov-card control-panel">
          <div className="card-header">
            <h3>Counter Controls</h3>
          </div>
          <div className="action-buttons">
            <button className="gov-btn gov-btn-primary large-btn">Call Next Token</button>
            <button className="gov-btn gov-btn-secondary large-btn">Mark Absent</button>
            <button className="gov-btn gov-btn-danger large-btn">End Service</button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default StaffDashboard;
