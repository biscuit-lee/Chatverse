
'use client'
export default function LoginPage(){


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
    }

    return(
        <div>
            <form  onSubmit={handleSumbit}> 
                <input type="text" name="username"></input>
                <input type="password" name="password"></input>
                <button>SUBMIT</button>
            </form>

        </div>
    )
}