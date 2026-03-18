import React, { useState, useEffect } from "react";
import axios from "axios";
import config from "../config";
import { useLanguage } from "../context/LanguageContext";
import "./AdminDashboard.css";

const AdminDashboard = () => {
    const { t } = useLanguage();
    const [activeTab, setActiveTab] = useState("dashboard"); // 'dashboard', 'offices', 'employees', 'settings'
    const [stats, setStats] = useState({ totalOffices: 0, totalEmployees: 0, totalTokens: 0, todayTokens: 0 });

    // Offices Pagination State
    const [offices, setOffices] = useState([]);
    const [officePage, setOfficePage] = useState(1);
    const [officeTotalPages, setOfficeTotalPages] = useState(1);
    const [officeNext, setOfficeNext] = useState(null);
    const [officePrev, setOfficePrev] = useState(null);

    const [employees, setEmployees] = useState([]);
    const [loading, setLoading] = useState(true);

    // Filter/Search State
    const [searchTerm, setSearchTerm] = useState("");

    // Forms State
    const [showOfficeForm, setShowOfficeForm] = useState(false);
    const [newOffice, setNewOffice] = useState({ office_name: "", office_code: "", address: "", office_type: "URBAN" });
    const [officeType, setOfficeType] = useState("URBAN");

    const [showStaffForm, setShowStaffForm] = useState(false);
    const [newStaff, setNewStaff] = useState({ first_name: "", last_name: "", email: "", password: "", office_id: "", designation: "Clerk" });

    useEffect(() => {
        fetchInitialData();
    }, []);

    const [debugInfo, setDebugInfo] = useState("No Debug Data");
    const [pageError, setPageError] = useState(null);

    const fetchInitialData = async () => {
        setLoading(true);
        setPageError(null);

        let debugLog = {};

        // Fetch Offices
        try {
            const officeRes = await axios.get(`${config.API_URL}offices/?page=1`);
            debugLog.officeStatus = officeRes.status;
            debugLog.officeDataStub = JSON.stringify(officeRes.data).substring(0, 200); // First 200 chars

            if (officeRes.data.results) {
                setOffices(officeRes.data.results);
                setStats(prev => ({ ...prev, totalOffices: officeRes.data.count }));
                setOfficeNext(officeRes.data.next);
                setOfficePrev(officeRes.data.previous);
                setOfficeTotalPages(Math.ceil(officeRes.data.count / 20));
            } else {
                setOffices(officeRes.data);
                setStats(prev => ({ ...prev, totalOffices: officeRes.data.length }));
            }
        } catch (error) {
            console.error("Error fetching offices:", error);
            setPageError("Error fetching offices: " + error.message);
            debugLog.officeError = error.message;
        }

        // Fetch Employees
        try {
            const empRes = await axios.get(`${config.API_URL}employees/`);
            setEmployees(empRes.data);
            setStats(prev => ({ ...prev, totalEmployees: empRes.data.length }));
        } catch (error) {
            console.error("Error fetching employees:", error);
            debugLog.employeeError = error.message;
        }

        // Fetch Tokens
        try {
            const tokenRes = await axios.get(`${config.API_URL}tokens/`);
            const tokens = tokenRes.data;
            setStats(prev => ({
                ...prev,
                totalTokens: tokens.length,
                todayTokens: tokens.filter(t => new Date(t.created_at).toDateString() === new Date().toDateString()).length
            }));
        } catch (error) {
            console.error("Error fetching tokens:", error);
            debugLog.tokenError = error.message;
        }

        setDebugInfo(JSON.stringify(debugLog, null, 2));
        setLoading(false);
    };

    const fetchOfficesPage = async (url) => {
        if (!url) return;
        setLoading(true);
        try {
            // Fix: Ensure we use the full URL provided by DRF which might include http://localhost...
            // Or if relative, append to API_URL. DRF usually gives full absolute URL.
            // But if running in container/different port, might need adjustment.
            // Simplest is to rely on axios handling the absolute URL, or if it's just path/query params.
            // DRF returns full absolute URL usually.
            const response = await axios.get(url);
            if (response.data.results) {
                setOffices(response.data.results);
                setOfficeNext(response.data.next);
                setOfficePrev(response.data.previous);

                // Extract page number from URL for UI
                const urlObj = new URL(url);
                const page = urlObj.searchParams.get("page") || 1;
                setOfficePage(parseInt(page));
            }
        } catch (error) {
            console.error("Error fetching offices page:", error);
        } finally {
            setLoading(false);
        }
    };

    const handleCreateOffice = async (e) => {
        e.preventDefault();
        try {
            await axios.post(`${config.API_URL}offices/`, { ...newOffice, office_type: officeType });
            alert("Office Created Successfully");
            setShowOfficeForm(false);
            setNewOffice({ office_name: "", office_code: "", address: "", office_type: "URBAN" });
            fetchInitialData(); // Refresh list
        } catch (error) {
            console.error("Error creating office:", error);
            alert("Failed to create office");
        }
    };

    const handleCreateStaff = async (e) => {
        e.preventDefault();
        try {
            await axios.post(`${config.API_URL}create-staff/`, newStaff);
            alert("Staff Member Created Successfully!");
            setShowStaffForm(false);
            setNewStaff({ first_name: "", last_name: "", email: "", password: "", office_id: "", designation: "Clerk" });
            fetchInitialData(); // Refresh Employee list
        } catch (error) {
            console.error("Error creating staff:", error);
            const errMsg = error.response?.data?.error || error.response?.data?.detail || error.response?.data?.message || JSON.stringify(error.response?.data) || error.message;
            alert("Failed to create staff: " + errMsg);
        }
    };


    const renderSidebar = () => (
        <aside className="admin-sidebar">
            <div className="sidebar-header">
                <h3>{t.adminPanel}</h3>
            </div>
            <ul className="sidebar-menu">
                <li className={activeTab === 'dashboard' ? 'active' : ''} onClick={() => setActiveTab('dashboard')}>
                    <span className="icon">📊</span> {t.dashboard}
                </li>
                <li className={activeTab === 'offices' ? 'active' : ''} onClick={() => setActiveTab('offices')}>
                    <span className="icon">🏢</span> {t.offices}
                </li>
                <li className={activeTab === 'employees' ? 'active' : ''} onClick={() => setActiveTab('employees')}>
                    <span className="icon">👥</span> {t.employees}
                </li>
                <li className={activeTab === 'settings' ? 'active' : ''} onClick={() => setActiveTab('settings')}>
                    <span className="icon">⚙️</span> {t.settings}
                </li>
            </ul>
        </aside>
    );

    const renderDashboardOverview = () => (
        <div className="dashboard-overview">
            <div className="stats-grid">
                <div className="stat-card">
                    <div className="stat-icon office-icon">🏢</div>
                    <div className="stat-info">
                        <h3>{stats.totalOffices}</h3>
                        <p>{t.totalOffices}</p>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon employee-icon">👥</div>
                    <div className="stat-info">
                        <h3>{stats.totalEmployees}</h3>
                        <p>{t.activeStaff}</p>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon token-icon">🎫</div>
                    <div className="stat-info">
                        <h3>{stats.todayTokens}</h3>
                        <p>{t.tokensToday}</p>
                    </div>
                </div>
                <div className="stat-card">
                    <div className="stat-icon total-icon">📈</div>
                    <div className="stat-info">
                        <h3>{stats.totalTokens}</h3>
                        <p>{t.totalTokensServed}</p>
                    </div>
                </div>
            </div>

            <div className="recent-activity-section">
                <h3>{t.systemHealth}</h3>
                <div className="health-card">
                    <p>✅ {t.dbConnected}</p>
                    <p>✅ {t.apiOnline}</p>
                    <p>✅ {t.smsGateway}</p>
                </div>
            </div>
        </div>
    );

    const renderOfficesTable = () => (
        <div className="data-section">
            <div className="section-header">
                <h2>{t.manageOffices}</h2>
                <button className="gov-btn gov-btn-primary" onClick={() => setShowOfficeForm(true)}>{t.addNewOfficeBtn}</button>
            </div>

            {showOfficeForm && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h3>{t.addNewOffice}</h3>
                        <form onSubmit={handleCreateOffice}>
                            <div className="form-group">
                                <label>{t.officeNameLabel}</label>
                                <input type="text" className="gov-input" required
                                    value={newOffice.office_name} onChange={e => setNewOffice({ ...newOffice, office_name: e.target.value })} />
                            </div>
                            <div className="form-group">
                                <label>{t.officeCodeLabel}</label>
                                <input type="text" className="gov-input" required
                                    value={newOffice.office_code} onChange={e => setNewOffice({ ...newOffice, office_code: e.target.value })} />
                            </div>
                            <div className="form-group">
                                <label>{t.officeTypeLabel}</label>
                                <select className="gov-input" value={officeType} onChange={e => setOfficeType(e.target.value)}>
                                    <option value="URBAN">Urban</option>
                                    <option value="RURAL">Rural</option>
                                    <option value="RTO">RTO</option>
                                </select>
                            </div>
                            <div className="form-group">
                                <label>{t.address}</label>
                                <input type="text" className="gov-input" required
                                    value={newOffice.address} onChange={e => setNewOffice({ ...newOffice, address: e.target.value })} />
                            </div>
                            <div className="form-actions">
                                <button type="button" className="gov-btn gov-btn-secondary" onClick={() => setShowOfficeForm(false)}>{t.cancelBtn}</button>
                                <button type="submit" className="gov-btn gov-btn-primary">{t.createBtn}</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <div className="table-responsive">
                <table className="gov-table">
                    <thead>
                        <tr>
                            <th>{t.officeNameLabel}</th>
                            <th>{t.officeCodeLabel}</th>
                            <th>{t.type}</th>
                            <th>{t.district}</th>
                            <th>{t.actions}</th>
                        </tr>
                    </thead>
                    <tbody>
                        {offices.map(office => (
                            <tr key={office.id}>
                                <td>{office.office_name}</td>
                                <td>{office.office_code}</td>
                                <td><span className={`badge badge-${office.office_type ? office.office_type.toLowerCase() : 'urban'}`}>{office.office_type || 'URBAN'}</span></td>
                                <td>{office.district_name || 'N/A'}</td>
                                <td>
                                    <button className="btn-icon">✏️</button>
                                    <button className="btn-icon delete">🗑️</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>

            <div className="pagination-controls" style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginTop: '20px' }}>
                <button
                    className="gov-btn gov-btn-secondary"
                    disabled={!officePrev}
                    onClick={() => fetchOfficesPage(officePrev)}
                >
                    Previous
                </button>
                <span>Page {officePage} of {officeTotalPages}</span>
                <button
                    className="gov-btn gov-btn-secondary"
                    disabled={!officeNext}
                    onClick={() => fetchOfficesPage(officeNext)}
                >
                    Next
                </button>
            </div>
        </div>
    );

    const renderEmployeesTable = () => (
        <div className="data-section">
            <div className="section-header">
                <h2>{t.employees} Management</h2>
                <button className="gov-btn gov-btn-primary" onClick={() => setShowStaffForm(true)}>Add New Staff</button>
            </div>

            {showStaffForm && (
                <div className="modal-overlay">
                    <div className="modal-content">
                        <h3>Create Employee Application Access</h3>
                        <form onSubmit={handleCreateStaff}>
                            <div className="form-row">
                                <div className="form-group half-width">
                                    <label>First Name</label>
                                    <input type="text" className="gov-input" required
                                        value={newStaff.first_name} onChange={e => setNewStaff({ ...newStaff, first_name: e.target.value })} />
                                </div>
                                <div className="form-group half-width">
                                    <label>Last Name</label>
                                    <input type="text" className="gov-input" required
                                        value={newStaff.last_name} onChange={e => setNewStaff({ ...newStaff, last_name: e.target.value })} />
                                </div>
                            </div>
                            
                            <div className="form-group">
                                <label>Email Address / Username</label>
                                <input type="email" className="gov-input" required placeholder="staff@gujarat.gov.in"
                                    value={newStaff.email} onChange={e => setNewStaff({ ...newStaff, email: e.target.value })} />
                            </div>

                            <div className="form-group">
                                <label>Password (Temporary)</label>
                                <input type="text" className="gov-input" required placeholder="e.g. securepass123"
                                    value={newStaff.password} onChange={e => setNewStaff({ ...newStaff, password: e.target.value })} />
                            </div>

                            <div className="form-group">
                                <label>Assigned Office</label>
                                <select className="gov-input" required 
                                    value={newStaff.office_id} onChange={e => setNewStaff({ ...newStaff, office_id: e.target.value })}>
                                    <option value="">Select Office</option>
                                    {offices.map(o => (
                                        <option key={o.id} value={o.id}>{o.office_name} ({o.office_type})</option>
                                    ))}
                                </select>
                            </div>

                            <div className="form-group">
                                <label>Designation</label>
                                <input type="text" className="gov-input" required placeholder="Clerk"
                                    value={newStaff.designation} onChange={e => setNewStaff({ ...newStaff, designation: e.target.value })} />
                            </div>

                            <div className="form-actions">
                                <button type="button" className="gov-btn gov-btn-secondary" onClick={() => setShowStaffForm(false)}>{t.cancelBtn}</button>
                                <button type="submit" className="gov-btn gov-btn-primary">Provision Account</button>
                            </div>
                        </form>
                    </div>
                </div>
            )}

            <div className="table-responsive">
                <table className="gov-table">
                    <thead>
                        <tr>
                            <th>Staff Username</th>
                            <th>Designation</th>
                            <th>Assigned Office</th>
                            <th>Active Status</th>
                            <th>{t.actions}</th>
                        </tr>
                    </thead>
                    <tbody>
                        {employees.map(emp => (
                            <tr key={emp.id}>
                                <td>{emp.user_details?.username}</td>
                                <td>{emp.designation}</td>
                                <td>{emp.office_name}</td>
                                <td>
                                    <span className={`badge badge-${emp.active_status ? 'success' : 'cancelled'}`}>
                                        {emp.active_status ? 'Active' : 'Disabled'}
                                    </span>
                                </td>
                                <td>
                                    <button className="btn-icon">✏️</button>
                                    <button className="btn-icon delete">🗑️</button>
                                </td>
                            </tr>
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );

    return (
        <div className="admin-layout">
            {renderSidebar()}
            <main className="admin-content">
                <header className="content-header">
                    <h1>{activeTab === 'dashboard' ? t.dashboard : activeTab === 'offices' ? t.offices : activeTab === 'employees' ? t.employees : activeTab === 'settings' ? t.settings : activeTab}</h1>
                    <div className="user-profile">
                        <span>Super Admin</span>
                        <div className="avatar">A</div>
                    </div>
                </header>

                <div className="content-body">
                    {loading ? <div className="loading-spinner">{t.loading}</div> : (
                        <>
                            {activeTab === 'dashboard' && renderDashboardOverview()}
                            {activeTab === 'offices' && renderOfficesTable()}
                            {activeTab === 'employees' && renderEmployeesTable()}
                            {activeTab === 'settings' && <div className="placeholder-view"><h3>System Settings</h3><p>Coming Soon...</p></div>}
                        </>
                    )}
                </div>
            </main>
        </div>
    );
};

export default AdminDashboard;
