"use client";
import { useEffect, useState } from "react"

export default function HomePage(){

    const [tweets,setTweet] = useState([]);


    console.log("IN HOMEPAGE");

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


    return(
        <div>
            <h1> Tweets </h1>

            <div>
                {tweets.map((tweet,index) =>(
                    
                    <div key={tweet.id}>
                        <h1> {tweet.author_id} </h1>
                        <h2> {tweet.text} </h2>
                        <h3> {tweet.timestamp}</h3>

                    </div>

                ))}

            </div>
        </div>
        
    )

}