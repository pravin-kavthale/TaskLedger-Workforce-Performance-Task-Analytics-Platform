import React from 'react';
import { Search, GitBranch, UserCheck } from 'lucide-react';

const Card = ({ icon: Icon, title }) => (
  <div className="bg-white/[0.03] border border-white/10 p-4 rounded-xl transition-all group hover:border-[#22d3ee]/30">
    <Icon className="text-[#22d3ee] w-5 h-5 mb-2" />
    <h3 className="text-white text-xs font-bold tracking-tight">{title}</h3>
  </div>
);

export default function AboutHero() {
  return (
    <>
      <div className="relative grid grid-cols-1 lg:grid-cols-2 gap-8 items-center py-4">
        {/* LIGHT GLOW BEHIND TITLE */}
        <div className="absolute -top-10 -left-10 w-64 h-64 bg-[#4fd1c5]/10 blur-[80px] rounded-full pointer-events-none"></div>
        
        <div className="relative z-10">
          <h1 className="text-4xl md:text-5xl font-black leading-tight text-white">
            About <span className="text-[#4fd1c5]">TaskLedger</span>
          </h1>
          <p className="mt-2 text-gray-400 text-sm max-w-md leading-relaxed">
            Building Accountability, One Event at Time. Every action is a verifiable event, 
            creating a permanent ledger of work.
          </p>
          <div className="mt-6 flex gap-3">
            <button className="bg-[#4fd1c5] text-[#1a1f26] px-6 py-2 rounded-full font-black text-[10px] uppercase shadow-lg shadow-teal-500/10">
              Get Started
            </button>
            <button className="border border-white/10 text-white px-6 py-2 rounded-full font-bold text-[10px] uppercase bg-white/5">
              Features
            </button>
          </div>
        </div>

        <div className="grid grid-cols-3 gap-3">
          <Card icon={Search} title="Transparency" />
          <Card icon={GitBranch} title="Traceability" />
          <Card icon={UserCheck} title="Accountability" />
        </div>
      </div>
    </>
  );
}