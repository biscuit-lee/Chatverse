"use client";
import { useEffect, useState } from "react"
import Sidebar from "./components/Sidebar";
import { FaBeer } from 'react-icons/fa';
import { CiHeart } from "react-icons/ci";
import { VscComment } from "react-icons/vsc";


export default function HomePage(){

    const [tweets,setTweet] = useState([]);
    const [like,setLike] = useState([]);
    const [commentCount,setCommentCount] = useState([]);

    async function addLike(tweetId){
        //const res = await fetch("http://localhost:5000/api/addLike")
        console.log("CLIKED CALLED" + "id " + tweetId);
        /* setTweet((prev) => prev.map((post) =>
            post.id === tweetId ? {...post,likes: post.likes + 1} : post
        )) */

        setTweet((prev) => {
            return prev.map(post => {
                if (post.id === tweetId){
                    return{...post,likes: post.likes + 1};   // This creates a new obj with everything the same in post except the likes column that we added 1 to
                }
                return post
            })
        })
        
        console.log('added likes to tweet ' + tweets)
    }
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
                
                console.log("FETCHIN");
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
        <div className="flex-1 ml-64 p-8">            
            <form onSubmit={postTweet} className="flex"> 
                <input placeholder="What's poppin" type="text" name="tweet" class="w-3/4 max-w-xl h-16 bg-transparent border-none outline-none text-left text-lg"

                ></input>
                <button className="bg-blue-500 text-white py-1 px-3 rounded-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300"> Post </button>

            </form>
            
            <div className="">
                {tweets.map((tweet,index) =>(
                
                <div key={tweet.id} className="border-r-2 border-l-2 border-t-2">
                    <div className="flex space-x-4 mt-5 px-2">
                        <h1 className="text-black "> {tweet.author_id} </h1>
                        <h3> {tweet.timestamp}</h3>
                    </div>
                    <div>
                        <h2 className="m-2 px-2"> {tweet.text} </h2>
                    </div>
                    <div className="flex px-2">
                        <CiHeart onClick={() => {addLike(tweet.id)}} className="w-6 h-6 mt-2 cursor-pointer text-red-500 hover:scale-110 transition-transform duration-200"/>
                        <p className="w-6 h-6 ml-2 mt-2 mb-2"> {tweet.likes} </p>

                        <VscComment className="w-6 h-6 mt-2 cursor-pointer hover:scale-110 transition-transform duration-200"/>
                        <p className="w-6 h-6 ml-2 mt-2 mb-2"> {tweet.comment_amount} </p>

                    </div>


                </div>

                ))}

            </div>
        </div>
        
    )

}