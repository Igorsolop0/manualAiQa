"use client";

import { TabType } from "./page";

interface SidebarProps {
  activeTab: TabType;
  onTabChange: (tab: TabType) => void;
}

const tabs: { id: TabType; label: string; icon: string }[] = [
  { id: "missions", label: "Missions", icon: "🚀" },
  { id: "tasks", label: "Tasks", icon: "📋" },
  { id: "calendar", label: "Calendar", icon: "📅" },
  { id: "heartbeat", label: "Heartbeat", icon: "💓" },
  { id: "memory", label: "Memory", icon: "🧠" },
  { id: "daily", label: "Daily", icon: "📝" },
];

export default function Sidebar({ activeTab, onTabChange }: SidebarProps) {
  return (
    <aside className="w-64 border-r border-border bg-background hover:bg-background-hover transition-colors">
      <div className="p-4">
        <h2 className="text-lg font-semibold text-text-primary mb-6 flex items-center gap-2">
          <span>🎛️</span>
          <span>Controls</span>
        </h2>

        <nav className="space-y-1">
          {tabs.map((tab) => (
            <button
              key={tab.id}
              onClick={() => onTabChange(tab.id)}
              className={`w-full text-left px-3 py-2 rounded-md text-sm font-medium transition-colors flex items-center gap-3 ${
                activeTab === tab.id
                  ? "bg-accent-blue/10 text-accent-blue"
                  : "text-text-secondary hover:text-text-primary hover:bg-background-elevated"
              }`}
            >
              <span className="text-base">{tab.icon}</span>
              <span>{tab.label}</span>
            </button>
          ))}
        </nav>
      </div>

      {/* Footer */}
      <div className="absolute bottom-0 left-0 w-64 p-4 border-t border-border">
        <div className="flex items-center gap-2 text-xs text-text-muted">
          <span className="w-2 h-2 rounded-full bg-accent-green animate-pulse"></span>
          <span>Connected</span>
        </div>
      </div>
    </aside>
  );
}
