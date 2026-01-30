import React, { useState } from "react";
import { Link } from "react-router-dom";
import { useLanguage } from "../context/LanguageContext";
import "./ForgotPassword.css";

const ForgotPassword = () => {
    const { t } = useLanguage();
    const [step, setStep] = useState(1); // 1: Input, 2: OTP, 3: New Password, 4: Success
    const [method, setMethod] = useState("mobile"); // 'mobile' | 'email'
    const [identifier, setIdentifier] = useState("");
    const [otp, setOtp] = useState("");
    const [newPassword, setNewPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");
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

    const handleSendOtp = (e) => {
        e.preventDefault();
        setError("");

        if (method === "mobile") {
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

        // Simulate sending OTP
        console.log("Sending OTP to:", { method, identifier });
        setStep(2);
    };

    const handleVerifyOtp = (e) => {
        e.preventDefault();
        setError("");

        // Simulate OTP verification (allow any 6 digit OTP for now)
        if (otp.length !== 6 || !/^\d+$/.test(otp)) {
            setError("Invalid OTP. Please enter a 6-digit code.");
            return;
        }

        console.log("Verifying OTP:", otp);
        setStep(3);
    };

    const handleResetPassword = (e) => {
        e.preventDefault();
        setError("");

        if (newPassword.length < 6) {
            setError("Password must be at least 6 characters");
            return;
        }

        if (newPassword !== confirmPassword) {
            setError("Passwords do not match");
            return;
        }

        console.log("Resetting password for:", identifier, "New Pass:", newPassword);
        setStep(4);
    };

    const renderStep1 = () => (
        <>
            <div className="login-methods">
                <button
                    className={`method-btn ${method === "mobile" ? "active" : ""}`}
                    onClick={() => {
                        setMethod("mobile");
                        setIdentifier("");
                        setError("");
                    }}
                >
                    {t.loginWithMobile}
                </button>
                <button
                    className={`method-btn ${method === "email" ? "active" : ""}`}
                    onClick={() => {
                        setMethod("email");
                        setIdentifier("");
                        setError("");
                    }}
                >
                    {t.loginWithEmail}
                </button>
            </div>

            <form onSubmit={handleSendOtp}>
                <div className="form-group">
                    <label>{method === "mobile" ? t.mobileLabel : t.email}</label>
                    <div className={method === "mobile" ? "input-with-prefix" : ""}>
                        {method === "mobile" && <span className="prefix">+91</span>}
                        <input
                            type={method === "mobile" ? "text" : "email"}
                            className="gov-input"
                            placeholder={method === "mobile" ? t.enterMobile : t.enterEmail}
                            value={identifier}
                            onChange={method === "mobile" ? handleMobileChange : handleEmailChange}
                        />
                    </div>
                    {error && <span className="error-text">{error}</span>}
                </div>

                <div className="form-actions">
                    <button type="submit" className="gov-btn gov-btn-primary full-width">
                        {t.sendOtp}
                    </button>
                </div>
            </form>
        </>
    );

    const renderStep2 = () => (
        <form onSubmit={handleVerifyOtp}>
            <div className="form-group">
                <p className="step-instruction">{t.otpSent}</p>
                <label>{t.otpLabel}</label>
                <input
                    type="text"
                    className="gov-input center-text"
                    placeholder={t.otpPlaceholder}
                    value={otp}
                    maxLength={6}
                    onChange={(e) => {
                        if (/^\d*$/.test(e.target.value)) setOtp(e.target.value);
                        setError("");
                    }}
                />
                {error && <span className="error-text">{error}</span>}
            </div>

            <div className="form-actions">
                <button type="submit" className="gov-btn gov-btn-primary full-width">
                    {t.verifyOtp}
                </button>
            </div>
        </form>
    );

    const renderStep3 = () => (
        <form onSubmit={handleResetPassword}>
            <div className="form-group">
                <label>{t.newPass}</label>
                <input
                    type="password"
                    className="gov-input"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                />
            </div>

            <div className="form-group">
                <label>{t.confirmNewPass}</label>
                <input
                    type="password"
                    className="gov-input"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                />
                {error && <span className="error-text">{error}</span>}
            </div>

            <div className="form-actions">
                <button type="submit" className="gov-btn gov-btn-primary full-width">
                    {t.resetBtn}
                </button>
            </div>
        </form>
    );

    const renderStep4 = () => (
        <div className="success-message">
            <div className="success-icon">✓</div>
            <p>{t.resetSuccess}</p>
        </div>
    );

    return (
        <div className="forgot-password-page">
            <div className="container">
                <div className="gov-card forgot-card">
                    <div className="card-header">
                        <h2>{t.forgotTitle}</h2>
                        <p>{t.forgotSubtitle}</p>
                    </div>

                    {step === 1 && renderStep1()}
                    {step === 2 && renderStep2()}
                    {step === 3 && renderStep3()}
                    {step === 4 && renderStep4()}

                    <div className="card-footer">
                        <Link to="/login" className="back-link">
                            ← {t.backToLogin}
                        </Link>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ForgotPassword;
