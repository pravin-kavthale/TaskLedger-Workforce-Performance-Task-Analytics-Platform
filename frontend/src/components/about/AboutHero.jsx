import React from 'react';
import { Search, GitBranch, UserCheck, Workflow, ShieldCheck, ListTodo, Zap } from 'lucide-react';


const Card = ({ icon: Icon, title }) => (
  <div className="relative bg-white/[0.03] border border-white/10 p-5 rounded-2xl transition-all duration-500 group overflow-hidden hover:bg-white/[0.05] hover:border-[#22d3ee]/30">
    <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-[#22d3ee] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      <div className="absolute inset-0 w-1/3 h-full bg-[#22d3ee] shadow-[0_0_15px_#22d3ee] animate-trace-right"></div>
    </div>
    <div className="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-[#22d3ee] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      <div className="absolute inset-0 w-1/3 h-full bg-[#22d3ee] shadow-[0_0_15px_#22d3ee] animate-trace-left"></div>
    </div>

    <div className="relative z-10">
      <Icon className="text-[#22d3ee] w-6 h-6 mb-2 drop-shadow-[0_0_8px_rgba(34,211,238,0.5)]" />
      <div className="w-8 h-[2px] bg-[#22d3ee] mb-3 rounded-full opacity-80"></div>
      <h3 className="text-white text-sm font-bold mb-1 tracking-tight">{title}</h3>
    </div>

    <div className="absolute -inset-24 bg-[#22d3ee]/5 blur-[40px] rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
  </div>
);

function Features() {
  const pillars = [
    { icon: Search, title: "Transparency" },
    { icon: GitBranch, title: "Traceability" },
    { icon: UserCheck, title: "Accountability" }
  ];

  return (
    <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
      {pillars.map((pillar, index) => (
        <Card key={index} {...pillar} />
      ))}
    </div>
  );
}

export default function AboutHero() {
  return (
    <section className="relative min-h-[60vh] flex items-center bg-[#0a0f12] py-20 px-8 md:px-16 lg:px-24">
      <div className="max-w-7xl mx-auto w-full grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
        
        <div>
          <h1 className="text-4xl md:text-6xl font-black leading-tight tracking-tight text-white">
            About <span className="text-[#4fd1c5]">TaskLedger</span>
          </h1>
          <p className="mt-4 text-gray-400 text-base max-w-lg leading-relaxed opacity-90">
            Building Accountability, One Event at Time. Every action is a verifiable event, 
            creating a permanent ledger of work.
          </p>

          <div className="mt-8 flex flex-wrap gap-4">
            <button className="bg-[#4fd1c5] text-[#1a1f26] px-8 py-3 rounded-full font-black text-xs uppercase transition-all shadow-xl shadow-teal-500/20 active:scale-95 hover:bg-[#3db8ae]">
              Get Started Now
            </button>
            <button className="border border-[#22d3ee]/30 text-white px-8 py-3 rounded-full font-bold text-xs uppercase bg-white/5 backdrop-blur-sm hover:bg-white/10 transition-colors">
              Explore Features
            </button>
          </div>
        </div>

        <div>
          <Features />
        </div>
        
      </div>
    </section>
  );
}