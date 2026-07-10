'use client'
import React from 'react';
import Link from 'next/link';
import { FaRegBell } from "react-icons/fa6";
import { FaMagnifyingGlass } from "react-icons/fa6";
import { IoHome } from "react-icons/io5";

export default function Sidebar() {
    return (<div className="fixed top-0 h-screen w-48 bg-gray-800 text-white shadow-lg flex flex-col items-start p-4 space-y-4">
        <nav className="w-full">
          <ul className="flex flex-col space-y-3">
            <li>
              <a
                href="/"
                className="flex gap-x-2 px-4 py-2 rounded-md hover:bg-gray-700 transition-colors duration-200"
              >
                <IoHome />
                 Home
              </a>
            </li>
            <li>
                
              <a
                href="#"
                className="px-4 gap-x-2 py-4 rounded-md hover:bg-gray-700 transition-colors duration-200 flex"
              >
                <FaRegBell/>
                Explore
              </a>
            </li>
            <li>
              <a
                href="#"
                className="flex gap-x-2 px-4 py-2 rounded-md hover:bg-gray-700 transition-colors duration-200"
              >
                <FaMagnifyingGlass />

                Notification
              </a>
            </li>
          </ul>
        </nav>
      </div>
    );
};
