import React from "react";
import "./LegalPages.css";
import { useLanguage } from "../context/LanguageContext";

const Disclaimer = () => {
    const { t } = useLanguage();
    return (
        <div className="legal-page">
            <div className="legal-container">
                <div className="legal-header">
                    <h1 className="legal-title">{t.disclaimer}</h1>
                </div>
                <div className="legal-content">
                    <p>{t.disclaimerP1}</p>
                    <h3>{t.limitationOfLiability}</h3>
                    <p>{t.liabilityP1}</p>
                    <h3>{t.externalLinks}</h3>
                    <p>{t.linksP1}</p>
                </div>
            </div>
        </div>
    );
};

export default Disclaimer;
