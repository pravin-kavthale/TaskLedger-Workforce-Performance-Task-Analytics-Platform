import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';


import Navbar from './components/sections/Navbar'; 
import Home from './pages/Home';
import About from './pages/About';

function App() {
  return (
    <Router>
      <div className="flex flex-col min-h-screen bg-[#0a0f12] text-white">
        <Navbar />
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/about" element={<About />} />
            <Route path="*" element={<Home />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;