import React, { createContext, useContext, useState, useEffect, useCallback, useRef } from 'react';
import { login as apiLogin, setTokens, clearTokens, getMe, getAccessToken } from '../api/auth';

const AuthContext = createContext(null);

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
}

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  
  // Track initialization to prevent race conditions
  const initializedRef = useRef(false);
  const initializingRef = useRef(false);

  // Initialize auth state on mount
  useEffect(() => {
    if (initializedRef.current || initializingRef.current) {
      return;
    }

    initializingRef.current = true;
    initializeAuth();
  }, []);

  const initializeAuth = async () => {
    try {
      const token = getAccessToken();
      if (!token) {
        // No token - user is not authenticated
        setUser(null);
        setIsAuthenticated(false);
        setLoading(false);
        initializedRef.current = true;
        initializingRef.current = false;
        return;
      }

      // Token exists - verify it by fetching user
      try {
        const userData = await getMe();
        setUser(userData);
        setIsAuthenticated(true);
      } catch (error) {
        // Token invalid or expired - clear state
        console.error('Auth initialization failed:', error);
        setUser(null);
        setIsAuthenticated(false);
        clearTokens();
      }
    } catch (error) {
      console.error('Auth initialization error:', error);
      setUser(null);
      setIsAuthenticated(false);
      clearTokens();
    } finally {
      setLoading(false);
      initializedRef.current = true;
      initializingRef.current = false;
    }
  };

  const login = useCallback(async (email, password) => {
    try {
      setLoading(true);
      // Call login API
      const { access, refresh } = await apiLogin(email, password);
      
      // Store tokens
      setTokens(access, refresh);
      
      // Fetch user data
      const userData = await getMe();
      
      // Update state
      setUser(userData);
      setIsAuthenticated(true);
      
      return { success: true };
    } catch (error) {
      // Clear any partial state
      clearTokens();
      setUser(null);
      setIsAuthenticated(false);
      throw error;
    } finally {
      setLoading(false);
    }
  }, []);

  const logout = useCallback(() => {
    clearTokens();
    setUser(null);
    setIsAuthenticated(false);
    // Navigation will be handled by components using useNavigate
  }, []);

  const refreshUser = useCallback(async () => {
    // Only refresh if authenticated
    if (!isAuthenticated || !getAccessToken()) {
      return;
    }

    try {
      const userData = await getMe();
      setUser(userData);
    } catch (error) {
      // If refresh fails, logout
      console.error('Failed to refresh user:', error);
      logout();
    }
  }, [isAuthenticated, logout]);

  const value = {
    user,
    isAuthenticated,
    loading,
    login,
    logout,
    refreshUser,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
