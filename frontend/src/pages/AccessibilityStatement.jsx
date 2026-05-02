import React from "react";
import "./LegalPages.css";
import { useLanguage } from "../context/LanguageContext";

const AccessibilityStatement = () => {
    const { t } = useLanguage();
    return (
        <div className="legal-page">
            <div className="legal-container">
                <div className="legal-header">
                    <h1 className="legal-title">{t.accessibility}</h1>
                </div>
                <div className="legal-content">
                    <p>{t.accessibilityP1}</p>
                    <h3>{t.conformanceStatus}</h3>
                    <p>{t.conformanceP1}</p>
                    <h3>{t.featuresTitle}</h3>
                    <ul>
                        <li>{t.feature1}</li>
                        <li>{t.feature2}</li>
                        <li>{t.feature3}</li>
                        <li>{t.feature4}</li>
                    </ul>
                    <h3>{t.feedbackTitle}</h3>
                    <p>{t.feedbackP1}</p>
                </div>
            </div>
        </div>
    );
};

export default AccessibilityStatement;
