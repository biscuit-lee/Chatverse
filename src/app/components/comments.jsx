export default function commentSection({comment}){

    return (
        <div className="flex space-x-4 mt-5 px-2">
            <div className="">
                <p>{comment.username}</p>
                <p>{comment.id}</p>
            </div>

        </div>
    )
}