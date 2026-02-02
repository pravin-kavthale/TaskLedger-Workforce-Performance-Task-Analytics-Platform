// Configuration for API base URL
// Uses environment variable VITE_API_URL or defaults to '/api'
export const API_BASE_URL = import.meta.env.VITE_API_URL
  ? `${import.meta.env.VITE_API_URL}/accounts/`
  : '/api/accounts/';
