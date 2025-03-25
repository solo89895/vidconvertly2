
import React from "react";
import { cn } from "@/lib/utils";

interface Platform {
  id: string;
  name: string;
  icon: React.ReactNode;
}

interface PlatformSelectorProps {
  platforms: Platform[];
  selectedPlatform: string;
  onSelect: (platformId: string) => void;
  className?: string;
}

const PlatformSelector = ({
  platforms,
  selectedPlatform,
  onSelect,
  className,
}: PlatformSelectorProps) => {
  return (
    <div className={cn("flex flex-wrap justify-center gap-3", className)}>
      {platforms.map((platform) => (
        <button
          key={platform.id}
          onClick={() => onSelect(platform.id)}
          className={cn(
            "flex items-center gap-2 px-4 py-2 rounded-full border transition-all duration-300 transform hover:scale-105",
            selectedPlatform === platform.id
              ? "border-brand-500 bg-brand-100 text-brand-700 shadow-md"
              : "border-gray-200 bg-white text-gray-600 hover:border-brand-300 hover:bg-brand-50/50"
          )}
        >
          <span className="text-brand-600">{platform.icon}</span>
          <span className="font-medium text-sm">{platform.name}</span>
        </button>
      ))}
    </div>
  );
};

export default PlatformSelector;
