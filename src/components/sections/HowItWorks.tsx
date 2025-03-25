
import React from "react";
import { Link, Cog, Download } from "lucide-react";

const steps = [
  {
    number: "01",
    icon: <Link className="w-6 h-6" />,
    title: "Paste URL",
    description: "Copy and paste the URL of the video you want to download from any supported platform."
  },
  {
    number: "02",
    icon: <Cog className="w-6 h-6" />,
    title: "Select Format",
    description: "Choose your preferred format and quality options for the downloaded video."
  },
  {
    number: "03",
    icon: <Download className="w-6 h-6" />,
    title: "Download",
    description: "Click the download button and save the converted file to your device."
  }
];

const HowItWorks = () => {
  return (
    <section id="how-it-works" className="section bg-white">
      <div className="container">
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl md:text-4xl font-bold text-brand-900 mb-4">
            How It Works
          </h2>
          <p className="text-brand-700">
            Three simple steps to download and convert any video
          </p>
        </div>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-12">
          {steps.map((step, index) => (
            <div key={index} className="flex flex-col items-center text-center">
              <div className="relative mb-6">
                <div className="w-16 h-16 bg-brand-100 rounded-full flex items-center justify-center">
                  <div className="w-12 h-12 bg-white rounded-full flex items-center justify-center text-brand-500">
                    {step.icon}
                  </div>
                </div>
                <span className="absolute -top-2 -right-2 bg-brand-500 text-white text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center">
                  {step.number}
                </span>
                
                {/* Connector Line */}
                {index < steps.length - 1 && (
                  <div className="hidden md:block absolute top-8 left-full w-full h-0.5 bg-brand-100"></div>
                )}
              </div>
              
              <h3 className="text-xl font-medium text-brand-900 mb-2">{step.title}</h3>
              <p className="text-brand-600 text-sm">{step.description}</p>
            </div>
          ))}
        </div>
        
        <div className="mt-16 text-center">
          <button 
            className="bg-brand-500 hover:bg-brand-600 text-white font-medium py-3 px-8 rounded-full transition-colors"
            onClick={() => {
              document.querySelector('html')?.scrollTo({ top: 0, behavior: 'smooth' });
            }}
          >
            Try It Now
          </button>
        </div>
      </div>
    </section>
  );
};

export default HowItWorks;
