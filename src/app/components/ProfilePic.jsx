import Image from 'next/image';


export default function ProfilePic({imgURL, size}){

    const finalURL = imgURL ?? 'https://rugvhgitcuakfjdeikgt.supabase.co/storage/v1/object/public/profilepicture/Default_pfp.png'

    const sizeMap = {
        "small": 25,
        "medium" : 70,
        "large" : 90
    }
    
    const dimension = sizeMap[size] ??sizeMap["medium"]
    return(
        <div className="div">
            <Image
                src={finalURL}
                width={dimension}
                height={dimension}
                alt='Profile picture'
            />
        </div>
    )
}