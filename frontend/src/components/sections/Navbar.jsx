import React from 'react';
import logoJpg from '../../assets/logo.png'; 

function Navbar() {
  return (
    <nav className="sticky top-0 z-50 flex items-center justify-between px-8 md:px-16 py-4 bg-[#1a1f26]/95 backdrop-blur-md border-b border-white/5 text-white font-sans">
      
      {/* 1. Logo Section */}
      <div className="flex items-center gap-4 cursor-pointer">
        <img 
          src={logoJpg} 
          alt="TaskLedger Logo" 
          /* Increased size from w-8/h-8 to w-12/h-12 or w-32 for horizontal logos */
          className="h-11 w-auto object-contain transition-transform hover:scale-105" 
        />
      </div>

      {/* 2. Navigation Links */}
      <div className="flex items-center gap-10 text-sm font-medium">
        <a href="#home" className="text-[#4fd1c5] border-b-2 border-[#4fd1c5] pb-1">Home</a>
        <a href="#features" className="text-gray-400 hover:text-white transition-all">Features</a>
        <a href="#about" className="text-gray-400 hover:text-white transition-all">About</a>
      </div>

      {/* 3. Action Buttons */}
      <div className="flex items-center gap-5">
        <button className="bg-[#f39452] hover:bg-[#e08341] text-white px-8 py-2.5 rounded-full text-xs font-black uppercase tracking-widest transition-all shadow-lg active:scale-95">
          Login
        </button>
        <button className="border border-[#4fd1c5]/40 hover:border-[#4fd1c5] text-white px-6 py-2.5 rounded-full text-xs font-black uppercase tracking-widest transition-all bg-white/5 active:scale-95">
          Get Started
        </button>
      </div>
      
    </nav>
  );
}

export default Navbar;