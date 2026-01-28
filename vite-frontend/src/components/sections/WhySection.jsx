import React from 'react';
import { Plus, UserCheck, BarChart3, MoveRight } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

const Step = ({ icon: Icon, label }) => (
  <div className="flex flex-col items-center group">
    <div className="w-10 h-10 rounded-full border border-[#22d3ee]/30 flex items-center justify-center bg-[#1a1f26] group-hover:border-[#22d3ee] transition-all">
      <Icon className="text-[#22d3ee] w-4 h-4" />
    </div>
    <p className="mt-2 text-gray-400 text-[8px] font-bold uppercase tracking-[0.2em] text-center">{label}</p>
  </div>
);

function WhySection() {

  const navigate = useNavigate();

  return (
    <section className="bg-transparent pt-6 pb-8 px-8 md:px-16 lg:px-24 border-t border-white/5">
      <div className="max-w-7xl mx-auto">
        <div className="mb-6 flex flex-col items-start">
          <h2 className="text-white font-black text-lg uppercase tracking-[0.3em] leading-none">Why TaskLedger?</h2>
          <div className="w-16 h-[3px] bg-[#22d3ee] mt-2 rounded-full shadow-[0_0_10px_rgba(34,211,238,0.5)]"></div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[1fr_auto] gap-8 items-center">
          <div className="flex items-center gap-6">
            <Step icon={Plus} label="Transparency" />
            <MoveRight className="text-white/10 w-4 h-4" />
            <Step icon={UserCheck} label="Accountability" />
            <MoveRight className="text-white/10 w-4 h-4" />
            <Step icon={BarChart3} label="Faster Work" />
          </div>

          <div className="flex items-center gap-6">
            <div className="flex flex-col items-center lg:items-end gap-3">
              <button 
                onClick={() => navigate('/login')}
                className="px-10 py-2 rounded-full font-black text-[10px] uppercase tracking-widest text-[#1a1f26] bg-[#22d3ee] shadow-[0_0_20px_rgba(34,211,238,0.3)] active:scale-95 transition-all">
                Login
              </button>
            </div>

            <div className="grid grid-cols-5 gap-4 border border-white/10 bg-white/[0.02] backdrop-blur-md rounded-xl px-6 py-3">
              {['Product', 'Home', 'Company', 'Community', 'Legal'].map((label) => (
                <div key={label} className="flex flex-col">
                  <span className="text-gray-500 text-[7px] uppercase font-bold">{label}</span>
                  <span className="text-gray-300 text-[8px] opacity-60">Info</span>
                </div>
              ))}
            </div>
          </div>
        </div>
        <p className="mt-6 text-gray-600 text-[8px] tracking-widest uppercase">© 2026 TaskLedger</p>
      </div>
    </section>
  );
}

export default WhySection;