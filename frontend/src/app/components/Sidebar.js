"use client";
import React from "react";
import Link from "next/link";
import { FaRegBell } from "react-icons/fa6";
import { FaMagnifyingGlass } from "react-icons/fa6";
import { IoHome } from "react-icons/io5";

export default function Sidebar({ onExplore }) {
  const navItems = [
    { label: "Home", icon: <IoHome size={24} />, href: "/" },
    { label: "Explore", icon: <FaMagnifyingGlass size={22} />, href: "#", onClick: () => onExplore() },
    { label: "Notifications", icon: <FaRegBell size={22} />, href: "#" },
  ];

  return (
    <div className="fixed top-0 left-0 h-screen w-72 bg-surface border-r border-border flex flex-col justify-between py-4 px-4">
      <div>
        <Link href="/" className="flex items-center gap-2 px-4 py-3 mb-2">
          <span className="text-2xl font-bold text-text-primary">Chatverse</span>
        </Link>

        <nav className="mt-2">
          <ul className="flex flex-col gap-1">
            {navItems.map((item) => (
              <li key={item.label}>
                <a
                  href={item.href}
                  onClick={item.onClick}
                  className="flex items-center gap-4 px-4 py-3 rounded-full text-text-primary font-medium text-[15px] hover:bg-border transition-colors duration-200 cursor-pointer"
                >
                  {item.icon}
                  {item.label}
                </a>
              </li>
            ))}
          </ul>
        </nav>
      </div>

      <button className="w-full bg-accent text-white font-bold py-3 rounded-full hover:bg-accent-hover transition-colors duration-200 text-[15px] cursor-pointer">
        Post
      </button>
    </div>
  );
}
