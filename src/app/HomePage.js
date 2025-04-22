"use client";
import { useEffect, useState } from "react"
import Sidebar from "./components/Sidebar";
import { FaBeer } from 'react-icons/fa';
import { CiHeart } from "react-icons/ci";
import { VscComment } from "react-icons/vsc";
import Tweet from "./components/Tweet";

export default function HomePage(){

    const [tweets,setTweet] = useState([]);    

    


    async function postTweet(event){
        event.preventDefault();

        const formData = new FormData(event.currentTarget)
        const tweetdata = formData.get("tweet");

        const res = await fetch("http://localhost:3000/api/tweet",{
            "method" : "POST",
            "headers": {"Content-Type":"application/json"},
            "body" : JSON.stringify({"content" : tweetdata , "userId":1})
        })

        if (res.ok){
            console.log(res);
            console.log("Sending tweet succeed");
        }else{
            console.log("sending tweet failed");
        }
    }
    // Fetch the tweets from backend
    useEffect(()=>{
        const fetchTweets = async ()=> {
            try{
                
                //const res = await fetch("/api/data");
                const res = await fetch("http://localhost:3000/api/data");
                const jsonres = await res.json();
                console.log(jsonres);
                setTweet(jsonres);
            }catch(error){
                console.log(error);
            }

        }

        fetchTweets();  
        
    },[])

    console.log(tweets);
    return(
        <div className="flex-1 ml-97 p-8 w-1/2">            
            <form onSubmit={postTweet} className="flex"> 
                <input autoComplete="off" placeholder="What's poppin" type="text" class="w-3/4 max-w-xl h-16 bg-transparent border-none outline-none text-left text-lg"

                ></input>
                <button className="bg-blue-500 text-white h-14 px-3 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300"> Post </button>

            </form>
            
            <div className="">
                {tweets.map((tweet,index) =>(
                    <Tweet tweet={tweet} setTweet={setTweet}/>

                ))}

            </div>
        </div>
        
    )

}