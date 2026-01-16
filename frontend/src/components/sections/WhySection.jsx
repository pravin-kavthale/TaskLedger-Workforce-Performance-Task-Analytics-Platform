import React from 'react';
import { Plus, UserCheck, BarChart3, MoveRight } from 'lucide-react';

const Step = ({ icon: Icon, label }) => (
  <div className="flex flex-col items-center group">
    <div className="w-14 h-14 rounded-full border-2 border-[#22d3ee]/30 flex items-center justify-center bg-[#1a1f26] group-hover:border-[#22d3ee] group-hover:shadow-[0_0_20px_rgba(34,211,238,0.5)] transition-all duration-300">
      <Icon className="text-[#22d3ee] w-6 h-6" />
    </div>
    <p className="mt-4 text-gray-400 text-[10px] font-bold uppercase tracking-[0.2em] text-center">
      {label}
    </p>
  </div>
);

function WhySection() {
  return (
    <section className="bg-[#1a1f26] py-24 px-8 md:px-16 lg:px-24 border-t border-white/5">
      <div className="max-w-7xl mx-auto">
        
       
        {/* Section Header - Forced Styling */}
        <div className="mb-20 flex flex-col items-center lg:items-start">
        <h2 
            style={{ 
            fontFamily: 'sans-serif', 
            fontWeight: '900', 
            letterSpacing: '0.3em',
            fontSize: '2rem' 
            }}
            className="text-white uppercase leading-none"
        >
            Why TaskLedger?
        </h2>
        <div className="w-24 h-[6px] bg-[#22d3ee] mt-4 rounded-full shadow-[0_0_20px_rgba(34,211,238,0.5)]"></div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-16 items-center">
          
          {/* LEFT: The Flow Diagram */}
          <div className="flex items-center justify-start gap-4 md:gap-10">
            <Step icon={Plus} label="Transparency" />
            <MoveRight className="text-[#22d3ee]/20 w-6 h-6" />
            
            <Step icon={UserCheck} label="Accountability" />
            <MoveRight className="text-[#22d3ee]/20 w-6 h-6" />
            
            <Step icon={BarChart3} label="Faster Workforce" />
          </div>

          {/* RIGHT: CTA and Links Block */}
          <div className="flex flex-col md:flex-row lg:flex-row items-center gap-12">
            
            {/* Login CTA with requested Gradient */}
            <div className="flex flex-col items-center gap-6">
              <h3 className="text-white text-lg font-bold text-center lg:text-left max-w-[250px]">
                Start managing work smarter with TaskLedger
              </h3>
              <button className="relative overflow-hidden px-14 py-3 rounded-full font-black text-sm uppercase tracking-widest transition-all active:scale-95 shadow-[0_0_30px_rgba(34,211,238,0.2)] text-[#1a1f26] bg-gradient-to-br from-[#22d3ee] via-[#22d3ee] to-[#000000]/5">
                Login
              </button>
            </div>

            {/* THE MISSING LINKS BLOCK: 5-Column Small Text Grid */}
            <div className="grid grid-cols-5 gap-6 border border-white/10 bg-white/[0.03] backdrop-blur-md rounded-2xl pl-8 pr-8 py-6 shadow-2xl">
            {[
                { label: 'Product', links: ['Best'] },
                { label: 'Home', links: ['High-performance'] },
                { label: 'Company', links: ['About'] },
                { label: 'Community', links: ['Privacy'] },
                { label: 'Legal', links: ['Terms'] }
            ].map((col, i) => (
                <div key={i} className="flex flex-col gap-2">
                <span className="text-gray-500 text-[9px] uppercase tracking-wider font-bold">
                    {col.label}
                </span>
                {col.links.map(link => (
                    <span key={link} className="text-gray-300 text-[10px] whitespace-nowrap opacity-80 hover:opacity-100 transition-opacity cursor-default">
                    {link}
                    </span>
                ))}
                </div>
            ))}
            </div>

          </div>
        </div>

        {/* Small Footer Copyright */}
        <p className="mt-20 text-gray-600 text-[10px] tracking-widest uppercase">
          © 2026 TaskLedger
        </p>

      </div>
    </section>
  );
}

export default WhySection;