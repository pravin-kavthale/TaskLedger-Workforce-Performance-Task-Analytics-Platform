import React from 'react';
// Corrected paths to match your 'sections' folder location
import Navbar from '../components/sections/Navbar';
import Hero from '../components/sections/Hero';
import FeatureCard from '../components/sections/FeatureCard';
import WhySection from '../components/sections/WhySection';

const Home = () => {
  return (
    <div className="bg-[#1a1f26] min-h-screen">
      <Navbar />
      <Hero />
      <FeatureCard />
      <WhySection />
    </div>
  );
};

export default Home;