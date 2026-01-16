import React from 'react';

function Navbar() {
  return (
    /* Change 1: Updated background color to the bluish-dark hex #1a1f26 */
    /* Change 2: Added sticky positioning and backdrop-blur for a premium feel */
    <nav className="sticky top-0 z-50 flex items-center justify-between px-8 md:px-16 py-5 bg-[#1a1f26]/90 backdrop-blur-md border-b border-white/5 text-white font-sans">
      
      {/* 1. Logo Section */}
      <div className="flex items-center gap-2 cursor-pointer">
        <div className="flex -space-x-2">
          {/* Matching the Teal color from your image */}
          <div className="w-6 h-6 border-2 border-[#4fd1c5] rounded-full"></div>
          <div className="w-6 h-6 border-2 border-[#4fd1c5] rounded-full"></div>
        </div>
        <span className="text-xl font-bold tracking-tight ml-2">TaskLedger</span>
      </div>

      {/* 2. Navigation Links */}
      <div className="flex items-center gap-10 text-sm font-medium">
        {/* 'Home' is active by default in your screenshot with teal text and underline */}
        <a 
          href="#home" 
          className="text-[#4fd1c5] border-b-2 border-[#4fd1c5] pb-1 transition-all"
        >
          Home
        </a>
        <a 
          href="#features" 
          className="text-gray-400 hover:text-white transition-all pb-1 border-b-2 border-transparent"
        >
          Features
        </a>
        <a 
          href="#about" 
          className="text-gray-400 hover:text-white transition-all pb-1 border-b-2 border-transparent"
        >
          About
        </a>
      </div>

      {/* 3. Action Buttons */}
      <div className="flex items-center gap-5">
        <button className="bg-[#f39452] hover:bg-[#e08341] text-white px-8 py-2 rounded-full text-sm font-bold transition-all shadow-lg shadow-orange-500/10">
          Login
        </button>
        <button className="border border-[#4fd1c5]/40 hover:border-[#4fd1c5] text-white px-6 py-2 rounded-full text-sm font-bold transition-all bg-white/5">
          Get Started
        </button>
      </div>
      
    </nav>
  );
}

export default Navbar;