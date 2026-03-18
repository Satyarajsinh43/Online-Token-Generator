import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import axios from 'axios';
import './VerifyToken.css';

const VerifyToken = () => {
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
                <h2>Verify Token Authenticity</h2>
                <p>Enter the blockchain hash from your token receipt or scan the QR code.</p>

                <form onSubmit={handleSearch} className="verify-form">
                    <input
                        type="text"
                        value={inputHash}
                        onChange={(e) => setInputHash(e.target.value)}
                        placeholder="Enter Token Hash (e.g. e4d909c290d0fb1ca068ffaddf22cbd0)"
                        required
                    />
                    <button type="submit" disabled={loading}>
                        {loading ? 'Verifying...' : 'Verify'}
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
                                <h3>Authentic Token</h3>
                                <p className="blockchain-secured-text">Secured by Polygon</p>
                            </div>
                        )}
                        <div className="result-header">
                            {verificationResult.status === 'Valid' ? '✅ Blockchain Verified' : '⚠️ Database Only (Not on Blockchain)'}
                        </div>
                        <div className="result-details">
                            <p><strong>Token Number:</strong> {verificationResult.token_number}</p>
                            <p><strong>Customer Name:</strong> {verificationResult.customer_name}</p>
                            <p><strong>Office:</strong> {verificationResult.office_name}</p>
                            <p><strong>Service:</strong> {verificationResult.service_name}</p>
                            <p><strong>Date Issued:</strong> {new Date(verificationResult.created_at).toLocaleString()}</p>

                            {verificationResult.blockchain_tx && (
                                <div className="tx-info">
                                    <p><strong>Transaction Hash:</strong></p>
                                    <a
                                        href={`https://amoy.polygonscan.com/tx/${verificationResult.blockchain_tx}`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="explorer-link"
                                    >
                                        View on Polygon Explorer
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
