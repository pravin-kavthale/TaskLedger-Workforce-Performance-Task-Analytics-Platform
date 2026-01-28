import React from 'react';
import Hero from '../components/sections/Hero';
import Features from '../components/sections/FeatureCard';
import WhySection from '../components/sections/WhySection';

const Home = () => {
  return (
    <div className="bg-[#1a1f26] h-screen overflow-hidden flex flex-col">
      {/* flex-1 allows the main content to fill the remaining space perfectly */}
      <main className="flex-1 flex flex-col justify-between overflow-hidden">
        <Hero />
        <Features />
        <WhySection />
      </main>
    </div>
  );
};

export default Home;