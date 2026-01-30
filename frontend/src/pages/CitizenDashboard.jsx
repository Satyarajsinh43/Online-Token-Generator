import React from "react";
import "./CitizenDashboard.css";
import { Link } from "react-router-dom";

const CitizenDashboard = () => {
  return (
    <div className="citizen-dashboard">
      <div className="container">
        
        <header className="page-header">
          <h2>Citizen Dashboard</h2>
          <p>Manage your appointments and view status</p>
        </header>

        <div className="dashboard-grid">
          
          <div className="gov-card dashboard-card">
            <h3>Book New Token</h3>
            <p>Select service and book your appointment online to save time.</p>
            <div className="card-actions">
              <Link to="/book-token" className="gov-btn gov-btn-primary">Book Now</Link>
            </div>
          </div>

          <div className="gov-card dashboard-card">
            <h3>Track Token Status</h3>
            <p>Check the live status of your booked tokens and estimated wait time.</p>
            <div className="card-actions">
              <Link to="/token-status" className="gov-btn gov-btn-secondary">Check Status</Link>
            </div>
          </div>

          <div className="gov-card dashboard-card">
            <h3>Office Details</h3>
            <p>Find office locations, contact numbers and working hours.</p>
            <div className="card-actions">
              <button className="gov-btn gov-btn-outline">Find Offices</button>
            </div>
          </div>

        </div>
      </div>
    </div>
  );
};

export default CitizenDashboard;
