import React from "react";
import { Link, useLocation } from "react-router-dom";
import { useLanguage } from "../context/LanguageContext";
import "./Navbar.css";

const Navbar = () => {
  const location = useLocation();
  const { t, language, toggleLanguage } = useLanguage();

  // Helper to check active state
  const isActive = (path) => location.pathname === path ? "active" : "";

  return (
    <header>
      {/* Top Protocol Bar */}
      <div className="gov-top-bar">
        <div className="container">
          <span>{t.govName}</span>
          <div className="top-links">
            <span onClick={toggleLanguage} style={{ cursor: 'pointer', fontWeight: 'bold', color: 'blue' }}>
              {language === 'en' ? 'ગુજરાતી' : 'English'}
            </span>
            | <span>{t.skipMain}</span> | <span>{t.screenReader}</span> | <span>A+ A-</span>
          </div>
        </div>
      </div>

      {/* Main Navigation */}
      <nav className="gov-navbar">
        <div className="container nav-content">
          <div className="logo-section">
            <Link to="/" style={{ display: 'flex', alignItems: 'center', gap: '15px', textDecoration: 'none' }}>
              <img
                src="https://gandhinagarportal.com/wp-content/uploads/2012/05/government_gujarat_gandhinagar.jpg"
                alt="Emblem"
                className="gov-emblem"
              />
              <div className="logo-text">
                <h1>{t.tokenSystem}</h1>
                <p>{t.portalName}</p>
              </div>
            </Link>
          </div>
          <div className="nav-links">
            <Link to="/" className={isActive("/")}>{t.navHome}</Link>
            <Link to="/citizen-dashboard" className={isActive("/citizen-dashboard")}>{t.navCitizen}</Link>
            <Link to="/staff-dashboard" className={isActive("/staff-dashboard")}>{t.navStaff}</Link>
            <Link to="/admin-dashboard" className={isActive("/admin-dashboard")}>{t.navAdmin}</Link>
            <Link to="/login" className="btn-nav login-btn">{t.navLogin}</Link>
            <Link to="/register" className="btn-nav register-btn">{t.navRegister}</Link>
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Navbar;
