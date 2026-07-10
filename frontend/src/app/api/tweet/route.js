export async function POST(request){

    const data = await request.json();
    console.log(data)

    try{
        const res = await fetch("http://localhost:5000/api/tweets", {
            "method" : "POST",
            "headers" : {"Content-Type" : "application/json"},
            "body" : JSON.stringify(data)
        })


        if (res.ok){
            console.log("middleware: send tweet succede")
            return Response.json({ message: "Backend failure" }, { status: 200 });

        }else{
            
            console.log("middleware: send tweet failed")
            const errorText = await res.text();
            console.error("Request failed:", res.status, errorText);

            return Response.json({ message: "Backend failure" }, { status: 500 });


        }
        

    }
    catch
    {
        return Response.json({ message: "Backend failure" }, { status: 500 });

}
}