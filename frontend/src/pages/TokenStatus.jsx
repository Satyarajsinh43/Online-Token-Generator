import React from "react";
import "./TokenStatus.css";

const TokenStatus = () => {
  return (
    <div className="status-page">
      <div className="container">

        <div className="page-header">
          <h2>Live Token Status</h2>
          <p>Real-time updates for your appointments</p>
        </div>

        <div className="gov-card status-card">
          <div className="status-header">
            <h3>Your Token Details</h3>
            <span className="live-indicator">● Live</span>
          </div>

          <div className="token-display">
            <div className="main-token">
              <span className="label">Your Token Number</span>
              <div className="number">A-023</div>
            </div>

            <div className="current-status status-waiting">
              Waiting for Turn
            </div>
          </div>

          <div className="details-grid">
            <div className="detail-item">
              <span className="label">Office</span>
              <strong>Mamlatdar Office</strong>
            </div>
            <div className="detail-item">
              <span className="label">Service</span>
              <strong>Income Certificate</strong>
            </div>
            <div className="detail-item">
              <span className="label">Current Token</span>
              <strong>A-021</strong>
            </div>
            <div className="detail-item">
              <span className="label">Est. Wait Time</span>
              <strong>~ 15 Mins</strong>
            </div>
          </div>

          <div className="card-actions centered">
            <button className="gov-btn gov-btn-primary refresh-btn">Refresh Status</button>
          </div>
        </div>

      </div>
    </div>
  );
};

export default TokenStatus;
