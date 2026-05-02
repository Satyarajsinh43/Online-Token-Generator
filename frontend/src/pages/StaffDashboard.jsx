import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import config from "../config";
import { useLanguage } from "../context/LanguageContext";
import { Link } from "react-router-dom";
import AuthContext from "../context/AuthContext";
import { QrReader } from "react-qr-reader";
import "./StaffDashboard.css";

const StaffDashboard = () => {
  const { t } = useLanguage();
  const { user } = useContext(AuthContext);
  const [selectedToken, setSelectedToken] = useState(null);
  const [tokenQueue, setTokenQueue] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filterDate, setFilterDate] = useState(new Date().toISOString().split('T')[0]);
  const [scannerOpen, setScannerOpen] = useState(false);
  const [manualHash, setManualHash] = useState("");

  // Fetch pending tokens
  const fetchQueue = async () => {
    try {
      setLoading(true);
      const response = await axios.get(`${config.API_URL}tokens/?booking_date=${filterDate}`);
      // Filter for active tokens and completed/cancelled tokens for the day
      const activeTokens = response.data.filter(t => ['WAITING', 'VERIFIED', 'SERVING', 'COMPLETED', 'CANCELLED'].includes(t.status));
      setTokenQueue(activeTokens);
      setError(null);
    } catch (err) {
      console.error("Error fetching queue:", err);
      setError(t.queueError);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchQueue();
    // Poll every 30 seconds
    const interval = setInterval(fetchQueue, 30000);
    return () => clearInterval(interval);
  }, [filterDate]);

  const handleTokenClick = (token) => {
    setSelectedToken(token);
  };

  const closeModal = () => {
    setSelectedToken(null);
  };

  const updateTokenStatus = async (tokenId, newStatus) => {
    try {
      await axios.patch(`${config.API_URL}tokens/${tokenId}/update_status/`, { status: newStatus });
      fetchQueue();
      if (selectedToken && selectedToken.id === tokenId) {
        closeModal();
      }
    } catch (err) {
      console.error("Error updating token:", err);
      alert("Failed to update status. " + (err.response?.data?.error || err.message));
    }
  };

  const verifyToken = async (tokenHash) => {
    if (!tokenHash) {
       alert("Please enter a valid token hash.");
       return;
    }
    try {
      let cleanHash = tokenHash;
      if (tokenHash.includes('/verify-token/')) {
         cleanHash = tokenHash.split('/').pop();
      }
      const response = await axios.post(`${config.API_URL}verify-token/`, { token_hash: cleanHash });
      fetchQueue();
      setManualHash("");
      if (scannerOpen) setScannerOpen(false);
      
      alert(`Token ${response.data.token_number} verified successfully!`);
    } catch (err) {
      console.error("Error verifying token:", err);
      alert("Verification failed: " + (err.response?.data?.error || err.message));
    }
  };

  const getServingToken = () => {
    return tokenQueue.find(t => t.status === 'SERVING');
  };

  const getNextToken = () => {
    // Assuming sorted by id or created_at implicitly or explicitly
    const verified = tokenQueue.filter(t => t.status === 'VERIFIED');
    if (verified.length > 0) return verified[0];
    return tokenQueue.filter(t => t.status === 'WAITING')[0];
  };

  const currentToken = getServingToken() || getNextToken();

  const districtName = user?.district_name || 'Your';

  return (
    <div className="staff-dashboard">
      <div className="container">

        <header className="page-header">
          <h2>Welcome {districtName} Staff</h2>
          <p>Showing Tokens for: {districtName} District</p>
          <div className="date-filter">
             <label htmlFor="bookingDate">Date: </label>
             <input type="date" id="bookingDate" value={filterDate} onChange={e => setFilterDate(e.target.value)} />
          </div>
        </header>

        {loading && <p>{t.loadingQueue}</p>}
        {error && <p className="error-text">{error}</p>}

        {!loading && !error && (
          <>
            <div className="staff-stats-grid">
              {/* Current Token */}
              <div className="gov-card highlight-card" onClick={() => currentToken && handleTokenClick(currentToken)} style={{ cursor: 'pointer' }}>
                <h3>{getServingToken() ? t.servingNow : t.nextInQueue}</h3>
                <p className="token-number">{currentToken ? currentToken.token_number : t.none}</p>
                <p style={{ fontSize: '0.9rem', opacity: 0.9 }}>{t.tokenDetails}</p>
              </div>

              <div className="gov-card">
                <h3>{t.pendingVerified}</h3>
                <p className="token-number">{tokenQueue.filter(t => t.status === 'WAITING' || t.status === 'VERIFIED').length}</p>
              </div>

              <div className="gov-card">
                <h3>{t.todaysTotal}</h3>
                <p className="token-number">{tokenQueue.length}</p> {/* Only shows active, ideally fetch total count from another endpoint */}
              </div>
            </div>

            <div className="dashboard-content">
              {/* Control Panel */}
              <div className="gov-card control-panel">
                <div className="card-header">
                  <h3>{t.actionPanel}</h3>
                </div>
                <div className="verification-section" style={{ marginBottom: '20px', padding: '15px', background: '#f8fafc', borderRadius: '8px' }}>
                  <h4>{t.secureVerification}</h4>
                  <div style={{ display: 'flex', gap: '10px', marginTop: '10px' }}>
                     <input 
                       type="text" 
                       placeholder={t.enterHashManually} 
                       value={manualHash}
                       onChange={(e) => setManualHash(e.target.value)}
                       style={{ flex: 1, padding: '8px', borderRadius: '4px', border: '1px solid #ccc' }}
                     />
                     <button className="gov-btn gov-btn-primary" onClick={() => verifyToken(manualHash)}>{t.verifyBtnTxt}</button>
                  </div>
                  <div style={{ marginTop: '10px', textAlign: 'center', display: 'flex', gap: '10px', justifyContent: 'center' }}>
                     <button className="gov-btn gov-btn-secondary" onClick={() => setScannerOpen(!scannerOpen)}>
                       {scannerOpen ? t.closeCamera : t.scanQrCode}
                     </button>
                     <Link to="/verify-token" className="gov-btn gov-btn-secondary" style={{textDecoration: 'none'}}>Advanced Verification</Link>
                  </div>
                  {scannerOpen && (
                     <div style={{ marginTop: '15px', border: '2px dashed #cbd5e1', borderRadius: '8px', overflow: 'hidden' }}>
                       <QrReader
                          onResult={(result, error) => {
                            if (result) {
                               verifyToken(result?.text);
                            }
                          }}
                          style={{ width: '100%' }}
                       />
                     </div>
                  )}
                </div>

                <div className="action-buttons">
                  <h4 style={{marginBottom: "10px", fontSize: "0.9rem", color: "#666"}}>{t.queueActions}</h4>
                  {currentToken ? (
                    <>
                      {currentToken.status === 'VERIFIED' && (
                        <button className="gov-btn gov-btn-primary large-btn" onClick={() => updateTokenStatus(currentToken.id, 'SERVING')}>{t.callNextBtn}</button>
                      )}
                      {currentToken.status === 'SERVING' && (
                        <button className="gov-btn gov-btn-success large-btn" onClick={() => updateTokenStatus(currentToken.id, 'COMPLETED')}>{t.completeBtn}</button>
                      )}
                      <button className="gov-btn gov-btn-danger large-btn" onClick={() => updateTokenStatus(currentToken.id, 'CANCELLED')}>{t.cancelSkipBtn}</button>
                    </>
                  ) : (
                    <p>{t.noPendingTokens}</p>
                  )}
                </div>
              </div>

              {/* Queue List */}
              <div className="gov-card queue-panel">
                <div className="card-header">
                  <h3>{t.pendingQueue}</h3>
                </div>
                <div className="queue-list">
                  {tokenQueue.map((token) => (
                    <div
                      key={token.id}
                      className={`queue-item ${token.status === 'SERVING' ? 'active-serving' : ''}`}
                      onClick={() => handleTokenClick(token)}
                    >
                      <span className="q-number">{token.token_number}</span>
                      <div className="q-info">
                        <span className="q-name">{token.customer_name}</span>
                        <span className="q-service">{t.officeToken}</span>
                      </div>
                      <span className={`q-status status-${token.status.toLowerCase()}`}>
                        {token.status}
                      </span>
                    </div>
                  ))}
                  {tokenQueue.length === 0 && <p style={{ padding: '20px', textAlign: 'center' }}>{t.noPendingTokens}</p>}
                </div>
              </div>
            </div>
          </>
        )}

        {/* Token Details Modal */}
        {selectedToken && (
          <div className="modal-overlay" onClick={closeModal}>
            <div className="modal-content" onClick={(e) => e.stopPropagation()}>
              <div className="modal-header">
                <h3>{t.tokenDetails}</h3>
                <button className="close-btn" onClick={closeModal}>&times;</button>
              </div>
              <div className="modal-body">
                <div className="detail-row">
                  <span className="label">{t.tokenNumberLabel}</span>
                  <span className="value highlight">{selectedToken.token_number}</span>
                </div>
                <div className="detail-row">
                  <span className="label">{t.customerNameLabel}</span>
                  <span className="value">{selectedToken.customer_name}</span>
                </div>
                <div className="detail-row">
                  <span className="label">{t.statusLabel}</span>
                  <span className={`value status-badge`}>
                    {selectedToken.status === 'VERIFIED' ? '✔ Verified' : selectedToken.status}
                  </span>
                </div>
                <div className="detail-row" style={{ flexDirection: 'column', alignItems: 'flex-start' }}>
                  <span className="label">Token Hash (Blockchain)</span>
                  <span className="value" style={{ wordBreak: 'break-all', fontSize: '0.85rem', color: '#666', marginTop: '5px', textAlign: 'left' }}>
                    {selectedToken.token_hash || 'Not available'}
                  </span>
                </div>
                {selectedToken.status === 'VERIFIED' && (
                  <>
                  <div className="detail-row">
                    <span className="label">{t.verifiedBy}</span>
                    <span className="value">{selectedToken.verified_by_name || 'Staff'}</span>
                  </div>
                  <div className="detail-row">
                    <span className="label">{t.verifiedTime}</span>
                    <span className="value">{selectedToken.verified_at ? new Date(selectedToken.verified_at).toLocaleTimeString() : 'N/A'}</span>
                  </div>
                  </>
                )}
                <div className="detail-row">
                  <span className="label">{t.createdAtLabel}</span>
                  <span className="value">{new Date(selectedToken.created_at).toLocaleString()}</span>
                </div>
              </div>
              <div className="modal-footer">
                <button className="gov-btn gov-btn-secondary" onClick={closeModal}>{t.close}</button>
                {selectedToken.status === 'VERIFIED' && (
                  <button className="gov-btn gov-btn-primary" onClick={() => updateTokenStatus(selectedToken.id, 'SERVING')}>{t.startServingBtn}</button>
                )}
                {selectedToken.status === 'SERVING' && (
                  <button className="gov-btn gov-btn-success" onClick={() => updateTokenStatus(selectedToken.id, 'COMPLETED')}>{t.completeBtn}</button>
                )}
                <button className="gov-btn gov-btn-danger" onClick={() => updateTokenStatus(selectedToken.id, 'CANCELLED')}>{t.cancelBtn}</button>
              </div>
            </div>
          </div>
        )}

      </div>

      <style jsx="true">{`
        .active-serving {
            background-color: #dcfce7 !important;
            border-left: 4px solid #16a34a;
        }
        .date-filter {
            margin-top: 10px;
            display: flex;
            align-items: center;
            gap: 10px;
            justify-content: center;
        }
        .date-filter input {
            padding: 8px;
            border-radius: 4px;
            border: 1px solid #ccc;
        }
        .dashboard-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-top: 20px;
        }
        .queue-panel {
            max-height: 400px;
            overflow-y: auto;
        }
        .queue-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 12px;
            border-bottom: 1px solid #eee;
            cursor: pointer;
            transition: background 0.2s;
        }
        .queue-item:hover {
            background-color: #f9fafb;
        }
        .q-number {
            font-weight: bold;
            font-size: 1.1rem;
            color: var(--primary-blue);
            width: 80px;
        }
        .q-info {
            flex: 1;
            display: flex;
            flex-direction: column;
        }
        .q-name {
            font-weight: 500;
        }
        .q-status {
            font-size: 0.8rem;
            padding: 2px 8px;
            border-radius: 12px;
            background: #eee;
        }
        .status-serving { background: #dcfce7; color: #166534; }
        .status-waiting { background: #fef9c3; color: #854d0e; }
        .status-verified { background: #dbeafe; color: #1e40af; }

        /* Modal Styles */
        .modal-overlay {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: rgba(0,0,0,0.5);
            display: flex;
            justify-content: center;
            align-items: center;
            z-index: 1000;
            animation: fadeIn 0.2s ease-out;
        }
        .modal-content {
            background: white;
            padding: 25px;
            border-radius: 8px;
            width: 90%;
            max-width: 500px;
            box-shadow: 0 4px 20px rgba(0,0,0,0.2);
            animation: slideUp 0.3s ease-out;
        }
        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            border-bottom: 1px solid #eee;
            padding-bottom: 10px;
        }
        .modal-header h3 { margin: 0; color: var(--primary-blue); }
        .close-btn {
            background: none;
            border: none;
            font-size: 1.5rem;
            cursor: pointer;
            color: #666;
        }
        .detail-row {
            display: flex;
            justify-content: space-between;
            padding: 8px 0;
        }
        .label {
            font-weight: 500;
            color: #555;
        }
        .value {
            font-weight: 600;
            color: #333;
            text-align: right;
        }
        .value.highlight {
            font-size: 1.2rem;
            color: var(--primary-blue);
        }
        .modal-footer {
            margin-top: 20px;
            display: flex;
            justify-content: flex-end;
            gap: 10px;
        }
        .status-badge {
            padding: 4px 10px;
            border-radius: 4px;
        }

        @media (max-width: 768px) {
            .dashboard-content {
                grid-template-columns: 1fr;
            }
        }
        @keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
        @keyframes slideUp { from { transform: translateY(20px); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
      `}</style>
    </div>
  );
};

export default StaffDashboard;
