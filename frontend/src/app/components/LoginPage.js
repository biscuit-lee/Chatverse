'use client'
import { useState } from "react";

export default function LoginPage(){

    const [loginError,setLoginerror] = useState("");
    async function handleSumbit(event){
        event.preventDefault();

        const formData = new FormData(event.currentTarget);
        const username = formData.get("username");
        const password = formData.get("password");


        // Request to router
        const res = await fetch("http://localhost:3000/api/login", {
            method : "POST",
            headers : {"Content-Type":"application/json"},
            body: JSON.stringify({
                username: username,
                password: password
            })

        })

        // If the credentials are wrong
        if(res.status == 401){
            setLoginerror("Wrong password/user")
        }
        else if(res.ok){
            setLoginerror("YOU'rE IN")
            // Redirect somewhere else
        }
    }

    return(
        <div>
            <form  onSubmit={handleSumbit}> 
                <input type="text" name="username"></input>
                <input type="password" name="password"></input>
                <p> { loginError }</p>
                <button>SUBMIT</button>
            </form>

        </div>
    )
}