import React from 'react';

type StatsBlockProps = {
  label: string;
  value: number | string | string[];
  c?: string;
};

const StatsBlock: React.FC<StatsBlockProps> = ({ label, value, c }) => {
  return (
    <div className='flex flex-col sm:flex-row items-center justify-between py-4 px-6 bg-gray-100 rounded-lg shadow-md'>
      <div className='text-gray-600'>{label}</div>
      <div
        className={`${c} text-2xl font-bold text-gray-900 mt-2 sm:mt-0 break-words`}
      >
        {value}
      </div>
    </div>
  );
};

export default StatsBlock;
