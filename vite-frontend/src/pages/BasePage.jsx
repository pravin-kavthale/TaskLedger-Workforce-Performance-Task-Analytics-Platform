import React, { useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import BaseLayout from '../components/base/BaseLayout';

export default function BasePage() {
  const location = useLocation();
  const [showPopup, setShowPopup] = useState(false);

  useEffect(() => {
    const params = new URLSearchParams(location.search);
    if (params.get('github_linked') === '1') {
      setShowPopup(true);

      // Remove the query param so it doesn't trigger again on refresh
      params.delete('github_linked');
      window.history.replaceState({}, '', location.pathname);

      const timer = setTimeout(() => setShowPopup(false), 5000);
      return () => clearTimeout(timer);
    }
  }, [location]);

  return (
    <BaseLayout>
      {showPopup && (
        <div style={{
          position: 'fixed',
          top: '20px',
          right: '20px',
          backgroundColor: '#4CAF50',
          color: 'white',
          padding: '15px',
          borderRadius: '5px',
          zIndex: 1000
        }}>
          GitHub account linked successfully!
        </div>
      )}

      <div className="rounded-2xl bg-[#1a1f26]/80 border border-white/5 p-6 min-h-[400px]">
        {/* Content area – no dashboards for now */}
        <p className="text-gray-500 text-sm">Content area. Add views here later.</p>
      </div>
    </BaseLayout>
  );
}