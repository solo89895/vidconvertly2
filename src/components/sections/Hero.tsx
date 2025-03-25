
import React, { useState } from "react";
import UrlInput from "@/components/ui/UrlInput";
import PlatformSelector from "@/components/ui/PlatformSelector";
import { Youtube, Facebook, Instagram, Twitter } from "lucide-react";

const platforms = [
  {
    id: "youtube",
    name: "YouTube",
    icon: <Youtube className="w-4 h-4" />,
  },
  {
    id: "facebook",
    name: "Facebook",
    icon: <Facebook className="w-4 h-4" />,
  },
  {
    id: "instagram",
    name: "Instagram",
    icon: <Instagram className="w-4 h-4" />,
  },
  {
    id: "twitter",
    name: "Twitter",
    icon: <Twitter className="w-4 h-4" />,
  },
  {
    id: "tiktok",
    name: "TikTok",
    icon: (
      <svg
        className="w-4 h-4"
        width="16"
        height="16"
        viewBox="0 0 16 16"
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
      >
        <path
          d="M8 0C12.4183 0 16 3.58172 16 8C16 12.4183 12.4183 16 8 16C3.58172 16 0 12.4183 0 8C0 3.58172 3.58172 0 8 0ZM11.75 4.25H10.25C10.1119 4.25 10 4.36193 10 4.5V9.5C10 9.63807 9.88807 9.75 9.75 9.75H9.25C9.11193 9.75 9 9.63807 9 9.5V6.5C9 6.36193 8.88807 6.25 8.75 6.25H8.25C8.11193 6.25 8 6.36193 8 6.5V9.5C8 9.63807 7.88807 9.75 7.75 9.75H7.25C7.11193 9.75 7 9.63807 7 9.5V7.5C7 7.36193 6.88807 7.25 6.75 7.25H6.25C6.11193 7.25 6 7.36193 6 7.5V9.5C6 9.63807 5.88807 9.75 5.75 9.75H5.25C5.11193 9.75 5 9.63807 5 9.5V5.5C5 5.36193 5.11193 5.25 5.25 5.25H11.5C11.6381 5.25 11.75 5.13807 11.75 5V4.5C11.75 4.36193 11.6381 4.25 11.5 4.25H11.75Z"
          fill="currentColor"
        />
      </svg>
    ),
  },
];

const Hero = () => {
  const [selectedPlatform, setSelectedPlatform] = useState("youtube");

  const handleUrlSubmit = (url: string) => {
    console.log("Processing URL:", url, "for platform:", selectedPlatform);
  };

  return (
    <section className="relative pt-24 pb-20 md:pt-32 md:pb-28 overflow-hidden bg-gradient-to-b from-gray-900 to-black">
      {/* Background Pattern */}
      <div className="absolute inset-0 opacity-10">
        <div className="absolute inset-0 bg-[url('data:image/svg+xml;base64,PHN2ZyB3aWR0aD0iNjAiIGhlaWdodD0iNjAiIHZpZXdCb3g9IjAgMCA2MCA2MCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj48ZyBmaWxsPSJub25lIiBmaWxsLXJ1bGU9ImV2ZW5vZGQiPjxnIGZpbGw9IiMyMkM1NUUiIGZpbGwtb3BhY2l0eT0iMC40Ij48cGF0aCBkPSJNMzYgMzBoLTZWMGg2djMwem0tNiAwaC02VjBoNnYzMHptLTYgMGgtNlYwaDZ2MzB6bS02IDBoLTZWMGg2djMwem0tNiAwSDB2LTZoNnY2em0wLTZIMHYtNmg2djZ6bTAtNkgwdi02aDZ2NnptMC02SDB2LTZoNnY2em0wLTZIMFYwaDB2NnoiLz48L2c+PC9nPjwvc3ZnPg==')] opacity-5"></div>
      </div>
      
      {/* Content */}
      <div className="container relative z-10">
        <div className="max-w-3xl mx-auto text-center mb-12 animate-fade-in">
          <div className="inline-block bg-brand-600 text-black px-3 py-1 rounded-full text-sm font-medium mb-6 animate-pulse">
            Fast, Free & Simple
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-gray-100 mb-6 tracking-tight">
            Convert Videos with <span className="text-gradient font-bold">Elegance</span>
          </h1>
          <p className="text-xl text-gray-300 mb-8 max-w-2xl mx-auto">
            Download and convert videos from YouTube, Facebook, Instagram, Twitter, and TikTok in seconds. No signup required.
          </p>
          
          <PlatformSelector
            platforms={platforms}
            selectedPlatform={selectedPlatform}
            onSelect={setSelectedPlatform}
            className="mb-8"
          />
          
          <UrlInput onSubmit={handleUrlSubmit} />
        </div>
        
        {/* Floating Elements Animation (Decorative) */}
        <div className="hidden md:block">
          <div className="absolute top-40 -right-16 w-32 h-32 glassmorphism rounded-xl rotate-12 animate-float opacity-30"></div>
          <div className="absolute bottom-20 -left-8 w-24 h-24 glassmorphism rounded-xl -rotate-12 animate-float opacity-30 animation-delay-1000"></div>
          <div className="absolute top-20 left-10 w-20 h-20 bg-brand-500/10 rounded-xl rotate-45 animate-bounce opacity-40"></div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
