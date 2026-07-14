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
          post.id === tweet.id ? { ...post, dislikes: post.dislikes + 1 } : post
        )
      );
    } catch (error) {
      console.log(error);
    }
  }

  async function addComment() {
    if (!commentText.trim()) return;
    try {
      await api.addComment(tweet.id, commentText);
      setCommentText("");
      getComments();
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
    <div key={tweet.id} className="border-r-2 border-l-2 border-t-2">
      <div className="flex space-x-4 mt-5 px-2">
        <ProfilePic imgURL={tweet.profilePictureUrl} size="small" />
        <h1 className="text-black">
          <Link className="hover:underline" href={`/users/${tweet.authorId}`}>
            <b>{tweet.username}</b>
          </Link>
        </h1>
        <h3 className="text-gray-500">
          {dayjs().from(dayjs(tweet.createdAt))}
        </h3>
      </div>
      <div>
        <h2 className="m-2 px-2">{tweet.text}</h2>
      </div>
      <div className="flex px-2">
        <CiHeart
          onClick={addLike}
          className="w-6 h-6 mt-2 cursor-pointer text-red-500 hover:scale-110 transition-transform duration-200"
        />
        <p className="select-none w-6 h-6 ml-2 mt-2 mb-2">{tweet.likes}</p>

        <BiSolidDislike
          onClick={addDislike}
          className="w-6 h-6 mt-2 cursor-pointer text-red-500 hover:scale-110 transition-transform duration-200"
        />
        <p className="select-none w-6 h-6 ml-2 mt-2 mb-2">{tweet.dislikes}</p>

        {!isComment && (
          <>
            <VscComment
              className="w-6 h-6 mt-2 cursor-pointer hover:scale-110 transition-transform duration-200"
            />
            <p className="select-none w-6 h-6 ml-2 mt-2 mb-2">
              {tweet.commentCount}
            </p>
            <IoMdArrowDropdown
              onClick={getComments}
              className="w-6 h-6 mt-2 cursor-pointer hover:scale-110 transition-transform duration-200"
            />
          </>
        )}
      </div>

      {!isComment && (
        <div className="flex px-4 py-2">
          <input
            type="text"
            value={commentText}
            onChange={(e) => setCommentText(e.target.value)}
            placeholder="Write a comment..."
            className="flex-1 border rounded-lg px-3 py-1 text-sm outline-none focus:ring-2 focus:ring-blue-300"
          />
          <button
            onClick={addComment}
            className="ml-2 bg-blue-500 text-white text-sm px-3 py-1 rounded-lg hover:bg-blue-600 transition-colors"
          >
            Reply
          </button>
        </div>
      )}

      {comments.length > 0 &&
        comments.map((comment) => (
          <div key={comment.id} className="ml-10">
            <h1 className="m-2">Replies</h1>
            <Tweet tweet={comment} setTweets={setComments} isComment={true} />
          </div>
        ))}
    </div>
  );
}
