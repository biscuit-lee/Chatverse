export async function POST(request){

    const data = await request.json()

    async function addComment(tweetId, content){
        const res = await fetch("http://localhost:3000/api/handleComment",{
            "method" : "POST",
            "headers": {"Content-Type":"application/json"},
            "body" : JSON.stringify(data)
        }
        )
        if (res.ok){
            return Response.json(
                {
                    "message" : "Successfully added comment"
                },
                {
                    status:200
                }
            )
        }

        else{
            return Response.json(
                {"Message" : "Failed to submit comment"},
                {status: 500}
            )
        }

    }

}


export async function GET(request, {params}){

    const tweetId = await params.tweetId;

    const res = await fetch(`http://localhost:5000/api/${tweetId}/handleComment`);

    const data = await res.json() // this turns the promise into java object
    console.log("MIDLLE WARE FETCH CMD")
    if (res.ok){
        console.log("MESSAGE FROM BACKEND AFTER FETCH CMD " , data)
        return new Response(JSON.stringify(data), {status:200, "headers":{"Content-Type" : "application/json"}})
    }else{
        console.log("MESSAGE FROM BACKEND AFTER FETCH CMD ", data)
        return new Response(JSON.stringify({"Message": "Cannot Fetch"}), {status:500, "headers":{"Content-Type" : "application/json"}})
    }
    
}