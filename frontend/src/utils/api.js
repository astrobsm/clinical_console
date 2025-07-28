// utils/api.js
// Centralized fetch wrapper to include JWT token in all requests

import { message } from 'antd';

const API_BASE = process.env.REACT_APP_API_BASE || 'http://localhost:5000';

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
  const res = await fetch(
    url.startsWith('http') ? url : `${API_BASE}${url}`,
    { ...options, headers }
  );
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
