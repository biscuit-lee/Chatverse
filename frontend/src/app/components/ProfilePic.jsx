import Image from "next/image";

export default function ProfilePic({ imgURL, size }) {
  const finalURL =
    imgURL ??
    "https://rugvhgitcuakfjdeikgt.supabase.co/storage/v1/object/public/profilepicture/Default_pfp.png";

  const sizeMap = {
    small: 32,
    medium: 40,
    large: 96,
  };

  const dimension = sizeMap[size] ?? sizeMap["medium"];

  return (
    <div
      className="rounded-full overflow-hidden border border-border shrink-0"
      style={{ width: dimension, height: dimension }}
    >
      <Image
        src={finalURL}
        width={dimension}
        height={dimension}
        alt="Profile picture"
        className="object-cover w-full h-full"
      />
    </div>
  );
}
