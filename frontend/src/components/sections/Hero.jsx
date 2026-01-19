import React from 'react';

function Hero() {
  return (
    <section className="relative bg-transparent pt-6 pb-2 px-8 md:px-16 lg:px-24 z-10">
      <div className="absolute top-0 left-[-5%] w-[400px] h-[400px] bg-[#4fd1c5]/10 blur-[100px] rounded-full pointer-events-none"></div>
      
      <div className="relative z-10 max-w-7xl mx-auto grid grid-cols-1 lg:grid-cols-[1.2fr_0.8fr] gap-8 items-center">
        <div>
          <h1 className="text-3xl md:text-5xl font-black leading-tight tracking-tight text-white">
            Organize Tasks. <br />
            <span className="text-[#4fd1c5] font-serif italic font-normal">Track Progress.</span> <br />
            Build Accountability.
          </h1>
          <p className="mt-4 text-gray-400 text-sm max-w-lg leading-relaxed opacity-90">
            A streamlined project management engine designed for teams valuing transparency and real-time tracking.
          </p>
          <div className="mt-6 flex gap-4">
            <button className="bg-[#4fd1c5] text-[#1a1f26] px-8 py-2.5 rounded-full font-black text-xs uppercase transition-all shadow-xl shadow-teal-500/20 active:scale-95">
              Get Started Now
            </button>
            <button className="border border-[#22d3ee]/30 text-white px-8 py-2.5 rounded-full font-bold text-xs uppercase bg-white/5 backdrop-blur-sm">
              Explore Features
            </button>
          </div>
        </div>

        <div className="hidden lg:block w-full max-w-[450px] justify-self-end">
          <div className="relative transform hover:scale-105 transition-transform duration-500">
            <img 
              src="/Home_Dashboard.png" 
              alt="Dashboard Interface" 
              className="w-full h-auto drop-shadow-[0_20px_50px_rgba(79,209,197,0.2)] animate-pulse-slow"
              style={{
                animation: 'float 6s ease-in-out infinite'
              }}
            />
            {/* Inline style for the float effect since we only change this div */}
            <style>{`
              @keyframes float {
                0% { transform: translateY(0px) rotateX(0deg); }
                50% { transform: translateY(-20px) rotateX(2deg); }
                100% { transform: translateY(0px) rotateX(0deg); }
              }
            `}</style>
          </div>
        </div>
      </div>
    </section>
  );
}

export default Hero;

