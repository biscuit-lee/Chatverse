import { FaBeer } from 'react-icons/fa';
import { CiHeart } from "react-icons/ci";
import { VscComment } from "react-icons/vsc";
import { useEffect, useState } from "react"
import { IoMdArrowDropdown } from "react-icons/io";
import { comment } from 'postcss';
import Link from 'next/link';
import { BiSolidDislike } from "react-icons/bi";


export default function Tweet({tweet,setTweet,isComment}){

    const [comments,setComment] = useState([])
    
    async function requestProfile(user_id){
        const res = await fetch(`http://localhost:3000/api/users/${user_id}`)

        if (res.ok){
            const data = await res.json();
        }
    }

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
    

    async function add_disLike(tweetId){
        const res = await fetch("http://localhost:3000/api/dislike",{
            "method" : "POST",
            "headers": {"Content-Type":"application/json"},
            "body": JSON.stringify({"tweetId":tweetId, "userId":1})

        })


        setTweet((prev) => {
            return prev.map(post => {
                if (post.id === tweetId){
                    return{...post,dislike: post.dislike + 1};   // This creates a new obj with everything the same in post except the likes column that we added 1 to
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
            // If theres no comments to display
            if (Array.isArray(data) && data.length === 0) {
                
                setComment([])
                //console.log("No comments found");
            }else{
                if ( isComment === true){
                    
                    setComment([])
                }else{
                    setComment(data)
                }

            }
            //console.log(data)
        }else{
            setComment([])
        }
    }


    return(
        
        <div key={tweet.id} className="border-r-2 border-l-2 border-t-2">
        <div className="flex space-x-4 mt-5 px-2">
            
            <h1 className="text-black "> 
                
           {/*  <div onClick={() => {requestProfile(tweet.user_id)}} className='hover:underline cursor-pointer'>
                <b>{tweet.username}</b> 
            </div> */}

            <Link className="hover:underline" href={`/users/${tweet.author_id}`}>
                <b>{tweet.username}</b>
            </Link>

            </h1>
            
            <h3 className='text-gray-500'> {tweet.timestamp}</h3>
        </div>
        <div>
            <h2 className="m-2 px-2"> {tweet.text} </h2>
        </div>
        <div className="flex px-2">
            <CiHeart onClick={() => {addLike(tweet.id)}} className="w-6 h-6 mt-2 cursor-pointer text-red-500 hover:scale-110 transition-transform duration-200"/>
            <p className="select-none w-6 h-6 ml-2 mt-2 mb-2"> {tweet.likes} </p>

            <BiSolidDislike onClick={() => {add_disLike(tweet.id)}} className="w-6 h-6 mt-2 cursor-pointer text-red-500 hover:scale-110 transition-transform duration-200"/>
            <p className="select-none w-6 h-6 ml-2 mt-2 mb-2"> {tweet.dislike} </p>

            {!isComment && (
            <>
                <VscComment 
                onClick={() => addComment(tweet.id)}  
                className="w-6 h-6 mt-2 cursor-pointer hover:scale-110 transition-transform duration-200"
                />
                <p className="select-none w-6 h-6 ml-2 mt-2 mb-2">
                {tweet.comment_amount}
                </p>
                <IoMdArrowDropdown 
                onClick={() => getComment(tweet.id)} 
                className="w-6 h-6 mt-2 cursor-pointer hover:scale-110 transition-transform duration-200" 
                />
            </>
            )}

           
        </div>
        
        <div className="div">
            
        </div>

        {comments.length > 0 && comments.map((comment,index) => (
            
            <div className="ml-10">
                
                <h1 className='m-2'>Replies</h1>
                
                <Tweet tweet={comment} setTweet={setComment} isComment={true}/>
            </div>
            
        
        ))}

        



    </div>
    )
}