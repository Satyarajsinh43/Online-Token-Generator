import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import ForgotPassword from "./pages/ForgotPassword";
import Register from "./pages/Register";
import CitizenDashboard from "./pages/CitizenDashboard";
import StaffDashboard from "./pages/StaffDashboard";
import AdminDashboard from "./pages/AdminDashboard";
import BookToken from "./pages/BookToken";
import TokenStatus from "./pages/TokenStatus";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";
import BlockchainProof from "./pages/BlockchainProof";
import { LanguageProvider } from "./context/LanguageContext";

function App() {
  return (
    <LanguageProvider>
      <BrowserRouter>
        <Navbar />
        <div style={{ minHeight: '80vh' }}>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/forgot-password" element={<ForgotPassword />} />
            <Route path="/register" element={<Register />} />
            <Route path="/citizen-dashboard" element={<CitizenDashboard />} />
            <Route path="/staff-dashboard" element={<StaffDashboard />} />
            <Route path="/admin-dashboard" element={<AdminDashboard />} />
            <Route path="/book-token" element={<BookToken />} />
            <Route path="/token-status" element={<TokenStatus />} />
            <Route path="/blockchain-proof" element={<BlockchainProof />} />
          </Routes>
        </div>
        <Footer />
      </BrowserRouter>
    </LanguageProvider>
  );
}

export default App;
