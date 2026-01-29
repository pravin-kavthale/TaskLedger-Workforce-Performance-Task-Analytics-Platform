import React from 'react';

const PhilosophyCard = ({ title, desc }) => (
  <div className="bg-[#161b22]/50 border border-white/5 p-6 rounded-2xl hover:border-white/10 transition-all hover:bg-white/[0.04] backdrop-blur-sm group">
    <h3 className="text-white font-bold text-sm mb-3 tracking-wide group-hover:text-[#22d3ee] transition-colors">
      {title}
    </h3>
    <p className="text-[11px] text-gray-500 leading-relaxed font-medium">
      {desc}
    </p>
  </div>
);

const MissionNode = ({ text }) => (
  <div className="flex items-center gap-3 bg-white/[0.03] border border-white/10 px-4 py-2 rounded-lg w-fit transition-all hover:border-[#22d3ee]/40">
    <div className="w-4 h-4 rounded-full border border-[#22d3ee] flex items-center justify-center">
      <div className="w-1.5 h-1.5 bg-[#22d3ee] rounded-full shadow-[0_0_10px_#22d3ee]" />
    </div>
    <span className="text-[10px] text-gray-400 font-mono tracking-tight">
      {text}
    </span>
  </div>
);

export default function AboutMissions() {
  return (
    <section className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-start">

      <div className="space-y-10">
        <h2 className="text-3xl font-bold tracking-tight">Our Mission</h2>

        <div className="relative flex items-center min-h-[220px]">

          <svg
            className="absolute left-0 top-1/2 -translate-y-1/2 w-56 h-56 pointer-events-none hidden lg:block"
            viewBox="0 0 100 100"
          >
            <path
              d="M5,50 H25 M25,50 L65,15 M25,50 L65,38 M25,50 L65,62 M25,50 L65,85"
              fill="none"
              stroke="#22d3ee"
              strokeWidth="0.7"
              strokeDasharray="3 3"
              opacity="0.3"
            />
            <circle cx="5" cy="50" r="2.5" fill="#22d3ee" />
            <circle cx="25" cy="50" r="2" fill="#22d3ee" opacity="0.6" />
          </svg>

          <div className="lg:ml-36 space-y-4">
            <MissionNode text="Task Created by User X" />
            <MissionNode text="Assigned for Progress" />
            <MissionNode text="Completed by User Y" />
            <MissionNode text="Verified by Manager" />
          </div>
        </div>
      </div>

      <div className="space-y-14">
        <div>
          <h2 className="text-3xl font-bold mb-4 tracking-tight">
            The Work Ledger
          </h2>
          <p className="text-gray-400 text-sm leading-relaxed max-w-md font-medium">
            Every action is a verifiable event. TaskLedger records who did what and when,
            creating an <span className="text-white font-semibold underline decoration-[#22d3ee] underline-offset-4">
              immutable ledger of work
            </span>.
          </p>
        </div>

        <div className="space-y-6">
          <h2 className="text-3xl font-bold tracking-tight">
            Core Philosophy
          </h2>

          <div className="grid grid-cols-2 gap-5">
            <PhilosophyCard
              title="Accountability"
              desc="Clear ownership and verifiable actions ensure responsibility across teams."
            />
            <PhilosophyCard
              title="Traceability"
              desc="Complete audit trails make progress visible, measurable, and defensible."
            />
          </div>
        </div>
      </div>
    </section>
  );
}
