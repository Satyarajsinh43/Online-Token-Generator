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
                    <p>
                        The Gujarat Online Token System is committed to ensuring digital accessibility for people with disabilities.
                        We are continually improving the user experience for everyone and applying the relevant accessibility standards.
                    </p>
                    <h3>Conformance Status</h3>
                    <p>
                        We are working towards conforming to the Web Content Accessibility Guidelines (WCAG) 2.1 level AA.
                        These guidelines explain how to make web content more accessible to people with wide range of disabilities.
                    </p>
                    <h3>Features</h3>
                    <ul>
                        <li>Text alternatives for non-text content.</li>
                        <li>Keyboard accessible navigation.</li>
                        <li>Readable and understandable text content.</li>
                        <li>Consistent navigation and identification of elements.</li>
                    </ul>
                    <h3>Feedback</h3>
                    <p>
                        We welcome your feedback on the accessibility of the Gujarat Online Token System. Please let us know if you
                        encounter accessibility barriers on our website.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default AccessibilityStatement;
