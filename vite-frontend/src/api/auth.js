import { API_BASE_URL } from './config';

const AUTH_KEYS = {
  ACCESS: 'taskledger_access_token',
  REFRESH: 'taskledger_refresh_token',
};

// Track refresh attempts to prevent infinite loops
// refreshPromise: tracks ongoing refresh to prevent concurrent refreshes
// refreshAttempted: tracks if we've attempted refresh for the current token
let refreshPromise = null;
let refreshAttempted = false;
let currentAccessToken = null;

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
  // Reset refresh tracking when new tokens are set (new token = new session)
  refreshPromise = null;
  refreshAttempted = false;
  currentAccessToken = access;
}

//get stored access token
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
  // Reset refresh tracking on logout
  refreshPromise = null;
  refreshAttempted = false;
  currentAccessToken = null;
}

// Default avatar 
export const DEFAULT_AVATAR_URL = '/avatars/user_avatar.webp';

// Refresh access token using refresh token
export async function refreshAccessToken() {
  // If already attempting refresh, return the existing promise
  if (refreshPromise) {
    return refreshPromise;
  }

  const refreshToken = getRefreshToken();
  if (!refreshToken) {
    const error = new Error('No refresh token available');
    error.code = 'NO_REFRESH_TOKEN';
    throw error;
  }

  // Prevent multiple simultaneous refresh attempts
  refreshPromise = (async () => {
    try {
      const res = await fetch(`${API_BASE_URL}/auth/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: refreshToken }),
      });

      const data = await res.json();

      if (!res.ok) {
        // Refresh failed - clear tokens
        clearTokens();
        const error = new Error(data.detail || data.message || 'Token refresh failed');
        error.code = 'REFRESH_FAILED';
        throw error;
      }

      // Update tokens
      setTokens(data.access, data.refresh || refreshToken);
      return data.access;
    } finally {
      // Clear the promise so future calls can attempt refresh again
      refreshPromise = null;
    }
  })();

  return refreshPromise;
}

// Fetch current user with automatic token refresh on 401
export async function getMe() {
  const token = getAccessToken();
  if (!token) {
    throw new Error('No access token available');
  }

  // Reset refreshAttempted if token has changed (new token = can retry refresh)
  if (currentAccessToken !== token) {
    refreshAttempted = false;
    currentAccessToken = token;
  }

  // Make initial request
  let res = await fetch(`${API_BASE_URL}/auth/me/`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  // If 401, try to refresh token exactly once per token
  if (res.status === 401 && !refreshAttempted) {
    refreshAttempted = true;
    try {
      const newAccessToken = await refreshAccessToken();
      // Retry with new token
      res = await fetch(`${API_BASE_URL}/auth/me/`, {
        headers: { Authorization: `Bearer ${newAccessToken}` },
      });
      // Update current token tracking
      currentAccessToken = newAccessToken;
    } catch (refreshError) {
      // Refresh failed - clear tokens and throw
      clearTokens();
      throw refreshError;
    }
  }

  // If still not ok after refresh attempt, throw error
  if (!res.ok) {
    if (res.status === 401) {
      // Still 401 after refresh - clear tokens
      clearTokens();
      const error = new Error('Authentication failed');
      error.code = 'AUTH_FAILED';
      throw error;
    }
    const error = new Error(`Request failed with status ${res.status}`);
    error.code = 'REQUEST_FAILED';
    throw error;
  }

  const data = await res.json();
  // Success - reset refresh attempt flag so future 401s can refresh again
  refreshAttempted = false;
  return data;
}
