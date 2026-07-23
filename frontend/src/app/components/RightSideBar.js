"use client";
import React, { useState } from "react";
import { FaMagnifyingGlass } from "react-icons/fa6";

const trending = [
  { topic: "Technology", title: "React 20", posts: "12.4K posts" },
  { topic: "Trending", title: "Web Development", posts: "8.2K posts" },
  { topic: "Gaming", title: "New Release", posts: "5.1K posts" },
];

const whoToFollow = [
  { name: "Suggested User", handle: "@suggested" },
  { name: "Another User", handle: "@another" },
];

export default function RightSidebar({ onSearch }) {
  const [searchValue, setSearchValue] = useState("");

  function handleKeyDown(e) {
    if (e.key === "Enter" && searchValue.trim()) {
      onSearch(searchValue.trim());
    }
  }

  return (
    <div className="fixed top-0 right-0 h-screen w-80 bg-surface border-l border-border flex flex-col gap-4 overflow-y-auto py-4 px-6">
      <div className="relative">
        <FaMagnifyingGlass
          size={16}
          className="absolute left-4 top-1/2 -translate-y-1/2 text-text-secondary"
        />
        <input
          type="text"
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Search"
          className="w-full bg-background border border-border rounded-full py-3 pl-12 pr-4 text-[15px] text-text-primary placeholder:text-text-secondary outline-none focus:border-accent focus:bg-surface transition-colors duration-200"
        />
      </div>

      <div className="bg-background rounded-2xl border border-border overflow-hidden">
        <h2 className="font-bold text-xl text-text-primary px-4 py-3">
          What&apos;s happening
        </h2>
        {trending.map((item, i) => (
          <div
            key={i}
            className="px-4 py-3 hover:bg-border/50 cursor-pointer transition-colors duration-200"
          >
            <p className="text-[13px] text-text-secondary">{item.topic}</p>
            <p className="font-bold text-[15px] text-text-primary">
              {item.title}
            </p>
            <p className="text-[13px] text-text-secondary">{item.posts}</p>
          </div>
        ))}
      </div>

      <div className="bg-background rounded-2xl border border-border overflow-hidden">
        <h2 className="font-bold text-xl text-text-primary px-4 py-3">
          Who to follow
        </h2>
        {whoToFollow.map((user, i) => (
          <div
            key={i}
            className="flex items-center justify-between px-4 py-3 hover:bg-border/50 transition-colors duration-200"
          >
            <div>
              <p className="font-bold text-[15px] text-text-primary">
                {user.name}
              </p>
              <p className="text-[13px] text-text-secondary">{user.handle}</p>
            </div>
            <button className="bg-text-primary text-surface text-sm font-bold rounded-full px-4 py-1.5 hover:opacity-90 transition-opacity duration-200 cursor-pointer">
              Follow
            </button>
          </div>
        ))}
      </div>
    </div>
  );
}
