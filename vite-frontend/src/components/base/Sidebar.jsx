import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import {
  LayoutDashboard,
  ListTodo,
  Users,
  FileBarChart,
  Activity,
  User,
  LogOut,
  Menu,
} from 'lucide-react';

const navItems = [
  { to: '/app', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/app/my-tasks', label: 'My Tasks', icon: ListTodo },
  { to: '/app/team-tasks', label: 'Team Tasks', icon: Users },
  { to: '/app/reports', label: 'Reports', icon: FileBarChart },
  { to: '/app/activity', label: 'Activity Log', icon: Activity },
  { to: '/app/profile', label: 'Profile', icon: User },
];

export default function Sidebar() {
  const location = useLocation();
  const navigate = useNavigate();
  const { logout } = useAuth();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <aside className="relative w-[240px] h-full flex-shrink-0 p-[3px] rounded-2xl sidebar-border-animate">
      <div className="h-full w-full min-h-0 rounded-2xl bg-[#1a1f26] flex flex-col overflow-hidden">
        {/* Hamburger */}
        <button
          type="button"
          className="flex items-center justify-center w-full h-12 text-gray-400 hover:text-white hover:bg-white/5 transition-colors"
          aria-label="Toggle menu"
        >
          <Menu size={22} />
        </button>

        {/* Nav items */}
        <nav className="flex-1 px-2 py-2 space-y-0.5">
          {navItems.map(({ to, label, icon: Icon }) => {
            const isActive = location.pathname === to || (to !== '/app' && location.pathname.startsWith(to));
            return (
              <Link
                key={to}
                to={to}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-cyan-500/10 text-white border-l-2 border-cyan-400'
                    : 'text-gray-400 hover:text-white hover:bg-white/5'
                }`}
              >
                <Icon size={18} className={isActive ? 'text-cyan-400' : ''} />
                {label}
              </Link>
            );
          })}
        </nav>

        {/* Logout */}
        <div className="p-2 border-t border-white/5">
          <button
            type="button"
            onClick={handleLogout}
            className="flex items-center justify-center gap-2 w-full py-2.5 rounded-lg bg-red-500/20 text-red-400 hover:bg-red-500/30 text-sm font-medium transition-colors"
          >
            <LogOut size={18} />
            Logout
          </button>
        </div>
      </div>
    </aside>
  );
}
