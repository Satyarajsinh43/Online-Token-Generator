import React, { useState } from 'react';
import axios from 'axios';
import './Home.css';
import config from '../config';
import { useLanguage } from "../context/LanguageContext";

const TokenStatus = () => {
  const { t } = useLanguage();
  const [tokenCode, setTokenCode] = useState("");
  const [tokenData, setTokenData] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!tokenCode) return;

    setLoading(true);
    setError("");
    setTokenData(null);

    try {
      // Using the check_status action
      const response = await axios.get(`${config.API_URL}tokens/check_status/?token_number=${tokenCode}`);
      setTokenData(response.data);
    } catch (err) {
      console.error(err);
      if (err.response && err.response.status === 404) {
        setError(t.tokenNotFound);
      } else {
        setError(t.errorFetchingStatus);
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="status-container gov-container" style={{ padding: '40px 20px', maxWidth: '800px', margin: '0 auto' }}>
      <h2 className="gov-heading" style={{ textAlign: 'center', marginBottom: '30px' }}>{t.checkTokenStatus}</h2>

      <form onSubmit={handleSearch} style={{ display: 'flex', gap: '10px', justifyContent: 'center', marginBottom: '40px' }}>
        <input
          type="text"
          className="gov-input"
          placeholder={t.enterTokenNumber}
          value={tokenCode}
          onChange={(e) => setTokenCode(e.target.value)}
          style={{ maxWidth: '400px' }}
        />
        <button type="submit" className="gov-btn gov-btn-primary" disabled={loading}>
          {loading ? t.searching : t.search}
        </button>
      </form>

      {error && <div className="gov-alert gov-alert-error">{error}</div>}

      {tokenData && (
        <div className="token-details-card" style={{
          background: 'white',
          padding: '30px',
          borderRadius: '8px',
          boxShadow: '0 4px 15px rgba(0,0,0,0.1)',
          borderTop: '5px solid #FF9933' // Saffron border
        }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderBottom: '1px solid #eee', paddingBottom: '15px', marginBottom: '20px' }}>
            <h3 style={{ margin: 0, color: '#1a237e' }}>{t.token} # {tokenData.token_number}</h3>
            <span style={{
              padding: '5px 15px',
              borderRadius: '20px',
              background: tokenData.status === 'COMPLETED' ? '#e8f5e9' : '#fff3e0',
              color: tokenData.status === 'COMPLETED' ? '#2e7d32' : '#ef6c00',
              fontWeight: 'bold',
              textTransform: 'uppercase'
            }}>
              {tokenData.status}
            </span>
          </div>

          <div className="details-grid" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
            <div>
              <label style={{ color: '#666', fontSize: '0.9rem' }}>{t.customer}</label>
              <div style={{ fontWeight: '500', fontSize: '1.1rem' }}>{tokenData.customer_name}</div>
            </div>
            <div>
              <label style={{ color: '#666', fontSize: '0.9rem' }}>{t.officeName}</label>
              <div style={{ fontWeight: '500', fontSize: '1.1rem' }}>{tokenData.office_name}</div>
            </div>
            <div>
              <label style={{ color: '#666', fontSize: '0.9rem' }}>{t.date}</label>
              <div style={{ fontWeight: '500', fontSize: '1.1rem' }}>{new Date(tokenData.created_at).toLocaleDateString()}</div>
            </div>
            <div>
              <label style={{ color: '#666', fontSize: '0.9rem' }}>{t.time}</label>
              <div style={{ fontWeight: '500', fontSize: '1.1rem' }}>{new Date(tokenData.created_at).toLocaleTimeString()}</div>
            </div>
          </div>

          {(tokenData.status === 'PENDING' || tokenData.status === 'CALLED' || tokenData.status === 'WAITING' || tokenData.status === 'SERVING') && (
            <div style={{ marginTop: '30px', padding: '15px', background: '#f5f5f5', borderRadius: '5px', textAlign: 'center' }}>
              <div style={{ color: '#666' }}>{tokenData.status === 'SERVING' ? t.currentlyAtCounter : t.status}</div>
              <div style={{ fontSize: '1.5rem', fontWeight: 'bold', color: '#1a237e' }}>
                {tokenData.status === 'SERVING' ? t.nowServingStatus : t.waitingInQueueStatus}
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default TokenStatus;
