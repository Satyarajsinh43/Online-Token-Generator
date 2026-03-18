import React, { useState, useContext } from "react";
import { useNavigate } from "react-router-dom";
import { useLanguage } from "../context/LanguageContext";
import AuthContext from "../context/AuthContext";
import "./Register.css";

const Register = () => {
  const { t } = useLanguage();
  const { registerUser } = useContext(AuthContext);
  const navigate = useNavigate();

  const [formData, setFormData] = useState({
    fullName: "",
    mobile: "",
    email: "",
    password: "",
    confirmPassword: "",
  });

  const [errors, setErrors] = useState({});
  const [passwordStrength, setPasswordStrength] = useState("");

  const validateEmail = (email) => {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
  };

  const calculateStrength = (password) => {
    let strength = 0;
    if (password.length > 5) strength++;
    if (password.length > 7) strength++;
    if (/[A-Z]/.test(password)) strength++;
    if (/[0-9]/.test(password)) strength++;
    if (/[^A-Za-z0-9]/.test(password)) strength++;

    if (strength <= 2) return "weak";
    if (strength <= 4) return "medium";
    return "strong";
  };

  const handleChange = (e) => {
    const { name, value } = e.target;

    if (name === "mobile") {
      if (/^\d*$/.test(value) && value.length <= 10) {
        setFormData({ ...formData, [name]: value });
        if (errors.mobile) setErrors({ ...errors, mobile: "" });
      }
    } else {
      setFormData({ ...formData, [name]: value });
      if (name === "password") {
        setPasswordStrength(calculateStrength(value));
      }
      if (errors[name]) setErrors({ ...errors, [name]: "" });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const newErrors = {};

    if (!formData.fullName.trim()) newErrors.fullName = "Name is required";
    if (formData.mobile.length !== 10) newErrors.mobile = t.invalidMobile;
    if (!validateEmail(formData.email)) newErrors.email = t.invalidEmail;
    if (formData.password.length < 6) newErrors.password = "Password too short";
    if (formData.password !== formData.confirmPassword)
      newErrors.confirmPassword = "Passwords do not match";

    setErrors(newErrors);

    if (Object.keys(newErrors).length === 0) {
      const userData = {
        username: formData.mobile, // Using mobile as username
        password: formData.password,
        email: formData.email,
        first_name: formData.fullName,
        role: 'CUSTOMER' // Default role
      };

      const success = await registerUser(userData);

      if (success) {
        alert("Registration Successful! Please login.");
        navigate('/login');
      }
    }
  };

  const getStrengthLabel = (strength) => {
    if (strength === "weak") return t.weakPass;
    if (strength === "medium") return t.mediumPass;
    if (strength === "strong") return t.strongPass;
    return "";
  };

  return (
    <div className="register-page">
      <div className="container">
        <div className="gov-card register-card">
          <div className="card-header">
            <h2>{t.regTitle}</h2>
            <p>{t.regSubtitle}</p>
          </div>

          <form onSubmit={handleSubmit}>
            <div className="form-group">
              <label>{t.fullName}</label>
              <input
                type="text"
                name="fullName"
                className="gov-input"
                placeholder={t.fullName}
                value={formData.fullName}
                onChange={handleChange}
              />
              {errors.fullName && <span className="error-text">{errors.fullName}</span>}
            </div>

            <div className="form-group">
              <label>{t.mobileLabel}</label>
              <div className="input-with-prefix">
                <span className="prefix">+91</span>
                <input
                  type="text"
                  name="mobile"
                  className="gov-input"
                  placeholder={t.mobilePlaceholder}
                  value={formData.mobile}
                  onChange={handleChange}
                />
              </div>
              {errors.mobile && <span className="error-text">{errors.mobile}</span>}
            </div>

            <div className="form-group">
              <label>{t.email}</label>
              <input
                type="email"
                name="email"
                className="gov-input"
                placeholder={t.email}
                value={formData.email}
                onChange={handleChange}
              />
              {errors.email && <span className="error-text">{errors.email}</span>}
            </div>

            <div className="form-group">
              <label>{t.passwordLabel}</label>
              <input
                type="password"
                name="password"
                className="gov-input"
                placeholder={t.passwordPlaceholder}
                value={formData.password}
                onChange={handleChange}
              />
              {formData.password && (
                <div className={`password-strength ${passwordStrength}`}>
                  <div className="strength-bar">
                    <div className="fill"></div>
                  </div>
                  <span className="strength-label">{getStrengthLabel(passwordStrength)}</span>
                </div>
              )}
              {errors.password && <span className="error-text">{errors.password}</span>}
            </div>

            <div className="form-group">
              <label>{t.confirmPass}</label>
              <input
                type="password"
                name="confirmPassword"
                className="gov-input"
                placeholder={t.confirmPass}
                value={formData.confirmPassword}
                onChange={handleChange}
              />
              {errors.confirmPassword && (
                <span className="error-text">{errors.confirmPassword}</span>
              )}
            </div>

            <div className="form-actions">
              <button type="submit" className="gov-btn gov-btn-primary full-width">
                {t.navRegister}
              </button>
            </div>
          </form>

          <div className="card-footer">
            <p className="login-text">
              {t.alreadyReg} <a href="/login">{t.loginHere}</a>
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Register;
