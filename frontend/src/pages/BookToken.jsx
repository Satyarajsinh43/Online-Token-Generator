import React from "react";
import "./BookToken.css";

const BookToken = () => {
  return (
    <div className="book-token-page">
      <div className="container">
        <div className="gov-card book-token-card">
          <div className="card-header">
            <h2>Book Appointment</h2>
            <p>Select your preferred office and time slot</p>
          </div>

          <form>
            <div className="form-row">
              <div className="form-group half-width">
                <label>District</label>
                <select className="gov-input">
                  <option>Select District</option>
                  <option>Ahmedabad</option>
                  <option>Vadodara</option>
                  <option>Rajkot</option>
                </select>
              </div>

              <div className="form-group half-width">
                <label>Office Type</label>
                <select className="gov-input">
                  <option>Select Office</option>
                  <option>Mamlatdar Office</option>
                  <option>Taluka Seva Sadan</option>
                  <option>RTO</option>
                </select>
              </div>
            </div>

            <div className="form-group">
              <label>Service</label>
              <select className="gov-input">
                <option>Select Service</option>
                <option>Income Certificate</option>
                <option>Caste Certificate</option>
                <option>Driving License</option>
              </select>
            </div>

            <div className="form-row">
              <div className="form-group half-width">
                <label>Date</label>
                <input type="date" className="gov-input" />
              </div>

              <div className="form-group half-width">
                <label>Time Slot</label>
                <select className="gov-input">
                  <option>Select Slot</option>
                  <option>10:00 – 10:30</option>
                  <option>10:30 – 11:00</option>
                  <option>11:00 – 11:30</option>
                </select>
              </div>
            </div>

            <div className="form-actions">
              <button type="submit" className="gov-btn gov-btn-primary full-width">
                Generate Token
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  );
};

export default BookToken;
