// TEST: Check what API base is being used
console.log('API_BASE from env:', process.env.REACT_APP_API_BASE);
console.log('Default fallback:', 'https://clinicalguru-36y53.ondigitalocean.app');

const API_BASE = process.env.REACT_APP_API_BASE || 'https://clinicalguru-36y53.ondigitalocean.app';
console.log('Final API_BASE:', API_BASE);

// Test URL construction
const testUrl = '/api/patients/';
const fullUrl = testUrl.startsWith('http') ? testUrl : `${API_BASE}${testUrl}`;
console.log('Constructed URL for /api/patients/:', fullUrl);
