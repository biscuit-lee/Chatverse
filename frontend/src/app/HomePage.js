"use client";
import { useEffect, useState, useCallback, useRef } from "react";
import { api } from "./lib/api";
import Tweet from "./components/Tweet";
import { useAuth } from "./lib/AuthContext";

const PAGE_SIZE = 10;

export default function HomePage() {
  const [tweets, setTweets] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(false);
  const sentinelRef = useRef(null);
  const { logout } = useAuth();

  const fetchPosts = useCallback(async (page = 0) => {
    setLoading(true);
    try {
      const data = await api.getPosts(page, PAGE_SIZE);
      if (page === 0) {
        setTweets(data.content);
      } else {
        setTweets((prev) => [...prev, ...data.content]);
      }
      setCurrentPage(data.number);
      setTotalPages(data.totalPages);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchPosts(0);
  }, [fetchPosts]);

  useEffect(() => {
    if (!sentinelRef.current) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !loading && currentPage + 1 < totalPages) {
          fetchPosts(currentPage + 1);
        }
      },
      { threshold: 0.1 }
    );
    observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [loading, currentPage, totalPages, fetchPosts]);

  async function postTweet(event) {
    event.preventDefault();
    const formData = new FormData(event.currentTarget);
    const content = formData.get("tweet");
    if (!content.trim()) return;

    try {
      await api.createPost(content);
      event.currentTarget.reset();
      fetchPosts(0);
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <div className="flex-1 ml-97 p-8 w-1/2">
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-xl font-bold">Feed</h1>
        <button
          onClick={logout}
          className="text-sm text-gray-500 hover:text-red-500 transition-colors"
        >
          Logout
        </button>
      </div>

      <form onSubmit={postTweet} className="flex">
        <input
          autoComplete="off"
          placeholder="What's poppin"
          name="tweet"
          type="text"
          className="w-3/4 max-w-xl h-16 bg-transparent border-none outline-none text-left text-lg"
        />
        <button className="bg-blue-500 text-white h-14 px-3 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300">
          Post
        </button>
      </form>

      <div className="">
        {tweets.map((tweet) => (
          <Tweet
            key={tweet.id}
            tweet={tweet}
            setTweets={setTweets}
            isComment={false}
          />
        ))}
      </div>

      {currentPage + 1 < totalPages ? (
        <div ref={sentinelRef} className="h-10 flex justify-center items-center my-6">
          {loading && <p className="text-gray-500">Loading...</p>}
        </div>
      ) : tweets.length > 0 ? (
        <p className="text-center text-gray-400 text-sm my-6">End of feed</p>
      ) : null}
    </div>
  );
}
