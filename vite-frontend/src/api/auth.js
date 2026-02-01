import { API_BASE_URL } from './config';

const AUTH_KEYS = {
  ACCESS: 'taskledger_access_token',
  REFRESH: 'taskledger_refresh_token',
};

// login function
export async function login(email, password) {
  const res = await fetch(`${API_BASE_URL}/auth/login/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  const data = await res.json();

  if (!res.ok) {
    const msg = data.detail || data.message || data.email?.[0] || data.password?.[0] || 'Login failed';
    throw new Error(typeof msg === 'string' ? msg : JSON.stringify(msg));
  }

  return data;
}

// store tokens 
export function setTokens(access, refresh) {
  localStorage.setItem(AUTH_KEYS.ACCESS, access);
  localStorage.setItem(AUTH_KEYS.REFRESH, refresh);
}

//get stoed access token
export function getAccessToken() {
  return localStorage.getItem(AUTH_KEYS.ACCESS);
}

//Get stored refresh token 
export function getRefreshToken() {
  return localStorage.getItem(AUTH_KEYS.REFRESH);
}

// clear stored tokens or logout
export function clearTokens() {
  localStorage.removeItem(AUTH_KEYS.ACCESS);
  localStorage.removeItem(AUTH_KEYS.REFRESH);
}
