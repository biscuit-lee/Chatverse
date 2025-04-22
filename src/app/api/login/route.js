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
        if (res.ok){
            console.log("RETURNED ok")

            return Response.json({status:200})
        }else{
            console.log("not ok")
            return Response.json(
                {"message": "unauthorised"},
                {status:401})
        }

    }catch(error){
        console.log(error);
        return Response.json(
            {error: "FAILED"},
            {status: 500})
    }

}