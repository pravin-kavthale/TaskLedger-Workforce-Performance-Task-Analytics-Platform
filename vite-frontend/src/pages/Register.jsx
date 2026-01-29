import React from 'react';
import RegisterForm from '../components/auth/RegisterForm';

const Register = () => {
  return (
    <main className="min-h-screen w-full bg-[#0a0f12] text-white flex items-center justify-center py-20 overflow-x-hidden relative">
      {/* GLOBAL BACKGROUND GLOW - Slightly wider for the larger registration card */}
      <div 
        className="absolute w-[800px] h-[800px] pointer-events-none opacity-20"
        style={{
          background: 'radial-gradient(circle, rgba(34, 211, 238, 0.25) 0%, transparent 70%)',
          filter: 'blur(100px)'
        }}
      />

      {/* REGISTRATION FORM COMPONENT */}
      <RegisterForm />

      {/* SYSTEM DECORATION */}
      <div className="absolute bottom-8 hidden md:block text-[10px] font-mono text-gray-600 tracking-[0.3em] uppercase">
        Node_Protocol: v2.04 // Registry_Open
      </div>
    </main>
  );
};

export default Register;