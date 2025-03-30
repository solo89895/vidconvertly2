// Get the current hostname
const hostname = window.location.hostname;

// Determine the backend URL based on the current hostname
export const API_BASE_URL = hostname === 'localhost' || hostname === '127.0.0.1'
    ? 'http://localhost:8000'
    : `http://${hostname}:8000`;

export const API_ENDPOINTS = {
    info: `${API_BASE_URL}/api/info`,
    download: `${API_BASE_URL}/api/download`,
    downloadProgress: `${API_BASE_URL}/api/download-progress`
}; 