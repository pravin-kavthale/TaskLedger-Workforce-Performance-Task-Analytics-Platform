import React, { useState } from 'react';
import { Mail, Lock, ArrowRight, Shield } from 'lucide-react';
import NeonInput from './NeonInput';
import { useNavigate } from 'react-router-dom';
import { login, setTokens } from '../../api/auth';

export default function LoginForm() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      const { access, refresh } = await login(email, password);
      setTokens(access, refresh);
      navigate('/');
    } catch (err) {
      setError(err.message || 'Invalid credentials');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="relative w-full max-w-[420px] px-6">
      
      {/* GLASS CARD CONTAINER */}
      <div className="bg-[#161b22]/40 border border-white/10 rounded-[2.5rem] p-10 backdrop-blur-2xl shadow-2xl relative overflow-hidden group">
        
        {/* ANIMATED TRACE LINE (Using your index.css keyframes) */}
        <div className="absolute top-0 left-0 w-full h-[1.5px] overflow-hidden">
          <div className="w-1/3 h-full bg-gradient-to-r from-transparent via-[#22d3ee] to-transparent animate-trace-right relative"></div>
        </div>

        {/* LOGO / HEADER SECTION */}
        <div className="flex flex-col items-center mb-8">
          <div className="w-14 h-14 bg-[#22d3ee]/10 border border-[#22d3ee]/30 rounded-2xl flex items-center justify-center mb-4 shadow-[0_0_20px_rgba(34,211,238,0.1)]">
            <Shield className="text-[#22d3ee]" size={28} />
          </div>
          <h1 className="text-3xl font-black text-white tracking-tighter">
            Task<span className="text-[#4fd1c5]">Ledger</span>
          </h1>
          <p className="text-[10px] text-gray-500 font-bold uppercase tracking-[0.2em] mt-1">
            Authentication Required
          </p>
        </div>

        {/* FORM SECTION */}
        <form onSubmit={handleLogin} className="space-y-5">
          {error && (
            <div className="text-red-400 text-sm bg-red-500/10 border border-red-500/30 rounded-xl px-4 py-2">
              {error}
            </div>
          )}

          <NeonInput 
            label="Identity"
            icon={Mail}
            type="email"
            placeholder="user@taskledger.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <div className="relative">
            <NeonInput 
              label="Access Key"
              icon={Lock}
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
            <div className="absolute top-0 right-1">
              <button type="button" className="text-[9px] font-bold text-[#22d3ee]/50 hover:text-[#22d3ee] uppercase tracking-tighter transition-colors">
                Lost Key?
              </button>
            </div>
          </div>

          <button 
            type="submit"
            disabled={loading}
            className="w-full bg-[#4fd1c5] text-[#0a0f12] py-4 rounded-2xl font-black uppercase text-[11px] tracking-[0.2em] flex items-center justify-center gap-2 transition-all hover:shadow-[0_0_30px_rgba(79,209,197,0.3)] hover:scale-[1.01] active:scale-95 mt-6 disabled:opacity-60 disabled:cursor-not-allowed disabled:hover:scale-100"
          >
            {loading ? 'Authorizing...' : 'Authorize'} <ArrowRight size={16} />
          </button>
        </form>

        <div className="mt-8 text-center">
          <p className="text-[11px] text-gray-600 font-medium">
            No identity found? {' '}
            <button 
            onClick={() => navigate('/signup')}
            className="text-white font-bold hover:text-[#22d3ee] transition-colors uppercase tracking-tighter">
              Create New Node
            </button>
          </p>
        </div>
      </div>
    </div>
  );
}