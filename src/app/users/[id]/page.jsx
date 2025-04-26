'use client'

import Tweet from '@/app/components/Tweet';
import { use } from 'react';  
import { useEffect, useState } from 'react';


export default function Userpage({params}){
    const [profile,setProfile] = useState([]);
    const [tweets,setTweet] = useState([]);

    console.log("Fetching user with id: ")
    
    const { id } = use(params);

    console.log(id)
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
            <div className="flex flex-col">
                <div className="">
                    {profile.username}
                </div>

                <div className="div">
                    {profile.bio}
                </div>

                {tweets?.map((tweet,index)=>(
                    <Tweet tweet={tweet} setTweet={setTweet}/>
                ))}
                
            </div>
            
        </div>
    )

}
