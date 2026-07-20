"use client";
import { useEffect, useState, useCallback, useRef } from "react";
import { api } from "../lib/api";
import Tweet from "./Tweet";

const PAGE_SIZE = 10;

export default function SearchResults({ query, onBack }) {
  const [results, setResults] = useState([]);
  const [currentPage, setCurrentPage] = useState(0);
  const [totalPages, setTotalPages] = useState(0);
  const [loading, setLoading] = useState(false);
  const sentinelRef = useRef(null);

  const fetchResults = useCallback(async (page = 0) => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const data = await api.searchPosts(query, page, PAGE_SIZE);
      if (page === 0) {
        setResults(data.content);
      } else {
        setResults((prev) => [...prev, ...data.content]);
      }
      setCurrentPage(data.number);
      setTotalPages(data.totalPages);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false);
    }
  }, [query]);

  useEffect(() => {
    setResults([]);
    setCurrentPage(0);
    setTotalPages(0);
    fetchResults(0);
  }, [fetchResults]);

  useEffect(() => {
    if (!sentinelRef.current) return;
    const observer = new IntersectionObserver(
      ([entry]) => {
        if (entry.isIntersecting && !loading && currentPage + 1 < totalPages) {
          fetchResults(currentPage + 1);
        }
      },
      { threshold: 0.1 }
    );
    observer.observe(sentinelRef.current);
    return () => observer.disconnect();
  }, [loading, currentPage, totalPages, fetchResults]);

  return (
    <div className="flex-1 min-w-0 border-r border-border">
      <div className="sticky top-0 bg-surface/80 backdrop-blur-md border-b border-border px-4 py-3 z-10">
        <div className="flex items-center gap-4">
          <button
            onClick={onBack}
            className="text-text-primary hover:text-accent transition-colors duration-200 cursor-pointer"
          >
            <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M10 19l-7-7m0 0l7-7m-7 7h18" />
            </svg>
          </button>
          <div>
            <h1 className="font-bold text-xl text-text-primary">Search</h1>
            <p className="text-[13px] text-text-secondary">{query}</p>
          </div>
        </div>
      </div>

      {results.length > 0 ? (
        <div>
          {results.map((post) => (
            <Tweet
              key={post.id}
              tweet={post}
              setTweets={setResults}
              isComment={false}
            />
          ))}
        </div>
      ) : !loading ? (
        <p className="text-center text-text-secondary text-sm py-12">
          No posts found for "{query}"
        </p>
      ) : null}

      {currentPage + 1 < totalPages ? (
        <div
          ref={sentinelRef}
          className="h-16 flex justify-center items-center"
        >
          {loading && (
            <div className="w-6 h-6 border-2 border-accent border-t-transparent rounded-full animate-spin" />
          )}
        </div>
      ) : results.length > 0 ? (
        <p className="text-center text-text-secondary text-sm py-8">
          You&apos;ve reached the end
        </p>
      ) : null}
    </div>
  );
}
