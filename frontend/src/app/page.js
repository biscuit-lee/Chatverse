"use client";
import { useAuth } from "./lib/AuthContext";
import HomePage from "./HomePage";
import LoginPage from "./components/LoginPage";
import Sidebar from "./components/Sidebar";
import RightSideBar from "./components/RightSideBar";

export default function Home() {
  const { user, loading } = useAuth();

  if (loading) return null;

  if (!user) {
    return (
      <div>
        <LoginPage />
      </div>
    );
  }

  return (
    <div>
      <RightSideBar />
      <Sidebar />
      <HomePage />
    </div>
  );
}
