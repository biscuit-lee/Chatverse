import { FaBeer } from 'react-icons/fa';
import { CiHeart } from "react-icons/ci";
import { VscComment } from "react-icons/vsc";
import { useEffect, useState } from "react"
import { IoMdArrowDropdown } from "react-icons/io";
import { comment } from 'postcss';

export default function Tweet({tweet,setTweet}){

    const [comments,setComment] = useState([])
    
    async function addLike(tweetId){
        const res = await fetch("http://localhost:3000/api/addlike",{
            "method" : "POST",
            "headers": {"Content-Type":"application/json"},
            "body": JSON.stringify({"tweetId":tweetId, "userId":1})

        })
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
        
    }

    async function addComment(tweetId, content){
        const res = await fetch(`http://localhost:3000/api/${tweetId}/addcomment`,{
            "method" : "POST",
            "headers": {"Content-Type":"application/json"},
            "body" : JSON.stringify({"tweetId" : tweetId, "content": content , "userId":1})
        }
    )
    }

    
    async function getComment(tweetId){
        const res = await fetch(`http://localhost:3000/api/${tweetId}/addcomment`,{
            "method" : "GET"}
    )

        const data = await res.json()
        if (res.ok){
            if (Array.isArray(data) && data.length === 0) {
                setComment([{"content" : "No Comments to display!"}])
                //console.log("No comments found");
            }else{
                setComment(data)

            }
            //console.log(data)
        }else{
            setComment([{"content" : "Error fetching comments"}])
        }
    }


    return(
        
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
            <p className="select-none w-6 h-6 ml-2 mt-2 mb-2"> {tweet.likes} </p>

            <VscComment onClick={() => {addComment(tweet.id)}}  className="w-6 h-6 mt-2 cursor-pointer hover:scale-110 transition-transform duration-200"/>
            <p className="select-none w-6 h-6 ml-2 mt-2 mb-2"> {tweet.comment_amount}  </p>

            <IoMdArrowDropdown onClick={()=> {getComment(tweet.id)}} className="w-6 h-6 mt-2 cursor-pointer hover:scale-110 transition-transform duration-200"/>
           
        </div>

        {comments.map((comment,index) => (
            <p key={index}> {comment.content} </p>
        ))}

        



    </div>
    )
}