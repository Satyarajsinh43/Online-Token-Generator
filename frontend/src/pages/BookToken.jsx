import React, { useState, useEffect, useContext } from "react";
import axios from "axios";
import config from "../config";
import AuthContext from "../context/AuthContext";
import { useLanguage } from "../context/LanguageContext";
import { useNavigate } from "react-router-dom";
import emailjs from '@emailjs/browser';
import "./BookToken.css";

const BookToken = () => {
  const { user } = useContext(AuthContext);
  const { t } = useLanguage();
  const navigate = useNavigate();
  const [districts, setDistricts] = useState([]);
  const [loading, setLoading] = useState(true);

  // Area Type State: 'RURAL', 'URBAN', 'RTO'
  const [areaType, setAreaType] = useState('URBAN');

  const [selectedDistrict, setSelectedDistrict] = useState("");
  const [selectedTaluka, setSelectedTaluka] = useState("");
  const [selectedVillage, setSelectedVillage] = useState("");
  const [selectedOffice, setSelectedOffice] = useState("");
  const [selectedService, setSelectedService] = useState("");

  const [talukas, setTalukas] = useState([]);
  const [villages, setVillages] = useState([]);
  const [offices, setOffices] = useState([]);
  const [services, setServices] = useState([]);

  const [name, setName] = useState(user ? user.first_name || user.username : "");
  const [mobile, setMobile] = useState(user ? user.username : "");
  const [email, setEmail] = useState("");

  // OTP State
  const [otp, setOtp] = useState("");
  const [showOtpInput, setShowOtpInput] = useState(false);
  const [isVerified, setIsVerified] = useState(false);
  const [otpLoading, setOtpLoading] = useState(false);
  const [otpMessage, setOtpMessage] = useState({ text: "", type: "" });

  // Load districts
  useEffect(() => {
    const fetchDistricts = async () => {
      try {
        const response = await axios.get(`${config.API_URL}districts/`, { headers: { Authorization: null } });
        if (Array.isArray(response.data)) {
          setDistricts(response.data);
        } else if (response.data.results) {
          setDistricts(response.data.results);
        }
        setLoading(false);
      } catch (error) {
        console.error("Error fetching districts:", error);
        setLoading(false);
      }
    };
    fetchDistricts();
  }, []);

  // Fetch Services & Reset downstream when Area Type changes
  useEffect(() => {
    setSelectedTaluka("");
    setSelectedVillage("");
    setSelectedOffice("");
    setSelectedService("");
    setVillages([]);
    setOffices([]);

    // Fetch Services for this Area Type
    const fetchServices = async () => {
      try {
        const response = await axios.get(`${config.API_URL}services/?office_type=${areaType}`, { headers: { Authorization: null } });
        setServices(response.data.results || response.data);
      } catch (error) {
        console.error("Error fetching services:", error);
      }
    };
    if (areaType) fetchServices();

    // If RTO, fetch RTO offices immediately if District is selected
    if (areaType === 'RTO' && selectedDistrict) {
      fetchOffices(selectedDistrict, null, null, 'RTO');
    }

  }, [areaType, selectedDistrict]); // Added selectedDistrict dependency for RTO check

  const handleDistrictChange = async (e) => {
    const districtId = e.target.value;
    setSelectedDistrict(districtId);
    setSelectedTaluka("");
    setSelectedVillage("");
    setSelectedOffice("");
    setTalukas([]);
    setVillages([]);
    setOffices([]);

    if (districtId) {
      if (areaType === 'RTO') {
        // RTO: Fetch offices directly for District
        fetchOffices(districtId, null, null, 'RTO');
      } else {
        // Rural/Urban: Fetch Talukas
        try {
          const response = await axios.get(`${config.API_URL}talukas/?district=${districtId}`, { headers: { Authorization: null } });
          const data = response.data;
          setTalukas(Array.isArray(data) ? data : (data.results || []));
        } catch (error) { console.error("Error fetching talukas:", error); }
      }
    }
  };

  const handleTalukaChange = async (e) => {
    const talukaId = e.target.value;
    setSelectedTaluka(talukaId);
    setSelectedVillage("");
    setSelectedOffice("");
    setVillages([]);
    setOffices([]);

    if (talukaId) {
      if (areaType === 'RURAL') {
        try {
          const response = await axios.get(`${config.API_URL}villages/?taluka=${talukaId}`, { headers: { Authorization: null } });
          const data = response.data;
          setVillages(Array.isArray(data) ? data : (data.results || []));
        } catch (error) { console.error("Error fetching villages:", error); }
      } else {
        // Urban: Fetch offices directly under Taluka
        fetchOffices(selectedDistrict, talukaId, null, 'URBAN');
      }
    }
  };

  const handleVillageChange = async (e) => {
    const villageId = e.target.value;
    setSelectedVillage(villageId);
    setSelectedOffice("");
    setOffices([]);

    if (villageId) {
      fetchOffices(selectedDistrict, selectedTaluka, villageId, 'RURAL');
    }
  };

  const fetchOffices = async (distId, talId, vilId, type) => {
    try {
      let url = `${config.API_URL}offices/?district=${distId}&office_type=${type}`;
      if (talId) url += `&taluka=${talId}`;
      if (vilId) url += `&village=${vilId}`;

      const response = await axios.get(url, { headers: { Authorization: null } });
      const res = response.data;
      if (Array.isArray(res)) setOffices(res);
      else if (res.results && Array.isArray(res.results)) setOffices(res.results);
      else setOffices([]);
    } catch (error) {
      console.error("Error fetching offices:", error);
      setOffices([]);
    }
  };

  const handleSendOtp = async () => {
    const contact = email;
    if (!contact || !contact.includes("@")) {
      setOtpMessage({ text: "Please enter a valid Email Address to verify.", type: "error" });
      return;
    }

    setOtpLoading(true);
    setOtpMessage({ text: "", type: "" });
    try {
      const response = await axios.post(`${config.API_URL}send-otp/`, { contact });
      const generatedOtp = response.data.otp;

      // Send it via EmailJS
      const serviceId = "service_lor8naa";
      const templateId = "template_ln655ad";
      const publicKey = "9g8wx1Zge3XNxD6Sg";

      const templateParams = {
        to_email: contact,
        to_name: name || "User",
        otp_code: generatedOtp,
      };

      try {
        emailjs.init(publicKey);
        await emailjs.send(serviceId, templateId, templateParams);
        console.log("EmailJS Send Triggered to", contact, "with OTP:", generatedOtp);
      } catch (emailErr) {
        console.error("EmailJS sending failed:", emailErr);
        // Throw an explicit error to abort the success message
        throw new Error("EmailJS Error: " + (emailErr.text || emailErr.message || "Invalid EmailJS setup or Keys."));
      }

      setShowOtpInput(true);
      setOtpMessage({ text: "OTP sent successfully to your email!", type: "success" });
    } catch (error) {
      console.error("Failed to send OTP:", error);
      let errorMsg = error.response?.data?.error || error.message || "Failed to send OTP";
      setOtpMessage({ text: errorMsg, type: "error" });
    } finally {
      setOtpLoading(false);
    }
  };

  const handleVerifyOtp = async () => {
    const contact = email;
    if (!otp || otp.length !== 6) {
      setOtpMessage({ text: "Please enter a valid 6-digit OTP.", type: "error" });
      return;
    }

    setOtpLoading(true);
    setOtpMessage({ text: "", type: "" });
    try {
      await axios.post(`${config.API_URL}verify-otp/`, { contact, otp });
      setIsVerified(true);
      setOtpMessage({ text: "✓ Email Verified Successfully", type: "success" });
    } catch (error) {
      console.error("OTP Verification failed:", error);
      setOtpMessage({ text: error.response?.data?.error || "Invalid or Expired OTP", type: "error" });
    } finally {
      setOtpLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!selectedOffice) {
      alert("Please select an Office");
      return;
    }
    if (!selectedService) {
      alert("Please select a Type of Work (Service)");
      return;
    }

    if (!name) return alert("Please enter Name");
    if (!email) return alert("Please enter Email");

    // Construct Payload matching BookTokenSerializer
    const payload = {
      customer_name: name,
      customer_phone: mobile,
      email: email, // ensure we can pass email to API if needed
      district_id: selectedDistrict,
      taluka_id: selectedTaluka || null,
      village_id: selectedVillage || null,
      office_id: selectedOffice,
      service_id: selectedService,
    };

    try {
      // Use the new book-token endpoint
      const response = await axios.post(`${config.API_URL}book-token/`, payload);

      // Navigate to Receipt Page
      navigate('/token-receipt', { state: { tokenData: response.data } });

    } catch (error) {
      console.error("Submission Error:", error);
      alert("Failed to generate token. " + (error.response?.data?.error || error.response?.data?.message || JSON.stringify(error.response?.data) || "Please try again."));
    }
  };

  return (
    <div className="book-token-page">
      <div className="container">
        <div className="gov-card book-token-card">
          <div className="card-header">
            <h2>{t.bookAppointment}</h2>
            <p>{t.bookAppointmentDesc}</p>
          </div>

          <form onSubmit={handleSubmit}>
            {/* Personal Details Section */}
            <div className="form-section-header">
              <h3>{t.personalDetails}</h3>
            </div>

            <div className="form-group">
              <label>{t.fullName}</label>
              <input
                type="text"
                className="gov-input"
                placeholder={t.enterFullName}
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="form-group">
              <label>Email Address</label>
              <input
                type="email"
                className="gov-input"
                placeholder="Enter Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={isVerified}
                required
              />
            </div>
            <div className="form-group">
              <label>{t.mobileLabel}</label>
              <input
                type="text"
                className="gov-input"
                placeholder={t.mobilePlaceholder}
                value={mobile}
                onChange={(e) => setMobile(e.target.value)}
                disabled={!!user}
              />
            </div>

            {/* OTP Verification Section */}
            <div className="otp-section">
              {!isVerified && !showOtpInput && (
                <button type="button" className="gov-btn gov-btn-secondary" onClick={handleSendOtp} disabled={otpLoading || !email}>
                  {otpLoading ? "Sending..." : "Send Email OTP"}
                </button>
              )}

              {showOtpInput && !isVerified && (
                <div className="otp-input-group">
                  <input
                    type="text"
                    className="gov-input otp-field"
                    placeholder="Enter 6-digit OTP"
                    value={otp}
                    onChange={(e) => setOtp(e.target.value)}
                    maxLength="6"
                  />
                  <button type="button" className="gov-btn gov-btn-primary" onClick={handleVerifyOtp} disabled={otpLoading}>
                    {otpLoading ? "Verifying..." : "Verify"}
                  </button>
                </div>
              )}

              {otpMessage.text && (
                <p className={`otp-message ${otpMessage.type}`}>{otpMessage.text}</p>
              )}
            </div>

            <hr className="form-divider" />

            {/* Location Details Section */}
            <div className="form-section-header">
              <h3>{t.locationDetails}</h3>
            </div>

            <div className="form-group">
              <label>{t.district}</label>
              <select
                className="gov-input"
                value={selectedDistrict}
                onChange={handleDistrictChange}
                required
              >
                <option value="">{t.selectDistrict}</option>
                {districts.map((d) => (
                  <option key={d.id} value={d.id}>{d.name}</option>
                ))}
              </select>
            </div>

            {/* Area Type Toggle */}
            {selectedDistrict && (
              <div className="form-group">
                <label>{t.areaType}</label>
                <div className="radio-group" style={{ display: 'flex', gap: '15px', marginBottom: '15px', flexWrap: 'wrap' }}>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                    <input
                      type="radio"
                      name="areaType"
                      value="URBAN"
                      checked={areaType === 'URBAN'}
                      onChange={(e) => setAreaType(e.target.value)}
                    />
                    {t.urbanArea}
                  </label>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                    <input
                      type="radio"
                      name="areaType"
                      value="RURAL"
                      checked={areaType === 'RURAL'}
                      onChange={(e) => setAreaType(e.target.value)}
                    />
                    {t.ruralArea}
                  </label>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '8px', cursor: 'pointer' }}>
                    <input
                      type="radio"
                      name="areaType"
                      value="RTO"
                      checked={areaType === 'RTO'}
                      onChange={(e) => setAreaType(e.target.value)}
                    />
                    {t.rtoArea}
                  </label>
                </div>
              </div>
            )}

            <div className="form-row">
              {areaType !== 'RTO' && (
                <div className="form-group half-width">
                  <label>{t.taluka}</label>
                  <select
                    className="gov-input"
                    value={selectedTaluka}
                    onChange={handleTalukaChange}
                    disabled={!selectedDistrict}
                    required={areaType !== 'RTO'}
                  >
                    <option value="">{t.selectTaluka}</option>
                    {talukas.map((t) => (
                      <option key={t.id} value={t.id}>{t.name}</option>
                    ))}
                  </select>
                </div>
              )}

              {areaType === 'RURAL' && (
                <div className="form-group half-width">
                  <label>{t.village}</label>
                  <select
                    className="gov-input"
                    value={selectedVillage}
                    onChange={handleVillageChange}
                    disabled={!selectedTaluka}
                    required
                  >
                    <option value="">{t.selectVillage}</option>
                    {villages.map((v) => (
                      <option key={v.id} value={v.id}>{v.name}</option>
                    ))}
                  </select>
                </div>
              )}
            </div>

            <div className="form-group">
              <label>{t.office}</label>
              <select
                className="gov-input"
                value={selectedOffice}
                onChange={(e) => setSelectedOffice(e.target.value)}
                disabled={!selectedDistrict || (areaType === 'RURAL' && !selectedVillage) || (areaType === 'URBAN' && !selectedTaluka)}
                required
              >
                <option value="">{t.selectOffice}</option>
                {offices.map((off) => (
                  <option key={off.id} value={off.id}>{off.office_name}</option>
                ))}
              </select>
            </div>

            {selectedOffice && (
              <div className="form-group">
                <label>{t.serviceType}</label>
                <select
                  className="gov-input"
                  value={selectedService}
                  onChange={(e) => setSelectedService(e.target.value)}
                  required
                >
                  <option value="">{t.selectService}</option>
                  {services.map((svc) => (
                    <option key={svc.id} value={svc.id}>{svc.name} ({t.approxMins.replace("{time}", svc.avg_time_minutes)})</option>
                  ))}
                </select>
              </div>
            )}

            <div className="form-actions">
              <button
                type="submit"
                className="gov-btn gov-btn-primary full-width secure-btn"
                disabled={loading || !isVerified}
              >
                {!isVerified ? "🔒 Verify Contact to Generate Token" : t.generateToken}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default BookToken;
