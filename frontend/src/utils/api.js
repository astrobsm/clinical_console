// utils/api.js
// Centralized fetch wrapper to include JWT token in all requests

import { message } from 'antd';

// Force HTTPS and add debugging
const API_BASE = process.env.REACT_APP_API_BASE || 'https://clinicalguru-36y53.ondigitalocean.app';

// Ensure API_BASE is always HTTPS
const SECURE_API_BASE = API_BASE.replace('http://', 'https://');

// Debug logging
if (process.env.NODE_ENV === 'development') {
  console.log('API Configuration:', {
    original: API_BASE,
    secure: SECURE_API_BASE,
    env: process.env.REACT_APP_API_BASE
  });
}

export async function authFetch(url, options = {}) {
  const token = localStorage.getItem('jwt');
  const headers = {
    ...(options.headers || {}),
    ...(token ? { Authorization: `Bearer ${token}` } : {}),
    'Content-Type': 'application/json',
  };
  
  if (!token && !url.includes('/auth/')) {
    message.error('Session expired or not logged in. Please log in.');
    throw new Error('No auth token');
  }
  
  // Construct URL and force HTTPS
  const fullUrl = url.startsWith('http') ? url : `${SECURE_API_BASE}${url}`;
  const secureUrl = fullUrl.replace('http://', 'https://');
  
  // Debug logging
  if (process.env.NODE_ENV === 'development') {
    console.log('API Request:', { original: url, fullUrl, secureUrl });
  }
  
  const res = await fetch(secureUrl, { ...options, headers });
  
  if (res.status === 401) {
    message.error('Session expired. Please log in again.');
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    localStorage.removeItem('jwt');
    throw new Error('Unauthorized');
  }
  const data = await res.json().catch(() => ({}));
  if (!res.ok) {
    throw new Error(data.msg || data.error || 'API error');
  }
  return data;
}
