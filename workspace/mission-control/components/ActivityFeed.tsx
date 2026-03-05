import { Clock, CheckCircle2, Plus, MessageCircle } from "lucide-react";
import { useEffect, useState } from "react";

interface ActivityItem {
  id: string;
  type: "task-created" | "task-updated" | "task-completed" | "task-deleted" | "system";
  message: string;
  timestamp: string;
  user?: string;
  taskTitle?: string;
}

export default function ActivityFeed() {
  const [activities, setActivities] = useState<ActivityItem[]>([]);
  const [filter, setFilter] = useState<"all" | "tasks" | "system">("all");

  useEffect(() => {
    // Load from localStorage or generate mock activities
    const saved = localStorage.getItem("activity-feed");
    if (saved) {
      setActivities(JSON.parse(saved));
    } else {
      // Generate initial mock activities
      const initialActivities: ActivityItem[] = [
        {
          id: "1",
          type: "task-completed",
          message: "BMW M5 completed 'NextCode QA Automation'",
          timestamp: new Date(Date.now() - 3600000).toISOString(),
          user: "BMW M5",
          taskTitle: "NextCode QA Automation",
        },
        {
          id: "2",
          type: "task-created",
          message: "Task Board Activity Feed інтеграція створена",
          timestamp: new Date(Date.now() - 7200000).toISOString(),
          user: "me",
          taskTitle: "Task Board Activity Feed інтеграція",
        },
        {
          id: "3",
          type: "system",
          message: "Gmail check scheduled for every 30 min",
          timestamp: new Date(Date.now() - 10800000).toISOString(),
        },
        {
          id: "4",
          type: "task-updated",
          message: "Deposit Streak Testing moved to Review",
          timestamp: new Date(Date.now() - 1800000).toISOString(),
          user: "BMW M5",
          taskTitle: "Deposit Streak Testing",
        },
        {
          id: "5",
          type: "system",
          message: "Mission Control v0.1.0 deployed to localhost:3000",
          timestamp: new Date(Date.now() - 86400000).toISOString(),
        },
      ];
      setActivities(initialActivities);
      localStorage.setItem("activity-feed", JSON.stringify(initialActivities));
    }
  }, []);

  const addActivity = (activity: Omit<ActivityItem, "id">) => {
    const newActivity: ActivityItem = {
      ...activity,
      id: Date.now().toString(),
      timestamp: new Date().toISOString(),
    };
    const updatedActivities = [newActivity, ...activities];
    setActivities(updatedActivities);
    localStorage.setItem("activity-feed", JSON.stringify(updatedActivities));
  };

  const getIcon = (type: ActivityItem["type"]) => {
    switch (type) {
      case "task-created":
        return <Plus className="w-4 h-4 text-accent-blue" />;
      case "task-updated":
        return <MessageCircle className="w-4 h-4 text-accent-purple" />;
      case "task-completed":
        return <CheckCircle2 className="w-4 h-4 text-accent-green" />;
      case "task-deleted":
        return <Trash2 className="w-4 h-4 text-accent-red" />;
      case "system":
        return <Clock className="w-4 h-4 text-text-muted" />;
    }
  };

  const getTypeColor = (type: ActivityItem["type"]) => {
    switch (type) {
      case "task-created":
        return "text-accent-blue bg-accent-blue/10";
      case "task-updated":
        return "text-accent-purple bg-accent-purple/10";
      case "task-completed":
        return "text-accent-green bg-accent-green/10";
      case "task-deleted":
        return "text-accent-red bg-accent-red/10";
      case "system":
        return "text-text-muted bg-background-elevated";
    }
  };

  const formatTimestamp = (timestamp: string) => {
    const date = new Date(timestamp);
    const now = new Date();
    const diff = now.getTime() - date.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(minutes / 60);
    const days = Math.floor(hours / 24);

    if (minutes < 1) return "Just now";
    if (minutes < 60) return `${minutes}m ago`;
    if (hours < 24) return `${hours}h ago`;
    if (days === 1) return "1d ago";
    return `${days}d ago`;
  };

  const filteredActivities = activities.filter((activity) => {
    if (filter === "all") return true;
    if (filter === "tasks") return activity.type.includes("task");
    if (filter === "system") return activity.type === "system";
    return true;
  });

  return (
    <div className="w-80 border-r border-border bg-background overflow-auto">
      <div className="p-4">
        <header className="flex items-center justify-between mb-6">
          <h2 className="text-lg font-semibold text-text-primary flex items-center gap-2">
            <span>📰</span>
            <span>Activity</span>
          </h2>
          <div className="flex gap-2">
            <button
              onClick={() => setFilter("all")}
              className={`px-2 py-1 text-xs rounded-md transition-colors ${
                filter === "all"
                  ? "bg-accent-blue/10 text-accent-blue"
                  : "text-text-secondary hover:bg-background-elevated"
              }`}
            >
              All
            </button>
            <button
              onClick={() => setFilter("tasks")}
              className={`px-2 py-1 text-xs rounded-md transition-colors ${
                filter === "tasks"
                  ? "bg-accent-blue/10 text-accent-blue"
                  : "text-text-secondary hover:bg-background-elevated"
              }`}
            >
              Tasks
            </button>
            <button
              onClick={() => setFilter("system")}
              className={`px-2 py-1 text-xs rounded-md transition-colors ${
                filter === "system"
                  ? "bg-accent-blue/10 text-accent-blue"
                  : "text-text-secondary hover:bg-background-elevated"
              }`}
            >
              System
            </button>
          </div>
        </header>

        {/* Activity List */}
        <div className="space-y-4">
          {filteredActivities.map((activity) => (
            <div
              key={activity.id}
              className="border-b border-border pb-4 last:border-b-0"
            >
              <div className="flex items-start gap-3">
                <div
                  className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${getTypeColor(activity.type)}`}
                >
                  {getIcon(activity.type)}
                </div>

                <div className="flex-1 min-w-0">
                  {activity.user && (
                    <span className="text-xs font-medium text-text-secondary mb-1">
                      {activity.user}
                    </span>
                  )}
                  <p className="text-sm text-text-primary">{activity.message}</p>
                  {activity.taskTitle && (
                    <p className="text-xs text-text-muted mt-1">
                      Task: "{activity.taskTitle}"
                    </p>
                  )}
                  <p className="text-xs text-text-muted mt-1">
                    {formatTimestamp(activity.timestamp)}
                  </p>
                </div>
              </div>
            </div>
          ))}

          {filteredActivities.length === 0 && (
            <div className="text-center py-8 text-text-muted">
              <p className="text-sm">No activity found</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
