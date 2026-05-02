import React from "react";
import "./LegalPages.css";
import { useLanguage } from "../context/LanguageContext";

const PrivacyPolicy = () => {
    const { t } = useLanguage();
    return (
        <div className="legal-page">
            <div className="legal-container">
                <div className="legal-header">
                    <h1 className="legal-title">{t.privacy}</h1>
                </div>
                <div className="legal-content">
                    <p>{t.privacyP1}</p>
                    <h3>{t.infoCollection}</h3>
                    <p>{t.infoP1}</p>
                    <h3>{t.dataSecurity}</h3>
                    <p>{t.securityP1}</p>
                    <h3>{t.dataSharing}</h3>
                    <p>{t.sharingP1}</p>
                    <h3>{t.cookiesTitle}</h3>
                    <p>{t.cookiesP1}</p>
                </div>
            </div>
        </div>
    );
};

export default PrivacyPolicy;
