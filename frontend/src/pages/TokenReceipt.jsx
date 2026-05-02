import React, { useRef } from "react";
import { useLocation, useNavigate } from "react-router-dom";
import config from "../config";
import { useLanguage } from "../context/LanguageContext";
import "./TokenReceipt.css"; // We'll create this CSS

const TokenReceipt = () => {
    const { t } = useLanguage();
    const location = useLocation();
    const navigate = useNavigate();
    const tokenData = location.state?.tokenData;
    const printRef = useRef();

    if (!tokenData) {
        return (
            <div className="receipt-container">
                <h2>{t.noReceiptFound}</h2>
                <button onClick={() => navigate('/book-token')}>{t.bookAToken}</button>
            </div>
        );
    }

    const handlePrint = () => {
        window.print();
    };

    return (
        <div className="receipt-page">
            <div className="receipt-card" ref={printRef}>
                <div className="receipt-header">
                    <img src="/logo.png" alt="Gov Logo" className="receipt-logo" onError={(e) => e.target.style.display = 'none'} />
                    <h2>{t.gujaratOnlineTokenSystem}</h2>
                    <p>{t.govName}</p>
                </div>

                <div className="receipt-body">
                    <div className="token-number-box">
                        <span>{t.token}</span>
                        <h1>{tokenData.token_number}</h1>
                    </div>

                    <div className="receipt-details">
                        <div className="detail-row">
                            <span className="label">Booking Date:</span>
                            <span className="value">{tokenData.booking_date || new Date().toLocaleDateString()}</span>
                        </div>
                        <div className="detail-row">
                            <span className="label">Reporting Time Slot:</span>
                            <span className="value">{tokenData.slot_time || new Date().toLocaleTimeString()}</span>
                        </div>
                        <div className="detail-row">
                            <span className="label">{t.applicantName}:</span>
                            <span className="value">{tokenData.customer_name}</span>
                        </div>
                        <div className="detail-row">
                            <span className="label">{t.serviceType}:</span>
                            <span className="value">{tokenData.service_name || t.generalInquiry}</span>
                        </div>
                        <div className="detail-row">
                            <span className="label">{t.officeName}:</span>
                            <span className="value">{tokenData.office_name}</span>
                        </div>
                        {/* Add Location details if available in response */}
                    </div>

                    <div className="receipt-footer">
                        <p>{t.arriveEarly}</p>
                        <p>{t.validForToday}</p>
                    </div>
                </div>
            </div>

            <div className="receipt-actions">
                <button className="gov-btn gov-btn-secondary" onClick={() => navigate('/')}>{t.navHome}</button>
                {tokenData.receipt_url && (
                    <a href={`${config.API_URL}${tokenData.receipt_url.replace('/api/', '')}`} target="_blank" rel="noopener noreferrer" className="gov-btn gov-btn-success" style={{ textDecoration: 'none', display: 'flex', alignItems: 'center' }}>
                        {t.downloadPdf}
                    </a>
                )}
            </div>
        </div>
    );
};

export default TokenReceipt;
