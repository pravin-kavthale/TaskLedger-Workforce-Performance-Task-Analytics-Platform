import React from 'react';
import { ShieldCheck, History } from 'lucide-react';

const MissionNode = ({ label, status, isLast }) => (
  <div className="relative flex items-center gap-3 mb-4 last:mb-0">
    {!isLast && (
      <div className="absolute left-[9px] top-6 w-[2px] h-6 bg-gradient-to-b from-[#22d3ee]/40 to-transparent"></div>
    )}
    <div className="relative">
      <div className="w-5 h-5 rounded-full bg-[#1a1f26] border-2 border-[#22d3ee] z-10 relative shadow-[0_0_10px_rgba(34,211,238,0.3)]"></div>
      <div className="absolute inset-0 w-5 h-5 bg-[#22d3ee] rounded-full blur-md opacity-20"></div>
    </div>
    <div className="bg-white/[0.03] border border-white/10 px-3 py-1.5 rounded-lg group-hover:border-[#22d3ee]/50 transition-colors">
      <p className="text-[10px] font-mono text-gray-400">
        <span className="text-[#22d3ee]/80">{label}</span>
        <span className="mx-2 opacity-30">|</span>
        <span className="text-gray-300">{status}</span>
      </p>
    </div>
  </div>
);

export default function AboutMissions() {
  const steps = [
    { label: "TASK_INIT", status: "User_Alpha" },
    { label: "NODE_ASSIGN", status: "Eng_Beta" },
    { label: "STATE_PUSH", status: "In_Progress" },
  ];

  return (
    <>
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center py-6">
        
        {/* Left Side: Interactive Ledger Graph */}
        <div className="relative pl-2 py-4 border-l border-white/5">
          <div className="absolute -left-[1px] top-0 h-8 w-[1px] bg-gradient-to-b from-[#22d3ee] to-transparent"></div>
          <h2 className="text-[#22d3ee] font-mono text-[10px] mb-8 tracking-[0.2em] uppercase opacity-70">
            // OPERATIONAL_LOG.EXE
          </h2>
          <div className="space-y-1">
            {steps.map((s, i) => (
              <MissionNode key={i} {...s} isLast={i === steps.length - 1} />
            ))}
          </div>
        </div>

        {/* Right Side: Content */}
        <div className="flex flex-col justify-center space-y-6">
          <div>
            {/* Fix: Bigger, bolder heading with character tracking */}
            <h3 className="text-3xl font-black text-white tracking-tight mb-3">
              The Work <span className="text-[#4fd1c5]">Ledger</span>
            </h3>
            <p className="text-gray-400 text-sm leading-relaxed max-w-sm">
              Every action within TaskLedger is a verifiable event. We create an 
              <span className="text-white font-medium"> immutable chain of truth </span> 
              for every project milestone.
            </p>
          </div>

          {/* Icon Section with cleaner alignment */}
          <div className="flex gap-6 pt-2">
             <div className="group flex items-center gap-2">
               <div className="p-2 rounded-lg bg-[#22d3ee]/5 border border-[#22d3ee]/10 group-hover:bg-[#22d3ee]/10 transition-colors">
                 <ShieldCheck size={16} className="text-[#22d3ee]" />
               </div>
               <div className="flex flex-col">
                 <span className="text-[10px] font-black text-white uppercase tracking-wider">Accountability</span>
                 <span className="text-[9px] text-gray-500 uppercase tracking-tighter">Verified</span>
               </div>
             </div>

             <div className="group flex items-center gap-2">
               <div className="p-2 rounded-lg bg-[#22d3ee]/5 border border-[#22d3ee]/10 group-hover:bg-[#22d3ee]/10 transition-colors">
                 <History size={16} className="text-[#22d3ee]" />
               </div>
               <div className="flex flex-col">
                 <span className="text-[10px] font-black text-white uppercase tracking-wider">Traceability</span>
                 <span className="text-[9px] text-gray-500 uppercase tracking-tighter">Immutable</span>
               </div>
             </div>
          </div>
        </div>
        
      </div>
    </>
  );
}