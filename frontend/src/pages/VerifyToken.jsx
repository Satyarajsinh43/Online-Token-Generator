import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import { useLanguage } from '../context/LanguageContext';
import './VerifyToken.css';

const VerifyToken = () => {
    const { t } = useLanguage();
    const { hash } = useParams();
    const navigate = useNavigate();
    const [inputHash, setInputHash] = useState(hash || '');
    const [verificationResult, setVerificationResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState('');

    useEffect(() => {
        if (hash) {
            verifyToken(hash);
        }
    }, [hash]);

    const verifyToken = async (tokenHash) => {
        if (!tokenHash) return;

        setLoading(true);
        setError('');
        setVerificationResult(null);

        try {
            // Replace with your actual backend URL or configured axios instance
            const response = await axios.get(`http://localhost:8000/api/verify-token/${tokenHash}/`);
            setVerificationResult(response.data);
        } catch (err) {
            if (err.response && err.response.data) {
                setError(err.response.data.message || 'Token verification failed.');
            } else {
                setError('Network error or server is unreachable.');
            }
        } finally {
            setLoading(false);
        }
    };

    const handleSearch = (e) => {
        e.preventDefault();
        if (inputHash.trim()) {
            navigate(`/verify-token/${inputHash.trim()}`);
            verifyToken(inputHash.trim());
        }
    };

    return (
        <div className="verify-container">
            <div className="verify-card">
                <h2>{t.verifyTokenTitle}</h2>
                <p>{t.verifyTokenDesc}</p>

                <form onSubmit={handleSearch} className="verify-form">
                    <input
                        type="text"
                        value={inputHash}
                        onChange={(e) => setInputHash(e.target.value)}
                        placeholder={t.enterTokenHash}
                        required
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? t.verifyingHash : t.verifyBtn}
                    </button>
                </form>

                {error && (
                    <div className="verify-error">
                        <span className="icon">❌</span>
                        {error}
                    </div>
                )}

                {verificationResult && (
                    <div className={`verify-result ${verificationResult.status.toLowerCase()}`}>
                        {verificationResult.status === 'Valid' && (
                            <div className="verified-badge-container">
                                <div className="verified-badge">
                                    <span className="shield-icon">🛡️</span>
                                </div>
                                <h3>{t.authenticToken}</h3>
                                <p className="blockchain-secured-text">{t.securedByPolygon}</p>
                            </div>
                        )}
                        <div className="result-header">
                            {verificationResult.status === 'Valid' ? t.blockchainVerifiedInfo : t.databaseOnlyInfo}
                        </div>
                        <div className="result-details">
                            <p><strong>{t.tokenNumberLabelHash}</strong> {verificationResult.token_number}</p>
                            <p><strong>{t.customerNameLabelHash}</strong> {verificationResult.customer_name}</p>
                            <p><strong>{t.officeHash}</strong> {verificationResult.office_name}</p>
                            <p><strong>{t.serviceHash}</strong> {verificationResult.service_name}</p>
                            <p><strong>{t.dateIssued}</strong> {new Date(verificationResult.created_at).toLocaleString()}</p>

                            {verificationResult.blockchain_tx && (
                                <div className="tx-info">
                                    <p><strong>{t.transactionHash}</strong></p>
                                    <a
                                        href={`https://amoy.polygonscan.com/tx/${verificationResult.blockchain_tx}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="explorer-link"
                                    >
                                        {t.viewOnPolygonExplorer}
                                    </a>
                                </div>
                            )}
                        </div>
                    </div>
                )}
            </div>
        </div>
    );
};

export default VerifyToken;
