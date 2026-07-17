import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import ForgotPassword from "./pages/ForgotPassword";
import Register from "./pages/Register";
import CitizenDashboard from "./pages/CitizenDashboard";
import StaffDashboard from "./pages/StaffDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import BookToken from "./pages/BookToken";
import TokenReceipt from "./pages/TokenReceipt";
import TokenStatus from "./pages/TokenStatus";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import BlockchainProof from "./pages/BlockchainProof";
import QuickLinks from "./pages/QuickLinks";
import Disclaimer from "./pages/Disclaimer";
import PrivacyPolicy from "./pages/PrivacyPolicy";
import AccessibilityStatement from "./pages/AccessibilityStatement";
import FindOffices from "./pages/FindOffices";
import { AuthProvider } from "./context/AuthContext";
import { LanguageProvider } from "./context/LanguageContext";
import ProtectedRoute from "./components/ProtectedRoute";
import VerifyToken from "./pages/VerifyToken";
import RoleRedirect from "./pages/RoleRedirect";

function App() {
  return (
    <AuthProvider>
      <LanguageProvider>
        <BrowserRouter>
          <Navbar />
          <div id="main-content" style={{ minHeight: '80vh' }}>
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/login" element={<Login />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
              <Route path="/register" element={<Register />} />
              <Route path="/token-receipt" element={<TokenReceipt />} />
              <Route path="/role-redirect" element={<RoleRedirect />} />

              {/* Protected Routes */}
              <Route
                path="/citizen-dashboard"
                element={
                  <ProtectedRoute allowedRoles={['CUSTOMER', 'SUPERADMIN', 'OFFICEADMIN']}>
                    <CitizenDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/staff-dashboard"
                element={
                  <ProtectedRoute allowedRoles={['EMPLOYEE', 'SUPERADMIN', 'OFFICEADMIN']}>
                    <StaffDashboard />
                  </ProtectedRoute>
                }
              />
              <Route
                path="/admin-dashboard"
                element={
                  <ProtectedRoute allowedRoles={['SUPERADMIN', 'OFFICEADMIN']}>
                    <AdminDashboard />
                  </ProtectedRoute>
                }
              />

              <Route
                path="/book-token"
                element={
                  <ProtectedRoute>
                    <BookToken />
                  </ProtectedRoute>
                }
              />
              <Route path="/token-status" element={<TokenStatus />} />
              <Route path="/blockchain-proof" element={<BlockchainProof />} />
              <Route path="/verify-token/:hash?" element={<VerifyToken />} />
              <Route path="/quick-links" element={<QuickLinks />} />
              <Route path="/disclaimer" element={<Disclaimer />} />
              <Route path="/privacy-policy" element={<PrivacyPolicy />} />
              <Route path="/accessibility-statement" element={<AccessibilityStatement />} />
              <Route path="/find-offices" element={<FindOffices />} />
            </Routes>

          </div>
          <Footer />
        </BrowserRouter>
      </LanguageProvider>
    </AuthProvider>
  );
}

export default App;
