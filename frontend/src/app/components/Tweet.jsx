import { CiHeart } from "react-icons/ci";
import { VscComment } from "react-icons/vsc";
import { useState } from "react";
import { IoMdArrowDropdown } from "react-icons/io";
import { BiSolidDislike } from "react-icons/bi";
import { BiSolidHeart } from "react-icons/bi";
import ProfilePic from "./ProfilePic";
import dayjs from "dayjs";
import relativeTime from "dayjs/plugin/relativeTime";
import Link from "next/link";
import { api } from "../lib/api";

dayjs.extend(relativeTime);

export default function Tweet({ tweet, setTweets, isComment }) {
  const [comments, setComments] = useState([]);
  const [commentText, setCommentText] = useState("");

  async function addLike() {
    try {
      await api.likePost(tweet.id);
      setTweets((prev) =>
        prev.map((post) =>
          post.id === tweet.id ? { ...post, likes: post.likes + 1 } : post
        )
      );
    } catch (error) {
      console.log(error);
    }
  }

  async function addDislike() {
    try {
      await api.dislikePost(tweet.id);
      setTweets((prev) =>
        prev.map((post) =>
          post.id === tweet.id
            ? { ...post, dislikes: post.dislikes + 1 }
            : post
        )
      );
    } catch (error) {
      console.log(error);
    }
  }

  async function addComment() {
    if (!commentText.trim()) return;
    try {
      const newComment = await api.addComment(tweet.id, commentText);
      setComments((prev) => [...prev, newComment]);
      setCommentText("");
      setTweets((prev) =>
        prev.map((post) =>
          post.id === tweet.id
            ? { ...post, commentCount: post.commentCount + 1 }
            : post
        )
      );
    } catch (error) {
      console.log(error);
    }
  }

  async function getComments() {
    try {
      const data = await api.getComments(tweet.id);
      if (isComment) {
        setComments([]);
      } else {
        setComments(data);
      }
    } catch (error) {
      setComments([]);
    }
  }

  return (
    <div
      key={tweet.id}
      className={`bg-surface px-4 py-3 animate-fade-in ${
        isComment ? "border-l-2 border-border ml-4" : "border-b border-border"
      }`}
    >
      <div className="flex gap-3">
        <ProfilePic imgURL={tweet.profilePictureUrl} size="small" />

        <div className="flex-1 min-w-0">
          <div className="flex items-center gap-2 flex-wrap">
            <Link
              className="font-bold text-text-primary text-[15px] hover:underline"
              href={`/users/${tweet.authorId}`}
            >
              {tweet.username}
            </Link>
            <span className="text-text-secondary text-[13px]">
              {dayjs().from(dayjs(tweet.createdAt))}
            </span>
          </div>

          <p className="text-text-primary text-[15px] leading-relaxed mt-1 whitespace-pre-wrap">
            {tweet.text}
          </p>

          <div className="flex items-center gap-6 mt-2">
            <button
              onClick={addLike}
              className="flex items-center gap-1.5 text-text-secondary hover:text-danger transition-colors duration-200 group cursor-pointer"
            >
              <BiSolidHeart className="w-5 h-5 group-hover:scale-110 transition-transform duration-200" />
              <span className="text-[13px]">{tweet.likes}</span>
            </button>

            <button
              onClick={addDislike}
              className="flex items-center gap-1.5 text-text-secondary hover:text-danger transition-colors duration-200 group cursor-pointer"
            >
              <BiSolidDislike className="w-5 h-5 group-hover:scale-110 transition-transform duration-200" />
              <span className="text-[13px]">{tweet.dislikes}</span>
            </button>

            {!isComment && (
              <>
                <button
                  onClick={getComments}
                  className="flex items-center gap-1.5 text-text-secondary hover:text-accent transition-colors duration-200 group cursor-pointer"
                >
                  <VscComment className="w-5 h-5 group-hover:scale-110 transition-transform duration-200" />
                  <span className="text-[13px]">{tweet.commentCount}</span>
                </button>
              </>
            )}
          </div>

          {!isComment && (
            <div className="flex items-center gap-2 mt-3 pb-1">
              <input
                type="text"
                value={commentText}
                onChange={(e) => setCommentText(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && addComment()}
                placeholder="Write a comment..."
                className="flex-1 bg-background border border-border rounded-full px-4 py-1.5 text-[13px] text-text-primary placeholder:text-text-secondary outline-none focus:border-accent transition-colors duration-200"
              />
              <button
                onClick={addComment}
                className="text-accent font-bold text-[13px] hover:text-accent-hover transition-colors duration-200 px-2 cursor-pointer"
              >
                Reply
              </button>
            </div>
          )}
        </div>
      </div>

      {comments.length > 0 &&
        comments.map((comment) => (
          <div key={comment.id} className="mt-2">
            <Tweet tweet={comment} setTweets={setComments} isComment={true} />
          </div>
        ))}
    </div>
  );
}
