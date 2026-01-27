import React from 'react';
import { Search, Settings, ShieldCheck } from 'lucide-react';

const HeroCard = ({ icon: Icon, title }) => (
  <div className="flex-1 min-w-[160px] bg-white/[0.04] border border-white/10 p-8 rounded-2xl flex flex-col items-center justify-center gap-4 backdrop-blur-md transition-all hover:shadow-[0_0_40px_rgba(34,211,238,0.15)]">
    <Icon size={36} strokeWidth={1.4} className="text-[#22d3ee]" />
    <span className="text-white text-[12px] font-bold tracking-widest uppercase">
      {title}
    </span>
  </div>
);

export default function AboutHero() {
  return (
    <section className="grid grid-cols-1 lg:grid-cols-[1.2fr_0.8fr] gap-16 items-center">
      
      <div>
        <h1 className="text-5xl md:text-6xl font-black leading-tight tracking-tight mb-4">
          About TaskLedger
        </h1>

        <p className="text-gray-400 text-lg max-w-md mb-10">
          Building accountability, one verifiable event at a time.
        </p>

        <div className="flex gap-4">
          <button className="bg-[#4fd1c5] text-[#1a1f26] px-8 py-3 rounded-full font-black text-xs uppercase shadow-xl shadow-teal-500/20 active:scale-95">
            Get Started Now
          </button>

          <button className="border border-white/20 px-8 py-3 rounded-full text-xs uppercase bg-white/5 backdrop-blur-sm">
            Explore Features
          </button>
        </div>
      </div>

      <div className="flex gap-6 flex-wrap">
        <HeroCard title="Transparency" icon={Search} />
        <HeroCard title="Traceability" icon={Settings} />
        <HeroCard title="Accountability" icon={ShieldCheck} />
      </div>
    </section>
  );
}
