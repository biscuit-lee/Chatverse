'use client'
import React from 'react';
import Link from 'next/link';

export default function RightSidebar() {
    return (
    
    <div className="fixed top-0 right-0 h-screen w-40 bg-gray-800 text-white p-4 flex flex-col justify-start space-y-4">
        <div className="bg-gray-700 p-3 rounded hover:bg-gray-600 cursor-pointer">
            Trending

        </div>
        <div className="bg-gray-700 p-3 rounded hover:bg-gray-600 cursor-pointer"> Who to follow </div>
        <div className="bg-gray-700 p-3 rounded hover:bg-gray-600 cursor-pointer">📞 Contact</div>
      </div>
    );
};
