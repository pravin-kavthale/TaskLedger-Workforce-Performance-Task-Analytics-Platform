import React, { useEffect } from 'react';
import AboutHero from '../components/about/AboutHero';
import AboutMission from '../components/about/AboutMissions';

const About = () => {
  useEffect(() => {
    window.scrollTo(0, 0);
  }, []);

  return (
    /* h-screen + overflow-hidden makes it a single non-scrollable page */
    <main className="h-screen bg-[#1a1f26] flex flex-col overflow-hidden selection:bg-[#4fd1c5]/30">
      
      {/* Content Container: flex-1 allows these to fill the space perfectly */}
      <div className="flex-1 flex flex-col justify-center px-8 md:px-16 lg:px-24">
        <AboutHero />
        
        {/* Subtle thin separator to match your style */}
        <div className="h-[1px] w-full bg-gradient-to-r from-transparent via-white/10 to-transparent my-4"></div>
        
        <AboutMission />
      </div>

      {/* Tighter Bottom CTA to save vertical space */}
      <footer className="pb-10 px-8 text-center">
        <div className="max-w-2xl mx-auto p-6 rounded-2xl bg-white/[0.02] border border-white/5 backdrop-blur-sm">
          <h2 className="text-lg font-bold text-white mb-3">
            Ready to build a more accountable team?
          </h2>
          <button className="bg-[#4fd1c5] text-[#1a1f26] px-8 py-2.5 rounded-full font-black uppercase text-[10px] transition-transform hover:scale-105">
            Initialize TaskLedger
          </button>
        </div>
      </footer>
    </main>
  );
};

export default About;