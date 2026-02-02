# Authentication System Implementation

## Overview
This document describes the refactored authentication system that eliminates repeated 401 errors and implements a clean, predictable authentication lifecycle.

## Architecture

### Single Source of Truth: AuthContext
- **Location**: `src/contexts/AuthContext.jsx`
- **Purpose**: Centralized authentication state management
- **State**: `user`, `isAuthenticated`, `loading`
- **Methods**: `login()`, `logout()`, `refreshUser()`

### Auth Service Layer
- **Location**: `src/api/auth.js`
- **Key Functions**:
  - `login()` - Authenticate user
  - `getMe()` - Fetch current user (with automatic token refresh on 401)
  - `refreshAccessToken()` - Refresh expired access token
  - `setTokens()`, `getAccessToken()`, `clearTokens()` - Token management

## Key Features

### 1. Automatic Token Refresh
- `getMe()` automatically attempts token refresh on 401 errors
- Refresh happens exactly once per token expiration
- Prevents infinite refresh loops using `refreshAttempted` flag
- Concurrent requests share the same refresh promise to prevent duplicate refresh calls

### 2. Race Condition Prevention
- AuthProvider initialization tracked with `initializedRef` and `initializingRef`
- Prevents multiple simultaneous initialization attempts
- Components wait for initialization to complete before accessing auth state

### 3. Error Handling
- All errors are properly thrown (not silently swallowed)
- Failed refresh attempts clear tokens and reset auth state
- Components can handle errors appropriately

### 4. No Direct API Calls
- Components use `useAuth()` hook instead of calling `getMe()` directly
- Prevents duplicate `/auth/me/` calls
- Ensures consistent auth state across all components

## Usage Examples

### App.jsx Setup
```jsx
import { AuthProvider } from './contexts/AuthContext';

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}
```

### Using Auth in Components
```jsx
import { useAuth } from '../contexts/AuthContext';

function MyComponent() {
  const { user, isAuthenticated, loading, login, logout } = useAuth();

  if (loading) return <div>Loading...</div>;
  
  if (!isAuthenticated) return <div>Please login</div>;

  return (
    <div>
      <p>Welcome, {user?.username}</p>
      <button onClick={logout}>Logout</button>
    </div>
  );
}
```

### Login Flow
```jsx
import { useAuth } from '../contexts/AuthContext';

function LoginForm() {
  const { login, loading } = useAuth();
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await login(email, password);
      navigate('/app');
    } catch (err) {
      setError(err.message);
    }
  };
}
```

## Authentication Flow

1. **App Initialization**
   - AuthProvider mounts and checks for stored access token
   - If token exists, calls `getMe()` to verify and fetch user
   - If token invalid/expired, `getMe()` attempts refresh automatically
   - If refresh fails, tokens are cleared and user is logged out

2. **Login**
   - User submits credentials via `login()` method
   - Tokens are stored and user data is fetched
   - Auth state is updated atomically

3. **Protected Requests**
   - Components access user data via `useAuth()` hook
   - No direct API calls to `/auth/me/`
   - Auth state is shared across all components

4. **Token Expiration**
   - When access token expires, next `getMe()` call receives 401
   - Automatic refresh is attempted exactly once
   - If refresh succeeds, request is retried with new token
   - If refresh fails, tokens are cleared and user is logged out

5. **Logout**
   - `logout()` clears tokens and resets auth state
   - Components automatically reflect logged-out state

## Security Features

- Tokens stored in localStorage (as per current implementation)
- Refresh tokens used only for obtaining new access tokens
- Failed authentication attempts properly clear all tokens
- No sensitive data exposed in error messages
- Proper error codes for different failure scenarios

## Backend Endpoints Used

- `POST /api/auth/login/` - User authentication
- `GET /api/auth/me/` - Get current user (requires access token)
- `POST /api/auth/refresh/` - Refresh access token (requires refresh token)

## Testing Checklist

- ✅ No repeated `/auth/me/` calls on page load
- ✅ Token refresh works automatically on 401
- ✅ No infinite refresh loops
- ✅ Proper logout clears all state
- ✅ Race conditions prevented during initialization
- ✅ Multiple components can use auth state simultaneously
- ✅ Page refresh correctly initializes auth state
