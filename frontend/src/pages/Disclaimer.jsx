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
                    <p>
                        The content on this website is for general information and public assistance purposes only.
                        While we strive to keep the information up to date and correct, we make no representations or warranties
                        of any kind, express or implied, about the completeness, accuracy, reliability, suitability, or availability
                        with respect to the website or the information, products, services, or related graphics contained on the website.
                    </p>
                    <h3>Limitation of Liability</h3>
                    <p>
                        In no event will the Gujarat Online Token System be liable for any loss or damage including without limitation,
                        indirect or consequential loss or damage, or any loss or damage whatsoever arising from loss of data or profits
                        arising out of, or in connection with, the use of this website.
                    </p>
                    <h3>External Links</h3>
                    <p>
                        This website provides links to other websites which are not under the control of the Gujarat Online Token System.
                        We have no control over the nature, content, and availability of those sites. The inclusion of any links does not
                        necessarily imply a recommendation or endorse the views expressed within them.
                    </p>
                </div>
            </div>
        </div>
    );
};

export default Disclaimer;
