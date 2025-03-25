
import React, { useState } from "react";
import { Search, Loader2 } from "lucide-react";
import { cn } from "@/lib/utils";

interface UrlInputProps {
  onSubmit: (url: string) => void;
  className?: string;
}

const UrlInput = ({ onSubmit, className }: UrlInputProps) => {
  const [url, setUrl] = useState("");
  const [isProcessing, setIsProcessing] = useState(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!url.trim()) return;
    
    setIsProcessing(true);
    
    // Simulate processing
    setTimeout(() => {
      onSubmit(url);
      setIsProcessing(false);
      
      // For demo purposes, show a toast or alert
      alert("This is a frontend demo. In a real application, this would process the URL.");
    }, 1500);
  };

  return (
    <form onSubmit={handleSubmit} className={cn("w-full max-w-3xl mx-auto", className)}>
      <div className="relative group">
        <div className="absolute inset-0 bg-gradient-to-r from-brand-200 to-brand-400 rounded-full blur opacity-30 group-hover:opacity-50 transition-opacity"></div>
        <div className="relative bg-white border border-brand-100 rounded-full shadow-lg flex items-center overflow-hidden">
          <div className="flex-shrink-0 pl-4">
            <Search className="h-6 w-6 text-brand-400" />
          </div>
          <input
            type="text"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Paste video URL here..."
            className="flex-grow py-4 px-4 bg-transparent focus:outline-none text-brand-900 placeholder:text-brand-300"
          />
          <button
            type="submit"
            disabled={isProcessing || !url.trim()}
            className={cn(
              "flex-shrink-0 bg-brand-500 hover:bg-brand-600 text-white font-medium py-3 px-6 m-1 rounded-full transition-colors flex items-center justify-center",
              (isProcessing || !url.trim()) && "opacity-70 cursor-not-allowed"
            )}
          >
            {isProcessing ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                <span>Processing</span>
              </>
            ) : (
              <span>Convert</span>
            )}
          </button>
        </div>
      </div>
      <p className="text-center mt-3 text-sm text-brand-500">
        Supports YouTube, Facebook, Instagram, and Twitter
      </p>
    </form>
  );
};

export default UrlInput;
