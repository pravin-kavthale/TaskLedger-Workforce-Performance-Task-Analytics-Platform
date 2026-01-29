import React from 'react';
import { Workflow, ShieldCheck, ListTodo, Zap } from 'lucide-react';

const FeatureCard = ({ icon: Icon, title, description }) => (
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
      <p className="text-gray-400 text-[10px] leading-relaxed font-light">{description}</p>
    </div>
    <div className="absolute -inset-24 bg-[#22d3ee]/5 blur-[40px] rounded-full opacity-0 group-hover:opacity-100 transition-opacity duration-700"></div>
  </div>
);

function Features() {
  const features = [
    { icon: Workflow, title: "Workflow Engine", description: "Manage complex tasks and milestones seamlessly." },
    { icon: ShieldCheck, title: "RBAC Security", description: "Granular access to keep sensitive data protected." },
    { icon: ListTodo, title: "Activity Logs", description: "Full audit trails for every change and action." },
    { icon: Zap, title: "Real-time Sync", description: "Instant updates across all platforms instantly." }
  ];

  return (
    <section className="relative bg-transparent py-2 px-8 md:px-16 lg:px-24">
      <div className="max-w-7xl mx-auto">
        <div className="mb-4 flex flex-col items-start">
          <h2 className="text-white font-black text-lg uppercase tracking-[0.3em] leading-none">Features</h2>
          <div className="w-12 h-[3px] bg-[#22d3ee] mt-2 rounded-full shadow-[0_0_10px_rgba(34,211,238,0.6)]"></div>
        </div>
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {features.map((feature, index) => (
            <FeatureCard key={index} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
}

export default Features;