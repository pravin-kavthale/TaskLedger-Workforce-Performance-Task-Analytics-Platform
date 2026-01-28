import React from 'react';
import LoginForm from '../components/auth/LoginForm';

const Login = () => {
  return (
    <main className="h-screen w-full bg-[#0a0f12] text-white flex items-center justify-center overflow-hidden relative">
      {/* GLOBAL BACKGROUND GLOW - Sky Blue focused on center */}
      <div 
        className="absolute w-[600px] h-[600px] pointer-events-none opacity-20"
        style={{
          background: 'radial-gradient(circle, rgba(34, 211, 238, 0.3) 0%, transparent 70%)',
          filter: 'blur(80px)'
        }}
      />

      {/* LOGIN COMPONENT */}
      <LoginForm />

      {/* FOOTER DECORATION */}
      <div className="absolute bottom-8 text-[10px] font-mono text-gray-600 tracking-[0.3em] uppercase">
        System_Status: Operational // SSL_Encrypted
      </div>
    </main>
  );
};

export default Login;