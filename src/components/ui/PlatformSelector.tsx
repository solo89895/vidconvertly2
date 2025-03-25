
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
            "flex items-center gap-2 px-4 py-2 rounded-full border transition-all duration-200",
            selectedPlatform === platform.id
              ? "border-brand-400 bg-brand-50 text-brand-700"
              : "border-brand-200 bg-white text-brand-600 hover:border-brand-300 hover:bg-brand-50/50"
          )}
        >
          {platform.icon}
          <span className="font-medium text-sm">{platform.name}</span>
        </button>
      ))}
    </div>
  );
};

export default PlatformSelector;
