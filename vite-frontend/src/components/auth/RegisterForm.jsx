import React, { useState } from 'react';
import { User, Mail, Lock, Building2, UserPlus, ArrowRight, ShieldCheck, ChevronDown } from 'lucide-react';
import NeonInput from './NeonInput';

export default function RegisterForm() {
  const [formData, setFormData] = useState({
    username: '',
    email: '',
    password: '',
    confirmPassword: '',
    department: '',
    role: 'EMPLOYEE' // Default value
  });

  // Simulation: Current logged-in user state
  const currentUserRole = "ADMIN"; 

  const handleSubmit = (e) => {
    e.preventDefault();
    console.log("Provisioning Node with Data:", formData);
  };

  return (
    <div className="relative w-full max-w-xl px-6 py-12">
      <div className="bg-[#161b22]/40 border border-white/10 rounded-[2.5rem] p-8 md:p-12 backdrop-blur-2xl shadow-2xl relative overflow-hidden group">
        
        {/* TOP TRACE ANIMATION */}
        <div className="absolute top-0 left-0 w-full h-[1.5px] overflow-hidden">
          <div className="w-1/3 h-full bg-gradient-to-r from-transparent via-[#22d3ee] to-transparent animate-trace-right relative"></div>
        </div>

        <div className="mb-10 text-center md:text-left">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-[#22d3ee]/10 border border-[#22d3ee]/20 mb-4">
            <ShieldCheck size={14} className="text-[#22d3ee]" />
            <span className="text-[10px] font-bold text-[#22d3ee] uppercase tracking-widest">Admin Provisioning</span>
          </div>
          <h1 className="text-4xl font-black text-white tracking-tighter">
            Initialize <span className="text-[#4fd1c5]">New Node</span>
          </h1>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          {/* USERNAME & EMAIL */}
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

          {/* DEPARTMENT */}
          <NeonInput 
            label="Department Assignment"
            icon={Building2}
            placeholder="Select Division (Department ID)"
            value={formData.department}
            onChange={(e) => setFormData({...formData, department: e.target.value})}
          />

          {/* ROLE ASSIGNMENT SECTION */}
          <div className="space-y-2 group">
            <label className="text-[10px] font-black text-gray-500 uppercase tracking-[0.2em] ml-1 transition-colors group-focus-within:text-[#4fd1c5]">
              Role Assignment
            </label>
            
            <div className="relative">
              {/* ICON: Now turns Skyblue on focus */}
              <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-600 group-focus-within:text-[#4fd1c5] transition-colors duration-300">
                <ShieldCheck size={18} strokeWidth={1.5} />
              </div>
              
              {/* THE SELECT: High-Tech Skyblue styling */}
              <select 
                value={formData.role}
                disabled={currentUserRole === "MANAGER"}
                onChange={(e) => setFormData({...formData, role: e.target.value})}
                className="w-full bg-[#0a0f12]/60 border border-white/5 text-white pl-12 pr-10 py-4 rounded-2xl text-sm outline-none transition-all duration-300 cursor-pointer
                          appearance-none 
                          focus:border-[#4fd1c5]/50 focus:bg-[#0a0f12] focus:ring-4 focus:ring-[#4fd1c5]/10 
                          group-hover:border-white/10 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {/* Options styled for dark-mode compatibility */}
                <option value="ADMIN" className="bg-[#161b22] text-white">ADMIN</option>
                <option value="MANAGER" className="bg-[#161b22] text-white">MANAGER</option>
                <option value="EMPLOYEE" className="bg-[#161b22] text-white">EMPLOYEE</option>
              </select>

              {/* RIGHT ACCESSORY: Chevron or Lock */}
              <div className="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none text-gray-600 group-focus-within:text-[#4fd1c5] transition-colors duration-300">
                {currentUserRole === "MANAGER" ? (
                  <Lock size={16} className="opacity-50" />
                ) : (
                  <ChevronDown size={18} strokeWidth={2} />
                )}
              </div>

              {/* SKYBLUE BOTTOM GLOW LINE: Matches your heading's primary accent */}
              <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-[1px] bg-[#4fd1c5] transition-all duration-500 group-focus-within:w-1/2 opacity-70 shadow-[0_0_12px_#4fd1c5]"></div>
            </div>

            <p className="text-[9px] text-gray-600 font-bold uppercase tracking-widest ml-1">
              {currentUserRole === "ADMIN" ? "Available roles depend on your permissions" : "⚠️ Role locked to Managerial hierarchy"}
            </p>
          </div>
          
          {/* PASSWORDS */}
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

          <button 
            type="submit"
            className="w-full bg-[#4fd1c5] text-[#0a0f12] py-4 rounded-2xl font-black uppercase text-[11px] tracking-[0.3em] flex items-center justify-center gap-3 transition-all hover:shadow-[0_0_30px_rgba(79,209,197,0.4)] hover:scale-[1.01] active:scale-95 pt-4"
          >
            Provision New Node <ArrowRight size={18} />
          </button>
        </form>
      </div>
    </div>
  );
}