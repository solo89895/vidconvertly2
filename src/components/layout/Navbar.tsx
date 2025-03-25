
import React, { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { Download, Menu, X } from "lucide-react";

const Navbar = () => {
  const [isScrolled, setIsScrolled] = useState(false);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);

  useEffect(() => {
    const handleScroll = () => {
      setIsScrolled(window.scrollY > 10);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  return (
    <header
      className={cn(
        "fixed top-0 left-0 right-0 z-50 transition-all duration-300 ease-in-out py-4",
        isScrolled
          ? "bg-white/90 backdrop-blur-lg shadow-sm"
          : "bg-transparent"
      )}
    >
      <div className="container flex items-center justify-between">
        <a href="/" className="flex items-center gap-2">
          <span className="text-brand-900 font-semibold text-xl flex items-center">
            <Download className="w-5 h-5 text-brand-500 mr-1" />
            vidconvertly
          </span>
        </a>

        {/* Desktop Navigation */}
        <nav className="hidden md:flex items-center gap-8">
          <a
            href="#features"
            className="text-brand-900/80 hover:text-brand-900 text-sm font-medium transition-colors"
          >
            Features
          </a>
          <a
            href="#how-it-works"
            className="text-brand-900/80 hover:text-brand-900 text-sm font-medium transition-colors"
          >
            How It Works
          </a>
          <a
            href="#disclaimer"
            className="text-brand-900/80 hover:text-brand-900 text-sm font-medium transition-colors"
          >
            Legal
          </a>
        </nav>

        {/* Mobile Menu Button */}
        <button
          onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
          className="md:hidden text-brand-900 hover:text-brand-700 transition-colors"
        >
          {isMobileMenuOpen ? (
            <X className="w-6 h-6" />
          ) : (
            <Menu className="w-6 h-6" />
          )}
        </button>
      </div>

      {/* Mobile Menu */}
      <div
        className={cn(
          "fixed inset-0 top-16 bg-white z-40 transform transition-transform duration-300 ease-in-out md:hidden",
          isMobileMenuOpen ? "translate-x-0" : "translate-x-full"
        )}
      >
        <nav className="container py-8 flex flex-col gap-6">
          <a
            href="#features"
            onClick={() => setIsMobileMenuOpen(false)}
            className="text-brand-900 text-lg font-medium py-2 border-b border-brand-100"
          >
            Features
          </a>
          <a
            href="#how-it-works"
            onClick={() => setIsMobileMenuOpen(false)}
            className="text-brand-900 text-lg font-medium py-2 border-b border-brand-100"
          >
            How It Works
          </a>
          <a
            href="#disclaimer"
            onClick={() => setIsMobileMenuOpen(false)}
            className="text-brand-900 text-lg font-medium py-2 border-b border-brand-100"
          >
            Legal
          </a>
        </nav>
      </div>
    </header>
  );
};

export default Navbar;
