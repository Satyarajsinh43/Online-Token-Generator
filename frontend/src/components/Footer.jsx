import React from "react";
import { useLanguage } from "../context/LanguageContext";
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
                            <li>{t.disclaimer}</li>
                            <li>{t.privacy}</li>
                            <li>{t.accessibility}</li>
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
                            <li>{t.indiaPortal}</li>
                            <li>{t.statePortal}</li>
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
