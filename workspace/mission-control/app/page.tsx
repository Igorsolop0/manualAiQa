"use client";

import { useEffect, useState } from "react";
import Sidebar from "@/components/Sidebar";
import MissionCard from "@/components/MissionCard";
import HeartbeatTasks from "@/components/HeartbeatTasks";
import MemoryViewer from "@/components/MemoryViewer";
import DailyNotes from "@/components/DailyNotes";
import SearchBar from "@/components/SearchBar";
import { readMemory, readHeartbeat } from "@/lib/file-reader";

type TabType = "missions" | "heartbeat" | "memory" | "daily";

export default function MissionControl() {
  const [activeTab, setActiveTab] = useState<TabType>("missions");
  const [memoryData, setMemoryData] = useState<any>(null);
  const [heartbeatData, setHeartbeatData] = useState<string>("");
  const [dailyNotes, setDailyNotes] = useState<any[]>([]);
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    // Load data on mount
    async function loadData() {
      try {
        const memory = await readMemory();
        setMemoryData(memory);

        const heartbeat = await readHeartbeat();
        setHeartbeatData(heartbeat);

        // Load daily notes from memory/ directory
        // This would need a backend API, for now using placeholder
        setDailyNotes([
          { date: "2026-03-04", title: "Daily Summary", content: "..." },
        ]);
      } catch (error) {
        console.error("Failed to load data:", error);
      }
    }

    loadData();
  }, []);

  // Filter missions based on search query
  const missions = [
    {
      id: "nextcode-qa",
      title: "NextCode QA Automation",
      status: "in-progress",
      progress: 65,
      description: "Automate test data preparation and Playwright E2E tests",
    },
    {
      id: "lorypten-web3",
      title: "Lorypten Web3 Testing",
      status: "planned",
      progress: 0,
      description: "Set up Playwright testing for Solana wallet integration",
    },
    {
      id: "ai-agent-improvements",
      title: "AI Agent Improvements",
      status: "in-progress",
      progress: 40,
      description: "Optimize prompt templates and integrate Slack directly",
    },
    {
      id: "deposit-streak-testing",
      title: "Deposit Streak Testing",
      status: "in-progress",
      progress: 80,
      description: "Complete E2E tests for Deposit Streak bonus feature",
    },
  ];

  const filteredMissions = missions.filter((m) =>
    searchQuery === "" ||
    m.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
    m.description.toLowerCase().includes(searchQuery.toLowerCase())
  );

  return (
    <div className="flex h-screen bg-background text-text-primary">
      {/* Sidebar */}
      <Sidebar activeTab={activeTab} onTabChange={setActiveTab} />

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <div className="max-w-7xl mx-auto p-8">
          {/* Header with Search */}
          <header className="mb-8">
            <div className="flex items-center justify-between mb-4">
              <h1 className="text-2xl font-semibold text-text-primary flex items-center gap-2">
                <span>🎛️</span>
                <span>Mission Control</span>
              </h1>
              <span className="text-xs text-text-muted bg-background-elevated px-2 py-1 rounded-full">
                v0.1.0
              </span>
            </div>
            <div className="max-w-md">
              <SearchBar
                onSearch={setSearchQuery}
                placeholder="Search missions, tasks, or notes..."
              />
            </div>
          </header>

          {/* Tab Content */}
          {activeTab === "missions" && (
            <div className="space-y-6">
              {filteredMissions.length === 0 ? (
                <div className="text-center py-12 text-text-muted">
                  <p className="text-sm">No missions found matching "{searchQuery}"</p>
                </div>
              ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {filteredMissions.map((mission) => (
                    <MissionCard
                      key={mission.id}
                      title={mission.title}
                      status={mission.status}
                      progress={mission.progress}
                      description={mission.description}
                    />
                  ))}
                </div>
              )}
            </div>
          )}

          {activeTab === "heartbeat" && <HeartbeatTasks data={heartbeatData} />}

          {activeTab === "memory" && <MemoryViewer data={memoryData} />}

          {activeTab === "daily" && <DailyNotes notes={dailyNotes} />}
        </div>
      </main>
    </div>
  );
}
