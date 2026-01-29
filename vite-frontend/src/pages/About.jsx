import React from 'react';
import AboutHero from '../components/about/AboutHero';
import AboutMissions from '../components/about/AboutMissions';

const About = () => {
  return (
    <main className="relative min-h-screen w-full bg-[#0a0f12] text-white px-8 md:px-16 lg:px-24 overflow-hidden selection:bg-[#4fd1c5]/30">
      <div className="absolute top-0 left-[-10%] w-[700px] h-[700px] bg-[#4fd1c5]/10 blur-[140px] rounded-full pointer-events-none" />
      <div className="absolute top-[45%] right-[-10%] w-[500px] h-[500px] bg-[#22d3ee]/5 blur-[160px] rounded-full pointer-events-none" />

      <div className="relative z-10 flex flex-col gap-28 py-28">
        <AboutHero />
        <AboutMissions />
      </div>
    </main>
  );
};

export default About;
