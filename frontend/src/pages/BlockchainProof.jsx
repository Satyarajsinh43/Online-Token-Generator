import React from "react";
import "./BlockchainProof.css";

const BlockchainProof = () => {
  return ( 
    <div className="blockchain-page">
      <div className="container">
        
        <div className="page-header centered">
          <h2>Blockchain Verification</h2>
          <p>Verify the authenticity of your token</p>
        </div>

        <div className="gov-card blockchain-card">
          <div className="card-header">
            <h3>Immutable Proof Record</h3>
          </div>

          <div className="proof-details">
            <div className="detail-row">
              <span className="label">Token ID:</span>
              <span className="value">A-023</span>
            </div>
            
            <div className="detail-row">
              <span className="label">Timestamp:</span>
              <span className="value">21-Jan-2026 15:45</span>
            </div>

            <div className="hash-block">
              <span className="label">Previous Hash</span>
              <code>0009af8c1a2e38c71b...</code>
            </div>

            <div className="hash-block">
              <span className="label">Current Hash</span>
              <code className="highlight-hash">8baf12e9c44d18c99a...</code>
            </div>
          </div>

          <div className="verification-status">
            <span className="verified-badge">✔ Token Verified on Blockchain</span>
          </div>
        </div>

      </div>
    </div>
  );
};

export default BlockchainProof;
