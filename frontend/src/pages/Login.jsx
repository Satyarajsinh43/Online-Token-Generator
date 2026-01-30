import React, { useState } from "react";
import { useLanguage } from "../context/LanguageContext";
import "./Login.css";

const Login = () => {
  const { t } = useLanguage();
  const [loginMethod, setLoginMethod] = useState("mobile"); // 'mobile' or 'email'
  const [identifier, setIdentifier] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");

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

  const handleSubmit = (e) => {
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

    // TODO: Connect to backend authentication
    console.log("Logging in with:", { loginMethod, identifier, password });
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
