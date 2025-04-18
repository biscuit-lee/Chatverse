'use client'
import React from 'react';
import Link from 'next/link';

export default function Sidebar() {
    return (
        <div className="fixed top-0 h-screen w-32 m-0 flex flex-col bg-gray-600">
            <nav>
                <ul>
                    <li>
                       
                        <a>Home</a>
                       
                    </li>
                    <li>
                       
                        <a>About</a>
                       
                    </li>
                    <li>
                        
                        <a>Contact</a>
                        
                    </li>
                </ul>
            </nav>
            <style jsx>{`
                .sidebar {
                    width: 250px;
                    background-color: #f4f4f4;
                    padding: 20px;
                    height: 100vh;
                }
                ul {
                    list-style: none;
                    padding: 0;
                }
                li {
                    margin: 10px 0;
                }
                a {
                    text-decoration: none;
                    color: #333;
                }
                a:hover {
                    color: #0070f3;
                }
            `}</style>
        </div>
    );
};
