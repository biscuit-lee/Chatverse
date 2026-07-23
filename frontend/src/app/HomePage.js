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
  const [posting, setPosting] = useState(false);
  const [postError, setPostError] = useState("");
  const [sortType, setSortType] = useState("new");
  const formRef = useRef(null);
  const sentinelRef = useRef(null);
  const { logout } = useAuth();

  const fetchPosts = useCallback(async (page = 0) => {
    setLoading(true);
    try {
      const data = await api.getPosts(page, PAGE_SIZE, sortType);
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
  }, [sortType]);

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
    const formData = new FormData(formRef.current);
    const content = formData.get("tweet");
    if (!content.trim()) return;

    setPosting(true);
    setPostError("");
    try {
      const newPost = await api.createPost(content);
      setTweets((prev) => [newPost, ...prev]);
      formRef.current.reset();
    } catch (error) {
      setPostError("Failed to post. Please try again.");
    } finally {
      setPosting(false);
    }
  }

  return (
    <div className="flex-1 min-w-0 border-r border-border">
      <div className="sticky top-0 bg-surface/80 backdrop-blur-md border-b border-border px-4 py-3 z-10">
        <div className="flex items-center justify-between">
          <h1 className="font-bold text-xl text-text-primary">Home</h1>
          <button
            onClick={logout}
            className="text-sm text-text-secondary hover:text-danger transition-colors duration-200 cursor-pointer"
          >
            Logout
          </button>
        </div>
        <div className="flex mt-3">
          <button
            onClick={() => setSortType("new")}
            className={`flex-1 text-center py-3 text-[15px] font-medium transition-colors duration-200 cursor-pointer ${
              sortType === "new"
                ? "text-text-primary border-b-2 border-accent"
                : "text-text-secondary hover:text-text-primary hover:bg-white/5"
            }`}
          >
            For you
          </button>
          <button
            onClick={() => setSortType("hot")}
            className={`flex-1 text-center py-3 text-[15px] font-medium transition-colors duration-200 cursor-pointer ${
              sortType === "hot"
                ? "text-text-primary border-b-2 border-accent"
                : "text-text-secondary hover:text-text-primary hover:bg-white/5"
            }`}
          >
            Top
          </button>
        </div>
      </div>

      <form
        ref={formRef}
        onSubmit={postTweet}
        className="flex items-start gap-3 px-4 py-4 border-b border-border bg-surface"
      >
        <div className="flex-1">
          <input
            autoComplete="off"
            placeholder="What's happening?"
            name="tweet"
            type="text"
            className="w-full bg-transparent text-text-primary placeholder:text-text-secondary outline-none text-[15px] py-2"
          />
          {postError && (
            <p className="text-danger text-sm mt-1">{postError}</p>
          )}
        </div>
        <button
          disabled={posting}
          className="bg-accent text-white font-bold px-5 py-2 rounded-full hover:bg-accent-hover disabled:opacity-50 transition-colors duration-200 text-[15px] shrink-0 cursor-pointer"
        >
          {posting ? "..." : "Post"}
        </button>
      </form>

      <div>
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
          No posts yet. Be the first to post!
        </p>
      ) : null}
    </div>
  );
}
