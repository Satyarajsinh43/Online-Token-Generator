import React from "react";
import { useLanguage } from "../context/LanguageContext";
import { Link } from "react-router-dom";
import "./Footer.css";

const Footer = () => {
    const { t } = useLanguage();

    return (
        <footer className="gov-footer">
            <div className="container">
                <div className="footer-links">
                    <div>
                        <h4>{t.quickLinks}</h4>
                        <ul>
                            <li><Link to="/quick-links">Quick Links</Link></li>
                            <li><Link to="/disclaimer">{t.disclaimer}</Link></li>
                            <li><Link to="/privacy-policy">{t.privacy}</Link></li>
                            <li><Link to="/accessibility-statement">{t.accessibility}</Link></li>
                        </ul>
                    </div>
                    <div>
                        <h4>{t.contactUs}</h4>
                        <ul>
                            <li>{t.helpDesk}</li>
                            <li>{t.emailSupport}</li>
                        </ul>
                    </div>
                    <div>
                        <h4>{t.otherSites}</h4>
                        <ul>
                            <li><a href="https://www.india.gov.in/" target="_blank" rel="noopener noreferrer" style={{ color: 'inherit', textDecoration: 'none' }}>{t.indiaPortal}</a></li>
                            <li><a href="https://gujaratindia.gov.in/" target="_blank" rel="noopener noreferrer" style={{ color: 'inherit', textDecoration: 'none' }}>{t.statePortal}</a></li>
                        </ul>
                    </div>
                </div>
                <div className="footer-bottom">
                    <p>{t.copyright}</p>
                    <p>{t.ownedBy}</p>
                </div>
            </div>
        </footer>
    );
};

export default Footer;
