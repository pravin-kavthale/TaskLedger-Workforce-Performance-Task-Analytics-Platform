import React from 'react';
import BaseLayout from '../components/base/BaseLayout';

export default function BasePage() {
  return (
    <BaseLayout>
      <div className="rounded-2xl bg-[#1a1f26]/80 border border-white/5 p-6 min-h-[400px]">
        {/* Content area – no dashboards for now */}
        <p className="text-gray-500 text-sm">Content area. Add views here later.</p>
      </div>
    </BaseLayout>
  );
}
