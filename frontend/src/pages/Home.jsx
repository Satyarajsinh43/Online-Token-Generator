import React from "react";
import "./Home.css";
import { useNavigate } from "react-router-dom";
import { useLanguage } from "../context/LanguageContext";

const Home = () => {
  const navigate = useNavigate();
  const { t } = useLanguage();

  return (
    <div className="gov-home-container">
      {/* Hero Section */}
      <header className="gov-hero">
        <div className="hero-overlay">
          <div className="container hero-content">
            <h2>{t.heroTitle}</h2>
            <p className="hero-subtitle">{t.heroSubtitle}</p>
            <div className="hero-actions">
              <button onClick={() => navigate("/book-token")} className="btn-hero primary-hero">{t.btnBook}</button>
              <button onClick={() => navigate("/token-status")} className="btn-hero secondary-hero">{t.btnStatus}</button>
            </div>
          </div>
        </div>
      </header>

      {/* Marquee Updates */}
      <div className="gov-marquee">
        <span className="marquee-label">{t.latestUpdates}</span>
        <marquee behavior="scroll" direction="left" onMouseOver={(e) => e.target.stop()} onMouseOut={(e) => e.target.start()}>
          {t.marqueeText}
        </marquee>
      </div>

      {/* Services Section */}
      <section className="gov-section services-section">
        <div className="container">
          <h2 className="section-title">{t.citizenServices}</h2>
          <div className="services-grid">
            <div className="service-card">
              <div className="icon">🏛️</div>
              <h3>{t.mamlatdar}</h3>
              <p>{t.mamlatdarDesc}</p>
            </div>
            <div className="service-card">
              <div className="icon">🚑</div>
              <h3>{t.civic}</h3>
              <p>{t.civicDesc}</p>
            </div>
            <div className="service-card">
              <div className="icon">🚗</div>
              <h3>{t.rto}</h3>
              <p>{t.rtoDesc}</p>
            </div>
            <div className="service-card">
              <div className="icon">🌾</div>
              <h3>{t.agri}</h3>
              <p>{t.agriDesc}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Statistics Strip */}
      <section className="gov-stats">
        <div className="container stats-grid">
          <div className="stat-item">
            <h3>1.2M+</h3>
            <p>{t.statsIssued}</p>
          </div>
          <div className="stat-item">
            <h3>850+</h3>
            <p>{t.statsOffices}</p>
          </div>
          <div className="stat-item">
            <h3>98%</h3>
            <p>{t.statsResolution}</p>
          </div>
          <div className="stat-item">
            <h3>24/7</h3>
            <p>{t.statsAvailability}</p>
          </div>
        </div>
      </section>

      {/* Steps */}
      <section className="gov-section steps-section">
        <div className="container">
          <h2 className="section-title">{t.howItWorks}</h2>
          <div className="steps-流程">
            <div className="step-item">
              <div className="step-number">1</div>
              <h4>{t.step1}</h4>
              <p>{t.step1Desc}</p>
            </div>
             <div className="step-connector"></div>
            <div className="step-item">
              <div className="step-number">2</div>
              <h4>{t.step2}</h4>
              <p>{t.step2Desc}</p>
            </div>
             <div className="step-connector"></div>
            <div className="step-item">
              <div className="step-number">3</div>
              <h4>{t.step3}</h4>
              <p>{t.step3Desc}</p>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
};

export default Home;
