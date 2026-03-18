import React, { useState, useEffect } from "react";
import { useLanguage } from "../context/LanguageContext";
import "./BookToken.css"; // Reusing form styles for consistency
import gujaratLocations from "../data/gujarat_locations.json";
import officeMetadata from "../data/office_metadata.json";

const FindOffices = () => {
  const { t } = useLanguage();
  const [districts, setDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState("");
  const [selectedTaluka, setSelectedTaluka] = useState("");
  const [talukas, setTalukas] = useState([]);
  const [offices, setOffices] = useState([]);

  useEffect(() => {
    setDistricts(gujaratLocations);
  }, []);

  const handleDistrictChange = (e) => {
    const districtName = e.target.value;
    setSelectedDistrict(districtName);
    setSelectedTaluka("");
    setTalukas([]);
    setOffices([]);

    if (districtName) {
      const districtData = gujaratLocations.find(d => d.name === districtName);
      if (districtData) {
        setTalukas(districtData.talukas || []);
        setOffices(districtData.offices || []);
      }
    }
  };

  const handleTalukaChange = (e) => {
    const talukaName = e.target.value;
    setSelectedTaluka(talukaName);

    if (talukaName) {
      const talukaData = talukas.find(t => t.name === talukaName);
      if (talukaData) {
        setOffices(talukaData.offices || []);
      }
    } else {
      const districtData = gujaratLocations.find(d => d.name === selectedDistrict);
      if (districtData) {
        setOffices(districtData.offices || []);
      }
    }
  };

  const getOfficeDetails = (officeName) => {
    // Try exact match first
    let details = officeMetadata.office_details[officeName];

    // If not found, try partial match (e.g., "Mamlatdar Office (City)" -> "Mamlatdar Office")
    if (!details) {
      for (const key of Object.keys(officeMetadata.office_details)) {
        if (officeName.includes(key) && key !== "default") {
          details = officeMetadata.office_details[key];
          break;
        }
      }
    }

    // Fallback
    return details || officeMetadata.office_details["default"];
  };

  return (
    <div className="book-token-page">
      <div className="container">
        <div className="gov-card book-token-card">
          <div className="card-header">
            <h2>{t.findOfficesTitle}</h2>
            <p>{t.findOfficesSubtitle}</p>
          </div>

          <div className="form-group">
            <label>{t.selectDistrict}</label>
            <select
              className="gov-input"
              value={selectedDistrict}
              onChange={handleDistrictChange}
            >
              <option value="">{t.allDistricts}</option>
              {districts.map((d) => (
                <option key={d.name} value={d.name}>{d.name}</option>
              ))}
            </select>
          </div>

          <div className="form-group">
            <label>{t.selectTaluka} (Optional)</label>
            <select
              className="gov-input"
              value={selectedTaluka}
              onChange={handleTalukaChange}
              disabled={!selectedDistrict}
            >
              <option value="">{t.allTalukas}</option>
              {talukas.map((t) => (
                <option key={t.name} value={t.name}>{t.name}</option>
              ))}
            </select>
          </div>

          <div className="form-section-header">
            <h3>{t.offices}</h3>
          </div>

          <div className="office-list">
            {offices.length > 0 ? (
              <div className="office-grid">
                {offices.map((office, index) => {
                  const details = getOfficeDetails(office);
                  return (
                    <div key={index} className="office-card-detail">
                      <div className="office-icon-large">🏛️</div>
                      <div className="office-info">
                        <h4>{office}</h4>
                        <p className="office-address">📍 {details.address}</p>
                        <p className="office-meta">📞 {details.contact}</p>
                        <p className="office-meta">🕒 {details.hours}</p>
                      </div>
                    </div>
                  );
                })}
              </div>
            ) : (
              <p className="no-data">
                {selectedDistrict ? t.noTokens : t.searchPlaceholder}
              </p>
            )}
          </div>
        </div>
      </div>

      <style jsx="true">{`
        .office-list {
            margin-top: 1rem;
        }
        .office-grid {
            display: grid;
            gap: 1rem;
        }
        .office-card-detail {
            background: white;
            border: 1px solid #e5e7eb;
            padding: 1.5rem;
            border-radius: 8px;
            display: flex;
            gap: 1.5rem;
            transition: all 0.2s;
            box-shadow: 0 1px 2px rgba(0,0,0,0.05);
        }
        .office-card-detail:hover {
            transform: translateY(-3px);
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            border-color: var(--primary-color);
        }
        .office-icon-large {
            font-size: 2.5rem;
            background: #f3f4f6;
            width: 60px;
            height: 60px;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 50%;
        }
        .office-info h4 {
            margin: 0 0 0.5rem 0;
            color: #1f2937;
            font-size: 1.1rem;
        }
        .office-address {
            margin: 0 0 0.5rem 0;
            color: #4b5563;
            font-size: 0.95rem;
        }
        .office-meta {
            margin: 0 0 0.25rem 0;
            color: #6b7280;
            font-size: 0.9rem;
            font-weight: 500;
        }
        .no-data {
            text-align: center;
            color: #6b7280;
            font-style: italic;
            padding: 2rem;
        }
        @media (max-width: 640px) {
            .office-card-detail {
                flex-direction: column;
                gap: 1rem;
            }
            .office-icon-large {
                width: 50px;
                height: 50px;
                font-size: 2rem;
            }
        }
      `}</style>
    </div>
  );
};

export default FindOffices;
