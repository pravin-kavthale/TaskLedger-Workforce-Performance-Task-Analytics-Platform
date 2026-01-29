import React from 'react';

const NeonInput = ({ 
  icon: Icon, 
  type = "text", 
  placeholder, 
  value, 
  onChange, 
  label 
}) => {
  return (
    <div className="space-y-2 w-full group">
      
      {label && (
        <label className="text-[10px] font-black text-gray-500 uppercase tracking-[0.2em] ml-1 transition-colors group-focus-within:text-[#22d3ee]">
          {label}
        </label>
      )}
      
      <div className="relative">
        
        <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none text-gray-600 group-focus-within:text-[#22d3ee] transition-colors duration-300">
          {Icon && <Icon size={18} strokeWidth={1.5} />}
        </div>

        
        <input 
          type={type}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          className="w-full bg-[#0a0f12]/60 border border-white/5 text-white pl-12 pr-4 py-4 rounded-2xl text-sm outline-none transition-all duration-300 
                     focus:border-[#22d3ee]/40 focus:bg-[#0a0f12] focus:ring-4 focus:ring-[#22d3ee]/5
                     placeholder:text-gray-700 group-hover:border-white/10"
        />

        <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-0 h-[1px] bg-[#22d3ee] transition-all duration-500 group-focus-within:w-1/2 opacity-50 shadow-[0_0_8px_#22d3ee]"></div>
      </div>
    </div>
  );
};

export default NeonInput;