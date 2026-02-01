import React, { useState, useEffect } from 'react';
import logoJpg from '../../assets/logo.png';
import { Link, useNavigate } from 'react-router-dom';
import { getAccessToken, getMe, clearTokens, DEFAULT_AVATAR_URL } from '../../api/auth';

function Navbar() {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  const isLoggedIn = !!getAccessToken();

  useEffect(() => {
    if (!isLoggedIn) {
      setUser(null);
      setLoading(false);
      return;
    }
    let cancelled = false;
    getMe()
      .then((data) => {
        if (!cancelled) setUser(data);
      })
      .catch(() => {
        if (!cancelled) setUser(null);
      })
      .finally(() => {
        if (!cancelled) setLoading(false);
      });
    return () => { cancelled = true; };
  }, [isLoggedIn]);

  const handleLogout = () => {
    clearTokens();
    setUser(null);
    navigate('/login');
  };

  const avatarUrl = user?.avatar_url || DEFAULT_AVATAR_URL;

  return (
    <nav className="sticky top-0 z-50 flex items-center justify-between px-8 md:px-16 py-4 bg-[#1a1f26]/95 backdrop-blur-md border-b border-white/5 text-white font-sans">
      
      <div 
        className="flex items-center gap-4 cursor-pointer" 
        onClick={() => navigate('/')}
      >
        <img 
          src={logoJpg} 
          alt="TaskLedger Logo" 
          className="h-11 w-auto object-contain transition-transform hover:scale-105" 
        />
      </div>

      <div className="flex gap-6">
        <Link to="/" className="hover:text-[#4fd1c5] transition-colors">Home</Link>
        <Link to="/about" className="hover:text-[#4fd1c5] transition-colors">About</Link>
        <Link to="/login" className="hover:text-[#4fd1c5] transition-colors">Features</Link>
      </div>

      <div className="flex items-center gap-5">
        {loading && isLoggedIn ? (
          <div className="w-10 h-10 rounded-full bg-white/10 animate-pulse" />
        ) : user ? (
          <div className="flex items-center gap-3">
            <img
              src={avatarUrl}
              alt=""
              className="w-10 h-10 rounded-full object-cover border-2 border-white/20 flex-shrink-0"
              onError={(e) => {
                e.target.onerror = null;
                e.target.src = DEFAULT_AVATAR_URL;
              }}
            />
            <button
              type="button"
              onClick={handleLogout}
              className="text-xs font-bold uppercase tracking-wider text-gray-400 hover:text-white transition-colors"
            >
              Log out
            </button>
          </div>
        ) : (
          <>
            <button 
              onClick={() => navigate('/login')}
              className="bg-[#f39452] hover:bg-[#e08341] text-white px-8 py-2.5 rounded-full text-xs font-black uppercase tracking-widest transition-all shadow-lg active:scale-95"
            >
              Login
            </button>
            <button 
              onClick={() => navigate('/login')}
              className="border border-[#4fd1c5]/40 hover:border-[#4fd1c5] text-white px-6 py-2.5 rounded-full text-xs font-black uppercase tracking-widest transition-all bg-white/5 active:scale-95"
            >
              Get Started
            </button>
          </>
        )}
      </div>
      
    </nav>
  );
}

export default Navbar;