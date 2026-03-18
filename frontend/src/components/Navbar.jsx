import React from "react";
import { Link, useLocation, useNavigate } from "react-router-dom";
import { useLanguage } from "../context/LanguageContext";
import "./Navbar.css";
import AuthContext from "../context/AuthContext";

const Navbar = () => {
  const location = useLocation();
  const { t, language, changeLanguage } = useLanguage();
  const { user, logoutUser } = React.useContext(AuthContext);
  const navigate = useNavigate();

  // Helper to check active state
  const isActive = (path) => location.pathname === path ? "active" : "";

  const handleLogout = () => {
    logoutUser();
    navigate('/');
  };

  return (
    <header>
      {/* Top Protocol Bar */}
      <div className="gov-top-bar">
        <div className="container">
          <span>{t.govName}</span>
          <div className="top-links">
            <span
              onClick={() => changeLanguage('en')}
              style={{ cursor: 'pointer', fontWeight: language === 'en' ? 'bold' : 'normal', color: language === 'en' ? '#000' : 'blue' }}
            >
              English
            </span>
            <span style={{ margin: '0 5px' }}>|</span>
            <span
              onClick={() => changeLanguage('gu')}
              style={{ cursor: 'pointer', fontWeight: language === 'gu' ? 'bold' : 'normal', color: language === 'gu' ? '#000' : 'blue' }}
            >
              ગુજરાતી
            </span>
            <span style={{ margin: '0 5px' }}>|</span>
            <span
              onClick={() => changeLanguage('hi')}
              style={{ cursor: 'pointer', fontWeight: language === 'hi' ? 'bold' : 'normal', color: language === 'hi' ? '#000' : 'blue' }}
            >
              हिंदी
            </span>
            <span style={{ margin: '0 5px' }}>|</span>
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
            <Link to="/book-token" className={isActive("/book-token")}>{t.bookToken || "Book Token"}</Link>
            <Link to="/token-status" className={isActive("/token-status")}>{t.tokenStatus || "Token Status"}</Link>
            <Link to="/citizen-dashboard" className={isActive("/citizen-dashboard")}>{t.navCitizen}</Link>
            <Link to="/staff-dashboard" className={isActive("/staff-dashboard")}>{t.navStaff}</Link>
            <Link to="/admin-dashboard" className={isActive("/admin-dashboard")}>{t.navAdmin}</Link>
            {user ? (
              <button onClick={handleLogout} className="btn-nav login-btn" style={{ border: 'none', cursor: 'pointer' }}>Logout</button>
            ) : (
              <>
                <Link to="/login" className="btn-nav login-btn">{t.navLogin}</Link>
                <Link to="/register" className="btn-nav register-btn">{t.navRegister}</Link>
              </>
            )}
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Navbar;
