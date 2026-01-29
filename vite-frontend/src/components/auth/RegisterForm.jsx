import React, { useState } from 'react';
import { User, Mail, Lock, Building2, UserPlus, ArrowRight } from 'lucide-react';
import NeonInput from './NeonInput';

export default function RegisterForm() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    department: ''
  });

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Provisioning Node with Data:", formData);
    // Logic to insert into User and Profile tables based on ER diagram
  };

  return (
    <div className="relative w-full max-w-xl px-6 py-12">
      {/* THE GLASS CARD */}
      <div className="bg-[#161b22]/40 border border-white/10 rounded-[2.5rem] p-8 md:p-12 backdrop-blur-2xl shadow-2xl relative overflow-hidden group">
        
        {/* ANIMATED TRACE LINE (From your index.css) */}
        <div className="absolute top-0 left-0 w-full h-[1.5px] overflow-hidden">
          <div className="w-1/3 h-full bg-gradient-to-r from-transparent via-[#22d3ee] to-transparent animate-trace-right relative"></div>
        </div>

        {/* HEADER */}
        <div className="mb-10 text-center md:text-left">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#22d3ee]/10 border border-[#22d3ee]/20 mb-4">
            <UserPlus size={14} className="text-[#22d3ee]" />
            <span className="text-[10px] font-bold text-[#22d3ee] uppercase tracking-widest">Identity Protocol</span>
          </div>
          <h1 className="text-4xl font-black text-white tracking-tighter">
            Initialize <span className="text-[#4fd1c5]">New Node</span>
          </h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* TWO COLUMN GRID FOR LARGE SCREENS */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <NeonInput 
              label="Node Identity"
              icon={User}
              placeholder="Username"
              value={formData.username}
              onChange={(e) => setFormData({...formData, username: e.target.value})}
            />
            <NeonInput 
              label="Secure Channel"
              icon={Mail}
              type="email"
              placeholder="Email Address"
              value={formData.email}
              onChange={(e) => setFormData({...formData, email: e.target.value})}
            />
          </div>

          <NeonInput 
            label="Department Assignment"
            icon={Building2}
            placeholder="Select Division (Department ID)"
            value={formData.department}
            onChange={(e) => setFormData({...formData, department: e.target.value})}
          />

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <NeonInput 
              label="Access Key"
              icon={Lock}
              type="password"
              placeholder="Password"
              value={formData.password}
              onChange={(e) => setFormData({...formData, password: e.target.value})}
            />
            <NeonInput 
              label="Verify Key"
              icon={Lock}
              type="password"
              placeholder="Confirm Password"
              value={formData.confirmPassword}
              onChange={(e) => setFormData({...formData, confirmPassword: e.target.value})}
            />
          </div>

          {/* SUBMIT ACTION */}
          <div className="pt-4">
            <button 
              type="submit"
              className="w-full bg-[#4fd1c5] text-[#0a0f12] py-4 rounded-2xl font-black uppercase text-[11px] tracking-[0.3em] flex items-center justify-center gap-3 transition-all hover:shadow-[0_0_30px_rgba(79,209,197,0.4)] hover:scale-[1.01] active:scale-95"
            >
              Provision New Node <ArrowRight size={18} />
            </button>
          </div>
        </form>

        {/* FOOTER */}
        <div className="mt-8 pt-6 border-t border-white/5 text-center">
          <p className="text-[11px] text-gray-500 font-medium">
            Node already registered? {' '}
            <a href="/login" className="text-white font-bold hover:text-[#22d3ee] transition-colors uppercase tracking-tighter">
              Authorize Existing Identity
            </a>
          </p>
        </div>
      </div>
    </div>
  );
}