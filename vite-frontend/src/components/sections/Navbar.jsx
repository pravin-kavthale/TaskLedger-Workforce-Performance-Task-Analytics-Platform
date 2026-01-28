import React from 'react';
import logoJpg from '../../assets/logo.png'; 
import { Link, useNavigate } from 'react-router-dom'; 

function Navbar() {
  const navigate = useNavigate();

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
      </div>
      
    </nav>
  );
}

export default Navbar;