'use client'

import ProfilePic from '@/app/components/ProfilePic';
import Tweet from '@/app/components/Tweet';
import { use } from 'react';  
import { useEffect, useState } from 'react';
import { supabase } from '@/app/lib/supabase';
import RightSidebar from '@/app/components/RightSideBar';
import Sidebar from '@/app/components/Sidebar';
export default function Userpage({params}){
    const [profile,setProfile] = useState([]);
    const [tweets,setTweet] = useState([]);

    const { id } = use(params);
    
    const {data,error} = supabase.storage.from('profilepicture').getPublicUrl('unamused.png')
    console.log("IMAGE: ",data.publicUrl)


    
    useEffect( () =>{
        async function fetchUser(){
            const res = await fetch(`http://localhost:3000/api/users/${id}`)
            console.log("fetching user in useefect");
            
            if (!res.ok){
                console.log("ERROR FETCHING DATA")
                setProfile([]);
            }
            const data = await res.json();
            setProfile(data[0]);
            setTweet(data[0]?.tweets);

            console.log("DATA ; ",data)
            console.log("PROFILE :",profile)
            console.log("Tweets: " , tweets)

        }
        fetchUser();
    },[id])


    return(
        <div>
            <RightSidebar/>
            <Sidebar/>
            <div className="flex flex-col ml-97 p-8 w-1/2">
                <div className="pfp m-2">
                    <ProfilePic imgURL={profile.profile_picture}/>
                </div>

                <div className="m-2 font-bold ">
                    <p className='text-2xl'> {profile.username} </p>
                </div>

                <div className="div m-2">
                    {profile.bio}
                </div>

                <div className="div m-2">
                    <p className='font-bold text-l'>Posts</p>
                </div>
                {tweets?.map((tweet,index)=>(
                    <Tweet tweet={tweet} setTweet={setTweet}/>
                ))}
                
            </div>
            
        </div>
    )

}
