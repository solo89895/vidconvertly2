
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
              ? "border-brand-500 bg-brand-500/20 text-brand-400 neon-glow"
              : "border-gray-700 bg-gray-800/50 text-gray-400 hover:border-brand-500/50 hover:bg-gray-800"
          )}
        >
          <span className="text-brand-400">{platform.icon}</span>
          <span className="font-medium text-sm">{platform.name}</span>
        </button>
      ))}
    </div>
  );
};

export default PlatformSelector;
