import React from "react";
import "./BlockchainProof.css";
import { useLanguage } from "../context/LanguageContext";

const BlockchainProof = () => {
  const { t } = useLanguage();
  return (
    <div className="blockchain-page">
      <div className="container">

        <div className="page-header centered">
          <h2>{t.blockchainVerification}</h2>
          <p>{t.verifyTruth}</p>
        </div>

        <div className="gov-card blockchain-card">
          <div className="card-header">
            <h3>{t.immutableProof}</h3>
          </div>

          <div className="proof-details">
            <div className="detail-row">
              <span className="label">{t.tokenIdLabel}</span>
              <span className="value">A-023</span>
            </div>

            <div className="detail-row">
              <span className="label">{t.timestampLabel}</span>
              <span className="value">21-Jan-2026 15:45</span>
            </div>

            <div className="hash-block">
              <span className="label">{t.prevHash}</span>
              <code>0009af8c1a2e38c71b...</code>
            </div>

            <div className="hash-block">
              <span className="label">{t.currHash}</span>
              <code className="highlight-hash">8baf12e9c44d18c99a...</code>
            </div>
          </div>

          <div className="verification-status">
            <span className="verified-badge">{t.tokenVerified}</span>
          </div>
        </div>

      </div>
    </div>
  );
};

export default BlockchainProof;
