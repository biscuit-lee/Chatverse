import { parseFallbackField } from "next/dist/lib/fallback";


export async function GET(request){
    return Response.json({"mesg" : "HELLO"});
}


export async function POST(request){
    const data = await request.json();
    console.log("POSTING the username and password > ")
    console.log(data)
    try{
        const res = await fetch("http://localhost:5000/api/login",{
            method:"POST",
            headers:{"Content-type":"application/json"},
            body: JSON.stringify(data)
            
        })

        console.log("result ", res);
        if (res){
            return Response.json({status:200})
        }
    }catch(error){
        console.log(error);
        return Response.json(
            {error: "FAILED"},
            {status: 500})
    }
    //console.log(data);
}