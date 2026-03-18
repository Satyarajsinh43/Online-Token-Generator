import React from "react";
import "./Home.css";
import { useNavigate } from "react-router-dom";
import { useLanguage } from "../context/LanguageContext";

const Home = () => {
  const navigate = useNavigate();
  const { t } = useLanguage();

  return (
    <div className="gov-home-container">
      {/* Hero Section with Slider Effect */}
      <header className="gov-hero-slider">
        <div className="hero-slide active">
          <div className="hero-overlay-gradient">
            <div className="container hero-content">
              <div className="hero-badge">{t.digitalGujarat}</div>
              <h1>{t.heroTitle}</h1>
              <p className="hero-subtitle">{t.heroSubtitle}</p>
              <div className="hero-actions">
                <button onClick={() => navigate("/book-token")} className="btn-hero primary-hero">{t.btnBook}</button>
                <button onClick={() => navigate("/token-status")} className="btn-hero secondary-hero">{t.btnStatus}</button>
              </div>
            </div>
          </div>
        </div>
      </header>

      {/* Marquee Updates - High Priority */}
      <div className="gov-marquee-section">
        <div className="container marquee-container">
          <span className="marquee-badge">
            <span className="blink-dot"></span>
            {t.latestUpdates}
          </span>
          <marquee behavior="scroll" direction="left" onMouseOver={(e) => e.target.stop()} onMouseOut={(e) => e.target.start()}>
            {t.marqueeText}
          </marquee>
        </div>
      </div>

      {/* Key Dignitaries Section - Government Standard */}
      <section className="gov-section dignitaries-section">
        <div className="container">
          <div className="dignitaries-grid">
            <div className="dignitary-card">
              <div className="image-frame">
                <img
                  src="https://img.etb2bimg.com/files/cp/data_file_17570547440376_15738_1x1.jpg"
                  alt="Governor"
                  referrerPolicy="no-referrer"
                />
              </div>
              <div className="dignitary-info">
                <h4>{t.governorName}</h4>
                <p>{t.governorTitle}</p>
              </div>
            </div>

            <div className="minister-message">
              <h3 className="message-title">{t.ministerQuote}</h3>
              <div className="azadi-logo">
                <img
                  src="https://tse3.mm.bing.net/th/id/OIP.GqsxVafi2hK7i7syvNE_DwAAAA?rs=1&pid=ImgDetMain&o=7&rm=3"
                  alt="Digital India"
                  style={{ height: '60px' }}
                  referrerPolicy="no-referrer"
                />
                <img
                  src="https://tse1.mm.bing.net/th/id/OIP.dqXxVAZB3m8F4y7f8410MgHaFj?w=600&h=450&rs=1&pid=ImgDetMain&o=7&rm=3"
                  alt="G20"
                  style={{ height: '60px' }}
                  referrerPolicy="no-referrer"
                />
              </div>
            </div>

            <div className="dignitary-card">
              <div className="image-frame">
                <img
                  src="https://wikibio.in/wp-content/uploads/2021/09/Bhupendra-Patel.jpg"
                  alt="Chief Minister"
                  referrerPolicy="no-referrer"
                />
              </div>
              <div className="dignitary-info">
                <h4>{t.cmName}</h4>
                <p>{t.cmTitle}</p>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Services Section */}
      <section className="gov-section services-section">
        <div className="container">
          <h2 className="section-title">
            <span className="title-decoration-left"></span>
            {t.citizenServices}
            <span className="title-decoration-right"></span>
          </h2>
          <div className="services-grid">
            <div className="service-card">
              <div className="card-icon-wrapper">
                <div className="icon">🏛️</div>
              </div>
              <h3>{t.mamlatdar}</h3>
              <p>{t.mamlatdarDesc}</p>
              <button className="text-btn" onClick={() => navigate("/book-token")}>{t.applyNow} &rarr;</button>
            </div>
            <div className="service-card">
              <div className="card-icon-wrapper">
                <div className="icon">🚑</div>
              </div>
              <h3>{t.civic}</h3>
              <p>{t.civicDesc}</p>
              <button className="text-btn" onClick={() => navigate("/book-token")}>{t.accessServices} &rarr;</button>
            </div>
            <div className="service-card">
              <div className="card-icon-wrapper">
                <div className="icon">🚗</div>
              </div>
              <h3>{t.rto}</h3>
              <p>{t.rtoDesc}</p>
              <button className="text-btn" onClick={() => navigate("/book-token")}>{t.bookSlot} &rarr;</button>
            </div>
            <div className="service-card">
              <div className="card-icon-wrapper">
                <div className="icon">🌾</div>
              </div>
              <h3>{t.agri}</h3>
              <p>{t.agriDesc}</p>
              <button className="text-btn" onClick={() => navigate("/quick-links")}>{t.viewSchemes} &rarr;</button>
            </div>
          </div>
        </div>
      </section>

      {/* Statistics Parallax Strip */}
      <section className="gov-stats-parallax">
        <div className="stats-overlay">
          <div className="container stats-grid">
            <div className="stat-item">
              <div className="stat-number">1.2M+</div>
              <p>{t.statsIssued}</p>
            </div>
            <div className="stat-item">
              <div className="stat-number">850+</div>
              <p>{t.statsOffices}</p>
            </div>
            <div className="stat-item">
              <div className="stat-number">98%</div>
              <p>{t.statsResolution}</p>
            </div>
            <div className="stat-item">
              <div className="stat-number">24/7</div>
              <p>{t.statsAvailability}</p>
            </div>
          </div>
        </div>
      </section>

      {/* Steps with Process Line */}
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
