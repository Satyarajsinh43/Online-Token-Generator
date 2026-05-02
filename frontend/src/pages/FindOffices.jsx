import React, { useState, useEffect } from "react";
import { useLanguage } from "../context/LanguageContext";
import "./BookToken.css";
import gujaratLocations from "../data/gujarat_locations.json";
import officeMetadata from "../data/office_metadata.json";
import { MapContainer, TileLayer, Marker, Popup, useMap } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

import icon from 'leaflet/dist/images/marker-icon.png';
import iconShadow from 'leaflet/dist/images/marker-shadow.png';

let DefaultIcon = L.icon({
    iconUrl: icon,
    shadowUrl: iconShadow,
    iconSize: [25, 41],
    iconAnchor: [12, 41]
});
L.Marker.prototype.options.icon = DefaultIcon;

// Helper to center map
function ChangeView({ center, zoom }) {
  const map = useMap();
  map.setView(center, zoom);
  return null;
}

const FindOffices = () => {
  const { t } = useLanguage();
  const [districts, setDistricts] = useState([]);
  const [selectedDistrict, setSelectedDistrict] = useState("");
  const [selectedTaluka, setSelectedTaluka] = useState("");
  const [talukas, setTalukas] = useState([]);
  const [offices, setOffices] = useState([]);
  
  // GPS & Map State
  const [userLocation, setUserLocation] = useState(null);
  const [isLocating, setIsLocating] = useState(false);
  const [nearestMode, setNearestMode] = useState(false);
  const [mapCenter, setMapCenter] = useState([22.2587, 71.1924]); // Center of Gujarat

  useEffect(() => {
    setDistricts(gujaratLocations);
  }, []);

  const handleDistrictChange = (e) => {
    const districtName = e.target.value;
    setSelectedDistrict(districtName);
    setSelectedTaluka("");
    setTalukas([]);
    setOffices([]);
    setNearestMode(false);

    if (districtName) {
      const districtData = gujaratLocations.find(d => d.name === districtName);
      if (districtData) {
        setTalukas(districtData.talukas || []);
        setOffices(districtData.offices || []);
        
        // Focus map on the first office of this district if posssible
        if (districtData.offices && districtData.offices.length > 0) {
            const firstOffice = getOfficeDetails(districtData.offices[0]);
            if (firstOffice.lat && firstOffice.lng) {
                setMapCenter([firstOffice.lat, firstOffice.lng]);
            }
        }
      }
    }
  };

  const handleTalukaChange = (e) => {
    const talukaName = e.target.value;
    setSelectedTaluka(talukaName);
    setNearestMode(false);

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
    let details = officeMetadata.office_details[officeName];
    if (!details) {
      for (const key of Object.keys(officeMetadata.office_details)) {
        if (officeName.includes(key) && key !== "default") {
          details = officeMetadata.office_details[key];
          break;
        }
      }
    }
    return details || officeMetadata.office_details["default"];
  };

  const calculateDistance = (lat1, lon1, lat2, lon2) => {
    const p = 0.017453292519943295;
    const c = Math.cos;
    const a = 0.5 - c((lat2 - lat1) * p)/2 + 
            c(lat1 * p) * c(lat2 * p) * 
            (1 - c((lon2 - lon1) * p))/2;
    return 12742 * Math.asin(Math.sqrt(a)); // km
  };

  const findNearestOffices = () => {
    setIsLocating(true);
    if (!navigator.geolocation) {
        alert("Geolocation is not supported by your browser");
        setIsLocating(false);
        return;
    }

    navigator.geolocation.getCurrentPosition(
        (position) => {
            const userLat = position.coords.latitude;
            const userLng = position.coords.longitude;
            setUserLocation([userLat, userLng]);
            setMapCenter([userLat, userLng]);
            
            // Collect all unique offices from our static dataset
            let allOffices = new Set();
            gujaratLocations.forEach(d => {
                if (d.offices) d.offices.forEach(o => allOffices.add(o));
                if (d.talukas) {
                    d.talukas.forEach(t => {
                        if (t.offices) t.offices.forEach(o => allOffices.add(o));
                    });
                }
            });

            // Calculate distance for all correctly mapped offices
            const officeWithDistances = Array.from(allOffices).map(officeName => {
                const details = getOfficeDetails(officeName);
                let dist = 999999;
                if (details.lat && details.lng) {
                    dist = calculateDistance(userLat, userLng, details.lat, details.lng);
                }
                return { name: officeName, details, dist };
            });

            // Sort and grab top 5 mapped offices
            officeWithDistances.sort((a, b) => a.dist - b.dist);
            const top5 = officeWithDistances.filter(o => o.dist !== 999999).slice(0, 5).map(o => o.name);
            
            setOffices(top5);
            setNearestMode(true);
            setSelectedDistrict("");
            setSelectedTaluka("");
            setIsLocating(false);
        },
        (error) => {
            console.error("Error getting location", error);
            alert("Unable to retrieve your location. Check your browser permissions.");
            setIsLocating(false);
        }
    );
  };

  // Render markers for actively shown offices
  const activeMarkers = offices.map(officeName => {
      const details = getOfficeDetails(officeName);
      if (details.lat && details.lng) {
          return { name: officeName, ...details };
      }
      return null;
  }).filter(Boolean);

  return (
    <div className="book-token-page">
      <div className="container">
        <div className="gov-card book-token-card" style={{ maxWidth: '1000px' }}>
          <div className="card-header" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
            <div>
                <h2>{t.findOfficesTitle || 'Find Offices'}</h2>
                <p>{t.findOfficesSubtitle || 'Locate government offices near you via GPS or Search'}</p>
            </div>
            <button 
                className="gov-btn gov-btn-primary" 
                onClick={findNearestOffices} 
                disabled={isLocating}
                style={{ display: 'flex', alignItems: 'center', gap: '8px', padding: '10px 20px', fontSize: '1rem', whiteSpace: 'nowrap' }}
            >
                <span>📍</span> {isLocating ? 'Locating...' : 'Use My GPS Location'}
            </button>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) minmax(0, 1fr)', gap: '1rem', marginBottom: '1.5rem' }}>
            <div className="form-group">
                <label>{t.selectDistrict || 'Select District'}</label>
                <select className="gov-input" value={selectedDistrict} onChange={handleDistrictChange}>
                <option value="">{t.allDistricts || 'All Districts'}</option>
                {districts.map((d) => (
                    <option key={d.name} value={d.name}>{d.name}</option>
                ))}
                </select>
            </div>

            <div className="form-group">
                <label>{t.selectTaluka || 'Select Taluka'} (Optional)</label>
                <select className="gov-input" value={selectedTaluka} onChange={handleTalukaChange} disabled={!selectedDistrict}>
                <option value="">{t.allTalukas || 'All Talukas'}</option>
                {talukas.map((t) => (
                    <option key={t.name} value={t.name}>{t.name}</option>
                ))}
                </select>
            </div>
          </div>
          
          {nearestMode && (
              <div style={{ background: '#e0f2fe', color: '#0369a1', padding: '10px 15px', borderRadius: '6px', marginBottom: '15px', fontWeight: 'bold' }}>
                  Showing the nearest offices to your current location (sorted by distance).
              </div>
          )}

          {/* MAP CANVAS */}
          <div className="map-container-wrapper" style={{ height: '400px', width: '100%', borderRadius: '8px', overflow: 'hidden', marginBottom: '2rem', border: '1px solid #e5e7eb', boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.1)' }}>
              <MapContainer center={mapCenter} zoom={7} style={{ height: '100%', width: '100%', zIndex: 1 }}>
                  <ChangeView center={mapCenter} zoom={nearestMode ? 10 : (selectedDistrict ? 9 : 7)} />
                  <TileLayer
                      attribution='&copy; <a href="https://osm.org/copyright">OpenStreetMap</a> contributors'
                      url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  />
                  
                  {/* User Location Marker */}
                  {userLocation && (
                      <Marker position={userLocation}>
                          <Popup>
                              <strong>Your Current Location</strong>
                          </Popup>
                      </Marker>
                  )}

                  {/* Dynamic Office Markers */}
                  {activeMarkers.map((marker, idx) => (
                      <Marker key={idx} position={[marker.lat, marker.lng]}>
                          <Popup minWidth={220}>
                              <div style={{ padding: '5px' }}>
                                <strong style={{ fontSize: '1.1em', color: '#1f2937' }}>{marker.name}</strong><br/>
                                <p style={{ margin: '5px 0', color: '#4b5563' }}>{marker.address}</p>
                                <hr style={{ borderTop: '1px solid #e5e7eb', margin: '8px 0' }} />
                                <strong>Contact:</strong> {marker.contact}<br/>
                                <strong>Hours:</strong> {marker.hours}
                              </div>
                          </Popup>
                      </Marker>
                  ))}
              </MapContainer>
          </div>

          <div className="form-section-header">
            <h3>{t.offices || 'Offices'} {nearestMode && '(Nearest)'}</h3>
          </div>

          <div className="office-list">
            {offices.length > 0 ? (
              <div className="office-grid">
                {offices.map((office, index) => {
                  const details = getOfficeDetails(office);
                  let distanceStr = null;
                  if (nearestMode && userLocation && details.lat) {
                      const d = calculateDistance(userLocation[0], userLocation[1], details.lat, details.lng);
                      distanceStr = `${d.toFixed(1)} km away`;
                  }

                  return (
                    <div key={index} className="office-card-detail" style={nearestMode && index === 0 ? { borderColor: '#10b981', background: '#f0fdf4' } : {}}>
                      <div className="office-icon-large">🏛️</div>
                      <div className="office-info" style={{ flex: 1 }}>
                        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                            <h4>{office}</h4>
                            {distanceStr && <span style={{ background: '#def7ec', color: '#03543f', padding: '3px 8px', borderRadius: '12px', fontSize: '0.8rem', fontWeight: 'bold' }}>{distanceStr}</span>}
                        </div>
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
                {selectedDistrict ? (t.noTokens || 'No offices found in this region.') : (t.searchPlaceholder || 'Select a district or use GPS to find offices.')}
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
