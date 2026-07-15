"use client";

import ProfilePic from "@/app/components/ProfilePic";
import Tweet from "@/app/components/Tweet";
import { use } from "react";
import { useEffect, useState, useCallback, useRef } from "react";
import RightSidebar from "@/app/components/RightSideBar";
import Sidebar from "@/app/components/Sidebar";
import { api } from "@/app/lib/api";

const PAGE_SIZE = 10;

export default function Userpage({ params }) {
  const [profile, setProfile] = useState(null);
  const [tweets, setTweets] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(false);
  const sentinelRef = useRef(null);
  const { id } = use(params);

  const fetchPosts = useCallback(
    async (page = 0) => {
      setLoading(true);
      try {
        const data = await api.getUserPosts(id, page, PAGE_SIZE);
        if (page === 0) {
          setTweets(data.content);
        } else {
          setTweets((prev) => [...prev, ...data.content]);
        }
        setCurrentPage(data.number);
        setTotalPages(data.totalPages);
      } catch (error) {
        console.log("ERROR FETCHING POSTS", error);
      } finally {
        setLoading(false);
      }
    },
    [id]
  );

  useEffect(() => {
    async function fetchProfile() {
      try {
        const profileData = await api.getUser(id);
        setProfile(profileData);
        fetchPosts(0);
      } catch (error) {
        console.log("ERROR FETCHING DATA", error);
        setProfile(null);
      }
    }
    fetchProfile();
  }, [id, fetchPosts]);

  useEffect(() => {
    if (!sentinelRef.current) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (
          entry.isIntersecting &&
          !loading &&
          currentPage + 1 < totalPages
        ) {
          fetchPosts(currentPage + 1);
        }
      },
      { threshold: 0.1 }
    );
    observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [loading, currentPage, totalPages, fetchPosts]);

  if (!profile) {
    return (
      <div className="flex justify-center min-h-screen bg-background">
        <Sidebar />
        <main className="flex-1 max-w-[600px] ml-72 mr-80 min-h-screen border-r border-border">
          <div className="flex items-center justify-center h-64">
            <div className="w-8 h-8 border-2 border-accent border-t-transparent rounded-full animate-spin" />
          </div>
        </main>
        <RightSidebar />
      </div>
    );
  }

  return (
    <div className="flex justify-center min-h-screen bg-background">
      <Sidebar />
      <main className="flex-1 max-w-[600px] ml-72 mr-80 min-h-screen border-r border-border">
        <div className="bg-surface border-b border-border">
          <div className="px-4 py-4">
            <ProfilePic imgURL={profile.profilePictureUrl} size="large" />
            <h1 className="text-xl font-bold text-text-primary mt-3">
              {profile.username}
            </h1>
            {profile.bio && (
              <p className="text-text-secondary text-[15px] mt-1">
                {profile.bio}
              </p>
            )}
            <div className="flex gap-5 mt-3">
              <span className="text-[15px]">
                <span className="font-bold text-text-primary">
                  {profile.followers}
                </span>{" "}
                <span className="text-text-secondary">Followers</span>
              </span>
              <span className="text-[15px]">
                <span className="font-bold text-text-primary">
                  {profile.following}
                </span>{" "}
                <span className="text-text-secondary">Following</span>
              </span>
            </div>
          </div>
        </div>

        <div>
          {tweets.map((tweet) => (
            <Tweet
              key={tweet.id}
              tweet={tweet}
              setTweets={setTweets}
            />
          ))}
        </div>

        {currentPage + 1 < totalPages ? (
          <div
            ref={sentinelRef}
            className="h-16 flex justify-center items-center"
          >
            {loading && (
              <div className="w-6 h-6 border-2 border-accent border-t-transparent rounded-full animate-spin" />
            )}
          </div>
        ) : tweets.length > 0 ? (
          <p className="text-center text-text-secondary text-sm py-8">
            You&apos;ve reached the end
          </p>
        ) : !loading ? (
          <p className="text-center text-text-secondary text-sm py-12">
            No posts yet
          </p>
        ) : null}
      </main>
      <RightSidebar />
    </div>
  );
}
