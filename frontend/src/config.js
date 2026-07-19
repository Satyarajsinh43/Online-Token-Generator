const isLocal = typeof window !== 'undefined' && (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1');

let rawApiUrl = process.env.REACT_APP_API_URL || (isLocal ? "http://localhost:8000/api/" : "https://online-token-generator-backend.onrender.com/api/");

if (rawApiUrl && !rawApiUrl.endsWith('/')) {
    rawApiUrl += '/';
}

const config = {
    API_URL: rawApiUrl,
};

export default config;
