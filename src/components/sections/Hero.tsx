
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
];

const Hero = () => {
  const [selectedPlatform, setSelectedPlatform] = useState("youtube");

  const handleUrlSubmit = (url: string) => {
    console.log("Processing URL:", url, "for platform:", selectedPlatform);
  };

  return (
    <section className="relative pt-24 pb-20 md:pt-32 md:pb-28 overflow-hidden">
      {/* Gradient Background */}
      <div className="absolute inset-0 bg-hero-pattern opacity-60"></div>
      
      {/* Content */}
      <div className="container relative z-10">
        <div className="max-w-3xl mx-auto text-center mb-12 animate-fade-in">
          <div className="inline-block bg-brand-100 text-brand-600 px-3 py-1 rounded-full text-sm font-medium mb-6">
            Fast, Free & Simple
          </div>
          <h1 className="text-5xl md:text-6xl font-bold text-brand-900 mb-6 tracking-tight">
            Convert Videos with Elegance
          </h1>
          <p className="text-xl text-brand-700 mb-8 max-w-2xl mx-auto">
            Download and convert videos from YouTube, Facebook, Instagram, and Twitter in seconds. No signup required.
          </p>
          
          <PlatformSelector
            platforms={platforms}
            selectedPlatform={selectedPlatform}
            onSelect={setSelectedPlatform}
            className="mb-8"
          />
          
          <UrlInput onSubmit={handleUrlSubmit} />
        </div>
        
        {/* Floating Cards Animation (Decorative) */}
        <div className="hidden md:block">
          <div className="absolute top-40 -right-16 w-32 h-32 bg-white/80 rounded-xl shadow-xl backdrop-blur-sm rotate-12 animate-float opacity-70"></div>
          <div className="absolute bottom-20 -left-8 w-24 h-24 bg-white/80 rounded-xl shadow-lg backdrop-blur-sm -rotate-12 animate-float opacity-70 animation-delay-1000"></div>
        </div>
      </div>
    </section>
  );
};

export default Hero;
