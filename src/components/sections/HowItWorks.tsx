
import React from "react";
import { Link, Cog, Download } from "lucide-react";
import { motion } from "framer-motion";

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
  const containerVariants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.2
      }
    }
  };

  const itemVariants = {
    hidden: { y: 20, opacity: 0 },
    visible: { 
      y: 0, 
      opacity: 1,
      transition: { duration: 0.5 }
    }
  };

  return (
    <section id="how-it-works" className="section bg-black py-20">
      <div className="container">
        <motion.div 
          className="text-center max-w-2xl mx-auto mb-16"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5 }}
        >
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            How It <span className="text-gradient">Works</span>
          </h2>
          <p className="text-gray-300">
            Three simple steps to download and convert any video
          </p>
        </motion.div>
        
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-3 gap-12"
          variants={containerVariants}
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true }}
        >
          {steps.map((step, index) => (
            <motion.div 
              key={index} 
              className="flex flex-col items-center text-center"
              variants={itemVariants}
            >
              <div className="relative mb-6">
                <div className="w-16 h-16 bg-brand-500/20 rounded-full flex items-center justify-center">
                  <div className="w-12 h-12 bg-gray-900 rounded-full flex items-center justify-center text-brand-400 neon-glow">
                    {step.icon}
                  </div>
                </div>
                <span className="absolute -top-2 -right-2 bg-brand-500 text-black text-xs font-bold w-6 h-6 rounded-full flex items-center justify-center">
                  {step.number}
                </span>
                
                {/* Connector Line */}
                {index < steps.length - 1 && (
                  <div className="hidden md:block absolute top-8 left-full w-full h-0.5 bg-brand-500/30"></div>
                )}
              </div>
              
              <h3 className="text-xl font-medium text-white mb-2">{step.title}</h3>
              <p className="text-gray-300 text-sm">{step.description}</p>
            </motion.div>
          ))}
        </motion.div>
        
        <motion.div 
          className="mt-16 text-center"
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.5, delay: 0.6 }}
        >
          <button 
            className="bg-brand-500 hover:bg-brand-600 text-black font-medium py-3 px-8 rounded-full transition-colors neon-glow hover-scale"
            onClick={() => {
              document.querySelector('html')?.scrollTo({ top: 0, behavior: 'smooth' });
            }}
          >
            Try It Now
          </button>
        </motion.div>
      </div>
    </section>
  );
};

export default HowItWorks;
