import React, { useState, useEffect } from 'react';
import logo from '../../assets/logo.png';
import { Bell, Search, MoreVertical } from 'lucide-react';
import { useAuth } from '../../contexts/AuthContext';
import { DEFAULT_AVATAR_URL } from '../../api/auth';

function formatDateTime() {
  const now = new Date();
  return now.toLocaleString('en-IN', {
    weekday: 'long',
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZoneName: 'short',
  });
}

export default function Navbar() {
  const { user } = useAuth();
  const [dateTime, setDateTime] = useState(formatDateTime());

  useEffect(() => {
    const t = setInterval(() => setDateTime(formatDateTime()), 1000);
    return () => clearInterval(t);
  }, []);

  const avatarUrl = user?.avatar_url || DEFAULT_AVATAR_URL;
  const displayName = user?.username || user?.name || user?.email || 'User';
  const role = user?.role || 'MANAGER';
  const initials = displayName.split(/\s+/).map((n) => n[0]).join('').slice(0, 2).toUpperCase() || 'U';

  return (
    <nav className="flex items-center justify-between px-6 md:px-8 py-4 bg-[#1a1f26]/95 backdrop-blur-md border-b border-white/5 text-white font-sans">
      {/* Logo */}
      <div className="flex items-center gap-3 shrink-0">
        <img src={logo} alt="TaskLedger" className="h-10 w-auto object-contain" />
      </div>

      {/* Search */}
      <div className="hidden md:flex items-center flex-1 max-w-[420px] mx-6">
        <div className="relative w-full">
          <Search
            size={18}
            className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400 pointer-events-none"
          />
          <input
            type="text"
            placeholder="Search tasks..."
            className="w-full pl-10 pr-4 py-2 rounded-lg bg-white/5 border border-white/10 focus:outline-none focus:border-cyan-400 text-white placeholder-gray-500"
          />
        </div>
      </div>

      {/* Right: notifications, user, more, date */}
      <div className="flex items-center gap-3 shrink-0">
        <button
          type="button"
          className="relative p-2 rounded-lg text-gray-400 hover:text-cyan-400 hover:bg-cyan-500/10 transition-colors hover:shadow-[0_0_12px_rgba(34,211,238,0.4)]"
          aria-label="Notifications"
        >
          <Bell size={20} />
        </button>

        <div className="flex items-center gap-2">
          <img
            src={avatarUrl}
            alt=""
            className="h-10 w-10 rounded-full object-cover shrink-0 border border-white/10"
            onError={(e) => {
              e.target.onerror = null;
              e.target.style.display = 'none';
              const fallback = e.target.nextElementSibling;
              if (fallback) {
                fallback.classList.remove('hidden');
                fallback.classList.add('flex');
              }
            }}
          />
          <div
            className="hidden h-10 w-10 items-center justify-center rounded-full bg-cyan-500/30 text-cyan-300 text-sm font-semibold shrink-0"
            aria-hidden
          >
            {initials}
          </div>
          <div className="hidden sm:flex flex-col leading-tight">
            <span className="text-sm font-medium text-white">{displayName}</span>
            <span className="text-xs bg-cyan-500/20 text-cyan-400 px-2 py-[2px] rounded w-fit uppercase tracking-wide">
              {role}
            </span>
          </div>
        </div>

        <button
          type="button"
          className="p-2 rounded-lg hover:bg-white/5 text-gray-400 hover:text-white transition-colors"
          aria-label="More options"
        >
          <MoreVertical size={18} />
        </button>

        <span className="hidden lg:block text-xs text-gray-500 ml-2 max-w-[220px] truncate">
          {dateTime}
        </span>
      </div>
    </nav>
  );
}
