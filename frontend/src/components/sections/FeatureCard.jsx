import React from 'react';
import { Workflow, ShieldCheck, ListTodo, Zap } from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description }) => (
  <div className="relative bg-white/[0.03] border border-white/10 p-8 rounded-3xl transition-all duration-500 group overflow-hidden hover:bg-white/[0.05] hover:border-[#22d3ee]/30">
    
    {/* --- HOVER ANIMATIONS (Tracing Lines) --- */}
    {/* Top Line: Moves Left to Right */}
    <div className="absolute top-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-[#22d3ee] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      <div className="absolute inset-0 w-1/3 h-full bg-[#22d3ee] shadow-[0_0_15px_#22d3ee] animate-trace-right"></div>
    </div>
    
    {/* Bottom Line: Moves Right to Left */}
    <div className="absolute bottom-0 left-0 w-full h-[1px] bg-gradient-to-r from-transparent via-[#22d3ee] to-transparent opacity-0 group-hover:opacity-100 transition-opacity duration-300">
      <div className="absolute inset-0 w-1/3 h-full bg-[#22d3ee] shadow-[0_0_15px_#22d3ee] animate-trace-left"></div>
    </div>

    {/* --- CONTENT --- */}
    <div className="relative z-10">
      {/* Icon: No box, just the icon with a glow like in the image */}
      <Icon className="text-[#22d3ee] w-8 h-8 mb-4 drop-shadow-[0_0_8px_rgba(34,211,238,0.5)]" />
      
      {/* Small Accent Line below icon - matches unnamed.jpg */}
      <div className="w-10 h-[2px] bg-[#22d3ee] mb-6 rounded-full opacity-80"></div>

      <h3 className="text-white text-xl font-semibold mb-3 tracking-tight">
        {title}
      </h3>
      
      <p className="text-gray-400 text-sm leading-relaxed font-light">
        {description}
      </p>
    </div>

    {/* Subtle Inner Glow on Hover */}
    <div className="absolute -inset-24 bg-[#22d3ee]/5 blur-[60px] rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
  </div>
);

function Features() {
  const features = [
    { icon: Workflow, title: "Project & Workflow Engine", description: "Manage complex workflows with nested tasks and milestones seamlessly." },
    { icon: ShieldCheck, title: "RBAC Security", description: "Granular role-based access to keep sensitive data protected at all times." },
    { icon: ListTodo, title: "Activity Logs", description: "Full audit trails for every change, ensuring team transparency and reflexivity." },
    { icon: Zap, title: "Real-time Sync", description: "Instant updates across all platforms without ever needing to refresh." }
  ];

  return (
    <section className="relative bg-[#1a1f26] py-32 px-8 md:px-16 lg:px-24">
      <div className="max-w-7xl mx-auto">
        {/* Section Header matches the spaced-out cyan text in image */}
        <div className="mb-20 flex flex-col items-center lg:items-start">
    {/* We use font-sans and font-black (900 weight) for that thick, premium look */}
    <h2 className="text-white font-sans font-black text-2xl md:text-3xl uppercase tracking-widest leading-none">
        Features
    </h2>
    
    {/* The Cyan underline is crucial for that 'TaskLedger' brand identity */}
    <div className="w-16 h-[4px] bg-[#22d3ee] mt-4 rounded-full shadow-[0_0_15px_rgba(34,211,238,0.6)]"></div>
    </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <FeatureCard key={index} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default Features;