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
                    <p>
                        Your privacy is important to us. This privacy policy explains how the Gujarat Online Token System collects,
                        uses, and protects your personal information.
                    </p>
                    <h3>Information Collection</h3>
                    <p>
                        We collect personal information such as your name, mobile number, and email address when you book an appointment.
                        This information is used strictly for the purpose of generating your token, sending OTPs for verification, and
                        providing appointment updates.
                    </p>
                    <h3>Data Security</h3>
                    <p>
                        We implement appropriate technical and organizational measures to protect your personal data against unauthorized
                        access, alteration, disclosure, or destruction.
                    </p>
                    <h3>Data Sharing</h3>
                    <p>
                        We do not sell, trade, or rent your personal identification information to others. We may share generic aggregated
                        demographic information regarding visitors and users with our partners and trusted affiliates for government analysis purposes.
                    </p>
                    <h3>Cookies</h3>
                    <p>
                        Our website may use "cookies" to enhance user experience. You may choose to set your web browser to refuse cookies
                        or to alert you when cookies are being sent.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default PrivacyPolicy;
