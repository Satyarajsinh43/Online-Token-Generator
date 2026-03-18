import React, { useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useLanguage } from "../context/LanguageContext";
import AuthContext from "../context/AuthContext";
import "./Login.css";

const Login = () => {
  const { t } = useLanguage();
  const { loginUser, user } = useContext(AuthContext); // Get loginUser from context
  const navigate = useNavigate();
  const [loginMethod, setLoginMethod] = useState("mobile"); // 'mobile' or 'email'
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

  // Redirect if already logged in
  // Redirect if already logged in
  useEffect(() => {
    console.log("Login useEffect - User:", user);
    if (user) {
      console.log("Redirecting based on role:", user.role);
      if (user.role === 'SUPERADMIN' || user.role === 'OFFICEADMIN') {
          console.log("Navigating to Admin Dashboard");
          navigate('/admin-dashboard');
      }
      else if (user.role === 'EMPLOYEE') {
          console.log("Navigating to Staff Dashboard");
          navigate('/staff-dashboard');
      }
      else {
          console.log("Navigating to Citizen Dashboard");
          navigate('/citizen-dashboard');
      }
    }
  }, [user, navigate]);

  if (user) return null; // Don't render login form if redirecting

  const handleMobileChange = (e) => {
    const value = e.target.value;
    if (/^\d*$/.test(value) && value.length <= 10) {
      setIdentifier(value);
      setError("");
    }
  };

  const handleEmailChange = (e) => {
    setIdentifier(e.target.value);
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    if (loginMethod === "mobile") {
      if (identifier.length !== 10) {
        setError(t.invalidMobile);
        return;
      }
    } else {
      const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
      if (!emailRegex.test(identifier)) {
        setError(t.invalidEmail);
        return;
      }
    }

    const username = identifier;
    const success = await loginUser(username, password);

    if (success) {
      // Navigation will be handled by the effect or redirect logic based on updated user state
      // But since user update might be async, we can check localStorage or wait for re-render
      // However, better to rely on the return value and updated state
      // We can force a check or just let the component re-render and the check at top to handle it
      // Or adding explicit navigation here based on the decoded token
    } else {
      setError(t.invalidCredentials || "Invalid credentials");
    }
  };

  return (
    <div className="login-page">
      <div className="container">
        <div className="gov-card login-card">
          <div className="card-header">
            <h2>{t.loginTitle}</h2>
            <p>{t.loginSubtitle}</p>
          </div>

          <div className="login-methods">
            <button
              className={`method-btn ${loginMethod === "mobile" ? "active" : ""}`}
              onClick={() => {
                setLoginMethod("mobile");
                setIdentifier("");
                setError("");
              }}
            >
              {t.loginWithMobile}
            </button>
            <button
              className={`method-btn ${loginMethod === "email" ? "active" : ""}`}
              onClick={() => {
                setLoginMethod("email");
                setIdentifier("");
                setError("");
              }}
            >
              {t.loginWithEmail}
            </button>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>
                {loginMethod === "mobile" ? t.mobileLabel : t.email}
              </label>
              <div className={loginMethod === "mobile" ? "input-with-prefix" : ""}>
                {loginMethod === "mobile" && <span className="prefix">+91 </span>}
                <input
                  type={loginMethod === "mobile" ? "text" : "email"}
                  className="gov-input"
                  placeholder={
                    loginMethod === "mobile" ? t.enterMobile : t.enterEmail
                  }
                  value={identifier}
                  onChange={
                    loginMethod === "mobile" ? handleMobileChange : handleEmailChange
                  }
                />
              </div>
              {error && <span className="error-text">{error}</span>}
            </div>

            <div className="form-group">
              <label>{t.passwordLabel}</label>
              <input
                type="password"
                className="gov-input"
                placeholder={t.passwordPlaceholder}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </div>

            <div className="form-actions">
              <button type="submit" className="gov-btn gov-btn-primary full-width">
                {t.secureLogin}
              </button>
            </div>
          </form>

          <div className="card-footer">
            <p>
              {t.newUser} <a href="/register">{t.registerNow}</a>
            </p>
            <p className="forgot-password">
              <a href="/forgot-password">{t.forgotPass}</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Login;
