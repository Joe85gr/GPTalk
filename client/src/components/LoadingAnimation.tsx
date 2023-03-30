import React from 'react';

 export const LoadingAnimation: React.FC = () => {
    return (
        <div className="p-4">
                <div className="flex items-center justify-center space-x-2 animate-pulse">
                    <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
                    <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
                    <div className="w-2 h-2 bg-gray-300 rounded-full"></div>
                </div>
        </div>
    )
  }

