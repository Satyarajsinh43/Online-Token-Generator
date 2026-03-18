import React, { useState, useEffect } from "react";
import axios from "axios";
import config from "../config";
import { Link } from "react-router-dom";
import { useLanguage } from "../context/LanguageContext";
import "./CitizenDashboard.css";

const CitizenDashboard = () => {
  const { t } = useLanguage();
  const [tokens, setTokens] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTokens = async () => {
      try {
        const response = await axios.get(`${config.API_URL}tokens/`);
        setTokens(response.data);
      } catch (error) {
        console.error("Error fetching tokens:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchTokens();
  }, []);

  const activeTokens = tokens.filter(t => ['PENDING', 'WAITING', 'SERVING'].includes(t.status));
  const historyTokens = tokens.filter(t => ['COMPLETED', 'CANCELLED', 'SKIPPED'].includes(t.status));

  return (
    <div className="citizen-dashboard">
      <div className="container">

        <header className="page-header">
          <h2>{t.dashboardTitle}</h2>
          <p>{t.welcomeUser}</p>
        </header>

        <div className="dashboard-grid">

          <div className="gov-card dashboard-card">
            <h3>{t.bookToken}</h3>
            <p>{t.heroSubtitle}</p>
            <div className="card-actions">
              <Link to="/book-token" className="gov-btn gov-btn-primary">{t.btnBook}</Link>
            </div>
          </div>

          <div className="gov-card dashboard-card">
            <h3>{t.myActiveTokens}</h3>
            {loading ? <p>{t.loading}</p> : (
              <div className="token-list-compact">
                {activeTokens.length > 0 ? (
                  activeTokens.map(token => (
                    <div key={token.id} className="token-item-compact">
                      <span className="token-number-badge">{token.token_number}</span>
                      <div className="token-details">
                        <span className="token-office">{token.office_details?.name || "Office"}</span>
                        <span className={`token-status status-${token.status.toLowerCase()}`}>{token.status}</span>
                      </div>
                    </div>
                  ))
                ) : (
                  <p>{t.noTokens}</p>
                )}
              </div>
            )}
          </div>
        </div>

        {/* Token History Section */}
        <div className="history-section" style={{ marginTop: '30px' }}>
          <h3 style={{ marginBottom: '15px' }}>{t.tokenHistory}</h3>
          {loading ? <p>{t.loading}</p> : (
            <div className="gov-card p-0">
              <table className="gov-table">
                <thead>
                  <tr>
                    <th>{t.tokenNo}</th>
                    <th>{t.office}</th>
                    <th>{t.date}</th>
                    <th>{t.status}</th>
                  </tr>
                </thead>
                <tbody>
                  {historyTokens.length > 0 ? (
                    historyTokens.map(token => (
                      <tr key={token.id}>
                        <td>{token.token_number}</td>
                        <td>{token.office_details?.name || "N/A"}</td>
                        <td>{new Date(token.created_at).toLocaleDateString()}</td>
                        <td><span className={`status-badge status-${token.status.toLowerCase()}`}>{token.status}</span></td>
                      </tr>
                    ))
                  ) : (
                    <tr><td colSpan="4" style={{ textAlign: 'center' }}>{t.noHistory}</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      <style jsx="true">{`
        .token-list-compact {
            display: flex;
            flex-direction: column;
            gap: 10px;
            margin-top: 10px;
        }
        .token-item-compact {
            display: flex;
            align-items: center;
            background: #f8fafc;
            padding: 10px;
            border-radius: 6px;
            border: 1px solid #e2e8f0;
        }
        .token-number-badge {
            background: var(--primary-blue);
            color: white;
            padding: 5px 10px;
            border-radius: 4px;
            font-weight: bold;
            margin-right: 15px;
        }
        .token-details {
            display: flex;
            flex-direction: column;
        }
        .token-office {
            font-weight: 500;
            font-size: 0.9rem;
        }
        .token-status {
            font-size: 0.8rem;
            margin-top: 2px;
        }
        .status-waiting { color: #d97706; }
        .status-serving { color: #16a34a; font-weight: bold; }
        .status-completed { background: #dcfce7; color: #166534; padding: 2px 6px; border-radius: 4px; }
        .status-cancelled { background: #fee2e2; color: #991b1b; padding: 2px 6px; border-radius: 4px; }
        
        .p-0 { padding: 0 !important; overflow: hidden; }
        .gov-table {
            width: 100%;
            border-collapse: collapse;
        }
        .gov-table th, .gov-table td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        .gov-table th {
            background-color: #f8fafc;
            font-weight: 600;
            color: #475569;
        }
      `}</style>
    </div>
  );
};

export default CitizenDashboard;
