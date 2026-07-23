"use client";
import { useState } from "react";
import { useAuth } from "./lib/AuthContext";
import HomePage from "./HomePage";
import LoginPage from "./components/LoginPage";
import SearchResults from "./components/SearchResults";
import Sidebar from "./components/Sidebar";
import RightSideBar from "./components/RightSideBar";

export default function Home() {
  const { user, loading } = useAuth();
  const [view, setView] = useState("home");
  const [searchQuery, setSearchQuery] = useState("");

  if (loading) return null;

  if (!user) {
    return <LoginPage />;
  }

  function handleSearch(query) {
    setSearchQuery(query);
    setView("search");
  }

  function handleBack() {
    setView("home");
  }

  function handleExplore() {
    setView("search");
    setSearchQuery("");
  }

  return (
    <div className="flex justify-center min-h-screen bg-background">
      <Sidebar onExplore={handleExplore} />
      <main className="flex-1 max-w-[600px] ml-72 mr-80 min-h-screen border-r border-border">
        {view === "home" ? (
          <HomePage />
        ) : (
          <SearchResults query={searchQuery} onBack={handleBack} />
        )}
      </main>
      <RightSideBar onSearch={handleSearch} />
    </div>
  );
}
