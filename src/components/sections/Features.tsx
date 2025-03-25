
import React from "react";
import FeatureCard from "@/components/ui/FeatureCard";
import { Download, Sliders, Clock, Zap, Shield, Music } from "lucide-react";

const features = [
  {
    icon: <Download className="w-6 h-6" />,
    title: "Multiple Platforms",
    description: "Download videos from YouTube, Facebook, Instagram, and Twitter with a single tool."
  },
  {
    icon: <Sliders className="w-6 h-6" />,
    title: "Format Selection",
    description: "Choose from various formats including MP4, MP3, WebM, and more to suit your needs."
  },
  {
    icon: <Clock className="w-6 h-6" />,
    title: "Instant Processing",
    description: "Get your converted videos instantly without waiting in long queues or delays."
  },
  {
    icon: <Zap className="w-6 h-6" />,
    title: "High Quality",
    description: "Download videos in high definition quality up to 4K resolution when available."
  },
  {
    icon: <Shield className="w-6 h-6" />,
    title: "Safe & Secure",
    description: "No registration required. We don't store your files or personal information."
  },
  {
    icon: <Music className="w-6 h-6" />,
    title: "Audio Extraction",
    description: "Extract audio from videos and download as MP3 files with a single click."
  }
];

const Features = () => {
  return (
    <section id="features" className="section bg-brand-50">
      <div className="container">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-brand-900 mb-4">
            Designed for Simplicity
          </h2>
          <p className="text-brand-700">
            Enjoy a seamless video conversion experience with our powerful, yet elegantly simple features
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {features.map((feature, index) => (
            <FeatureCard
              key={index}
              icon={feature.icon}
              title={feature.title}
              description={feature.description}
              className="animate-fade-in"
              style={{ animationDelay: `${index * 100}ms` }}
            />
          ))}
        </div>
      </div>
    </section>
  );
};

export default Features;
