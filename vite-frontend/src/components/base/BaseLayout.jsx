import React from 'react';
import Navbar from './Navbar';
import Sidebar from './Sidebar';

export default function BaseLayout({ children }) {
  return (
    <div className="flex flex-col min-h-screen bg-[#0a0f12] text-white">
      <Navbar />
      <div className="flex flex-1 min-h-0">
        <Sidebar />
        <main className="flex-1 overflow-auto p-6 md:p-8 bg-[#0a0f12]">
          {children}
        </main>
      </div>
    </div>
  );
}
