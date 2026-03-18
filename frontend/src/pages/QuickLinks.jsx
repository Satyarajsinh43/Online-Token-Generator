import React from "react";
import "./LegalPages.css";
import { Link } from "react-router-dom";
import { useLanguage } from "../context/LanguageContext";

const QuickLinks = () => {
    const { t } = useLanguage();
    return (
        <div className="legal-page">
            <div className="legal-container">
                <div className="legal-header">
                    <h1 className="legal-title">{t.quickLinks}</h1>
                </div>
                <div className="legal-content">
                    <div className="legal-link-grid">
                        <Link to="/book-token" className="legal-link-card">
                            {t.bookAppointment}
                        </Link>
                        <Link to="/token-status" className="legal-link-card">
                            {t.checkTokenStatus}
                        </Link>
                        <a href="https://gujaratindia.gov.in/" target="_blank" rel="noopener noreferrer" className="legal-link-card">
                            {t.statePortal}
                        </a>
                        <a href="https://digitalgujarat.gov.in/" target="_blank" rel="noopener noreferrer" className="legal-link-card">
                            {t.digitalGujarat}
                        </a>
                        <Link to="/disclaimer" className="legal-link-card">
                            {t.disclaimer}
                        </Link>
                        <Link to="/privacy-policy" className="legal-link-card">
                            {t.privacy}
                        </Link>
                        <Link to="/accessibility-statement" className="legal-link-card">
                            {t.accessibility}
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default QuickLinks;
