'use client'

import ProfilePic from '@/app/components/ProfilePic';
import Tweet from '@/app/components/Tweet';
import { use } from 'react';
import { useEffect, useState, useCallback, useRef } from 'react';
import RightSidebar from '@/app/components/RightSideBar';
import Sidebar from '@/app/components/Sidebar';
import { api } from '@/app/lib/api';

const PAGE_SIZE = 10;

export default function Userpage({params}){
    const [profile, setProfile] = useState(null);
    const [tweets, setTweets] = useState([]);
    const [currentPage, setCurrentPage] = useState(0);
    const [totalPages, setTotalPages] = useState(0);
    const [loading, setLoading] = useState(false);
    const sentinelRef = useRef(null);
    const { id } = use(params);

    const fetchPosts = useCallback(async (page = 0) => {
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
    }, [id]);

    useEffect(() => {
        async function fetchProfile(){
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
    }, [id, fetchPosts])

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

    if (!profile) {
        return (
            <div>
                <RightSidebar/>
                <Sidebar/>
                <div className="flex-1 ml-97 p-8 w-1/2">
                    <p className="text-gray-500">Loading profile...</p>
                </div>
            </div>
        )
    }

    return(
        <div>
            <RightSidebar/>
            <Sidebar/>
            <div className="flex flex-col ml-97 p-8 w-1/2">
                <div className="pfp m-2">
                    <ProfilePic imgURL={profile.profilePictureUrl}/>
                </div>

                <div className="m-2 font-bold ">
                    <p className='text-2xl'>{profile.username}</p>
                </div>

                <div className="div m-2">
                    {profile.bio}
                </div>

                <div className="flex flex-row gap-4">
                    <p className="font-bold text-1">Followers</p>
                    <p className="font-bold text-1 ml-5">Following</p>
                </div>

                <div className="flex flex-row gap-4 m-2">
                    <p className="text-1">{profile.followers}</p>
                    <p className="ml-21">{profile.following}</p>
                </div>

                <div className="div m-2">
                    <p className='font-bold text-l'>Posts</p>
                </div>
                {tweets?.map((tweet) => (
                    <Tweet key={tweet.id} tweet={tweet} setTweets={setTweets}/>
                ))}

                {currentPage + 1 < totalPages ? (
                    <div ref={sentinelRef} className="h-10 flex justify-center items-center my-6">
                        {loading && <p className="text-gray-500">Loading...</p>}
                    </div>
                ) : tweets.length > 0 ? (
                    <p className="text-center text-gray-400 text-sm my-6">End of posts</p>
                ) : null}
            </div>
        </div>
    )
}
