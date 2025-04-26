export async function POST(request){
    try{

        const data = await request.json();


        const res = fetch("http://localhost:5000/api/addlike",{
            "method":"POST",
            "headers": {"Content-Type":"application/json"},
            "body" : JSON.stringify(data)
        })
        
        if ((await res).ok) {
            return Response.json(
                { message: "Successfully liked the post" },
                { status: 200 }
            );
        } else {
            return Response.json(
                { message: "Unsuccessfully adding like" },
                { status: 500 } 
            );
        }
        
    }
    catch{
        return Response.json(
            { message: "Unsuccessfully adding like" },
            { status: 500 } 
        );
    }
}