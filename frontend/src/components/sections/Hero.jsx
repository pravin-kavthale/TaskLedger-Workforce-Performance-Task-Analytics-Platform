import React from 'react';


function Hero() {
  return (
    <section className="relative bg-transparent py-20 px-8 md:px-16 lg:px-24 z-10">
      {/* --- BACKGROUND ATMOSPHERE (Light Effects) --- */}
      {/* Soft teal glow on the left */}
      <div className="absolute top-[-10%] left-[-5%] w-[600px] h-[600px] bg-[#4fd1c5]/10 blur-[140px] rounded-full -z-0"></div>
      {/* Deep blue glow on the right */}
      <div className="absolute top-[10%] right-[0%] w-[500px] h-[500px] bg-blue-500/5 blur-[120px] rounded-full -z-0"></div>

      {/* Grid Layout: Text side is now much wider (1.4fr) than the graphic side (0.6fr) */}
      <div className="relative z-10 max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-[1.4fr_0.6fr] gap-12 items-center w-full">
        
        {/* 1. Left Content Side (Increased Width) */}
        <div className="text-left">
          <h1 className="text-4xl md:text-5xl lg:text-6xl xl:text-7xl font-bold leading-[1.05] tracking-tight font-sans text-white">
            Organize Tasks. <br />
            <span className="text-[#4fd1c5] font-serif italic font-normal">Track Progress.</span> <br />
            Build Accountability.
          </h1>

          <p className="mt-8 text-gray-400 text-sm md:text-lg max-w-xl leading-relaxed opacity-90 font-sans">
            A streamlined project management engine designed for teams 
            valuing transparency, role-based security, and real-time activity tracking.
          </p>

          {/* 2. Enhanced Buttons (Increased Size and Aquatic Blue theme) */}
          <div className="mt-12 flex flex-wrap gap-6">
            {/* Primary Aquatic Blue Button */}
            <button className="bg-[#4fd1c5] hover:bg-[#38b2ac] text-[#1a1f26] px-12 py-4 rounded-full font-bold text-base transition-all shadow-2xl shadow-teal-500/30 active:scale-95">
              Get Started Now
            </button>
            
            {/* Secondary 'Explore' Button with the requested Aquatic Blue tint */}
            <button className="border-2 border-[#22d3ee]/30 hover:border-[#22d3ee] text-white px-12 py-4 rounded-full font-bold text-base transition-all bg-[#0ea5e9]/10 hover:bg-[#0ea5e9]/20 backdrop-blur-sm active:scale-95">
              Explore Features
            </button>
          </div>
        </div>

        {/* 3. Right Graphic Side (Scaled down to balance the wider text) */}
        <div className="relative hidden lg:block justify-self-end w-full max-w-[380px]">
          {/* Internal Glow for the box */}
          <div className="absolute -inset-4 bg-[#4fd1c5]/5 blur-[40px] rounded-full"></div>
          
          <div className="relative border border-white/5 rounded-2xl bg-white/[0.02] backdrop-blur-xl h-[280px] flex items-center justify-center border-dashed">
            <p className="text-gray-600 italic text-[10px] tracking-[0.2em] text-center px-10 uppercase">
              Interactive Dashboard <br /> Interface
            </p>
          </div>
        </div>

      </div>
    </section>
  );
}

export default Hero;