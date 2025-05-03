import Image from 'next/image';


export default function ProfilePic({imgURL}){

    const finalURL = imgURL ?? 'https://rugvhgitcuakfjdeikgt.supabase.co/storage/v1/object/public/profilepicture/Default_pfp.png'



    return(
        <div className="div">
            <Image
                src={finalURL}
                width={70}
                height={70}
                alt='Profile picture'
            />
        </div>
    )
}