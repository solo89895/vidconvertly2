
import React from "react";
import { Download } from "lucide-react";

const Footer = () => {
  return (
    <footer className="bg-brand-50 border-t border-brand-100">
      <div className="container py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="md:col-span-1">
            <a href="/" className="flex items-center gap-2">
              <span className="text-brand-900 font-semibold text-xl flex items-center">
                <Download className="w-5 h-5 text-brand-500 mr-1" />
                vidconvertly
              </span>
            </a>
            <p className="mt-4 text-sm text-brand-700">
              Convert and download videos from various platforms with ease. Fast, free, and simple.
            </p>
          </div>
          
          <div className="md:col-span-3 grid grid-cols-2 md:grid-cols-3 gap-8">
            <div>
              <h3 className="text-brand-900 font-medium mb-4">Platform</h3>
              <ul className="space-y-2">
                <li>
                  <a href="#features" className="text-sm text-brand-700 hover:text-brand-900 transition-colors">
                    Features
                  </a>
                </li>
                <li>
                  <a href="#how-it-works" className="text-sm text-brand-700 hover:text-brand-900 transition-colors">
                    How It Works
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-brand-700 hover:text-brand-900 transition-colors">
                    FAQs
                  </a>
                </li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-brand-900 font-medium mb-4">Legal</h3>
              <ul className="space-y-2">
                <li>
                  <a href="#disclaimer" className="text-sm text-brand-700 hover:text-brand-900 transition-colors">
                    Disclaimer
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-brand-700 hover:text-brand-900 transition-colors">
                    Terms of Service
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-brand-700 hover:text-brand-900 transition-colors">
                    Privacy Policy
                  </a>
                </li>
              </ul>
            </div>
            
            <div>
              <h3 className="text-brand-900 font-medium mb-4">Supported</h3>
              <ul className="space-y-2">
                <li>
                  <a href="#" className="text-sm text-brand-700 hover:text-brand-900 transition-colors">
                    YouTube
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-brand-700 hover:text-brand-900 transition-colors">
                    Facebook
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-brand-700 hover:text-brand-900 transition-colors">
                    Instagram
                  </a>
                </li>
                <li>
                  <a href="#" className="text-sm text-brand-700 hover:text-brand-900 transition-colors">
                    Twitter
                  </a>
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className="mt-12 pt-8 border-t border-brand-100 flex flex-col md:flex-row justify-between items-center">
          <p className="text-sm text-brand-600">
            © {new Date().getFullYear()} vidconvertly. All rights reserved.
          </p>
          <div className="mt-4 md:mt-0">
            <p className="text-xs text-brand-600">
              vidconvertly does not host any copyrighted content and respects intellectual property rights.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
