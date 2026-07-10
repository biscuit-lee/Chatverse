export  async function GET(request,{params}){
    console.log("the user / id route called");
    const id = await params.id;

    const res = await fetch(`http://localhost:5000/api/users/${id}`);

    const data = await res.json()
    
    console.log("RECEIVED USER PROFILE ",data);
    if (res.ok){
        console.log("middle man received OK", data);
        return Response.json(data, {status:200})
    }else{
        console.log("middle man got an error");
        return Response.json({"Message":"Failed fetching user profile"}, {status:200})

    }

}