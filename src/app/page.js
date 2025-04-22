//import { useState } from "react";
import HomePage from "./HomePage";
import LoginPage from "./components/LoginPage";
import Sidebar from "./components/Sidebar";
import RightSideBar from './components/RightSideBar'
export default function Home() {
  //const res = await fetch('http://localhost:3000/api/data', { cache: 'no-store' });
  //const data = await res.json();
  
  //const [tweet,setTweet] = useState("")

  return (

    <div>
      {/* <LoginPage/> */}
      <RightSideBar/>
      <Sidebar/>
      <HomePage />
      

      
    </div>
  );
}
