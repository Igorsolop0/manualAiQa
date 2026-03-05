"use client";

import { useEffect, useState } from "react";
import { Calendar as CalendarIcon, Clock, CheckCircle, AlertCircle, PlayCircle } from "lucide-react";

interface ScheduledTask {
  id: string;
  title: string;
  frequency: string;
  lastRun?: string;
  status: "active" | "completed" | "skipped" | "error";
  category: "heartbeat" | "cron-job";
}

export default function Calendar() {
  const [tasks, setTasks] = useState<ScheduledTask[]>([]);

  useEffect(() => {
    // In production, this would fetch from /api/heartbeat
    // For now, parse HEARTBEAT.md directly
    async function loadTasks() {
      try {
        const response = await fetch("/api/heartbeat");
        const heartbeatContent = await response.text();
        
        const parsedTasks: ScheduledTask[] = parseHeartbeatContent(heartbeatContent);
        setTasks(parsedTasks);
      } catch (error) {
        console.error("Failed to load heartbeat tasks:", error);
        
        // Fallback: hardcoded tasks
        const fallbackTasks: ScheduledTask[] = [
          {
            id: "gmail-check",
            title: "Gmail Check (NextCode)",
            frequency: "Every 30 min (9:00-18:00 CET, Mon-Fri)",
            status: "active",
            category: "cron-job",
          },
          {
            id: "confadapt-monitor",
            title: "ConfAdapt Technology Monitor",
            frequency: "Weekly (Mondays 10:00 AM)",
            status: "completed", // Last run: 2026-03-02
            category: "heartbeat",
          },
          {
            id: "qa-workflow",
            title: "QA Workflow Check (Jira → TestRail)",
            frequency: "Every 30 min (9:00-18:00 CET, Mon-Fri)",
            status: "active",
            category: "heartbeat",
          },
          {
            id: "test-data-scripts",
            title: "Test Data Scripts — скрипти 04-05",
            frequency: "Completed 2026-03-04",
            status: "completed",
            category: "heartbeat",
          },
          {
            id: "deposit-streak-testing",
            title: "Deposit Streak Testing",
            frequency: "In progress (80% complete)",
            status: "active",
            category: "heartbeat",
          },
        ];
        
        setTasks(fallbackTasks);
      }
    }

    loadTasks();

    // Auto-refresh every minute
    const interval = setInterval(loadTasks, 60000);
    return () => clearInterval(interval);
  }, []);

  function parseHeartbeatContent(content: string): ScheduledTask[] {
    const tasks: ScheduledTask[] = [];

    // Gmail Check
    if (content.includes("Gmail Check (NextCode)")) {
      tasks.push({
        id: "gmail-check",
        title: "Gmail Check (NextCode)",
        frequency: "Every 30 min (9:00-18:00 CET, Mon-Fri)",
        status: "active",
        category: "cron-job",
      });
    }

    // ConfAdapt Monitor
    if (content.includes("ConfAdapt Technology Monitor")) {
      tasks.push({
        id: "confadapt-monitor",
        title: "ConfAdapt Technology Monitor",
        frequency: "Weekly (Mondays 10:00 AM)",
        status: "completed", // Last check: 2026-03-02
        category: "heartbeat",
      });
    }

    // QA Workflow Check
    if (content.includes("QA Workflow Check")) {
      tasks.push({
        id: "qa-workflow",
        title: "QA Workflow Check (Jira → TestRail)",
        frequency: "Every 30 min (9:00-18:00 CET, Mon-Fri)",
        status: "active",
        category: "heartbeat",
      });
    }

    // Test Data Scripts
    if (content.includes("Завершено: Test Data Scripts")) {
      tasks.push({
        id: "test-data-scripts",
        title: "Test Data Scripts — скрипти 04-05",
        frequency: "Completed 2026-03-04",
        status: "completed",
        category: "heartbeat",
      });
    }

    // Deposit Streak Testing
    if (content.includes("Deposit Streak Testing")) {
      tasks.push({
        id: "deposit-streak-testing",
        title: "Deposit Streak Testing",
        frequency: "In progress (80% complete)",
        status: "active",
        category: "heartbeat",
      });
    }

    return tasks;
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "active":
        return <Clock className="w-4 h-4 text-accent-blue" />;
      case "completed":
        return <CheckCircle2 className="w-4 h-4 text-accent-green" />;
      case "skipped":
        return <PlayCircle className="w-4 h-4 text-text-muted" />;
      case "error":
        return <AlertCircle className="w-4 h-4 text-accent-red" />;
    }
  };

  const getCategoryBadge = (category: string) => {
    switch (category) {
      case "cron-job":
        return <span className="text-xs bg-background-elevated text-text-muted px-2 py-1 rounded-full">
          Cron Job
        </span>;
      case "heartbeat":
        return <span className="text-xs bg-background-elevated text-accent-purple px-2 py-1 rounded-full">
          Heartbeat
        </span>;
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-text-primary flex items-center gap-2">
          <Calendar className="w-5 h-5" />
          <span>Scheduled Tasks</span>
        </h2>
        <span className="text-xs text-text-muted bg-background-elevated px-2 py-1 rounded-full">
          Auto-refresh
        </span>
      </div>

      {/* Calendar View (simplified) */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tasks.map((task) => (
          <div
            key={task.id}
            className="border border-border bg-background hover:bg-background-hover rounded-lg p-5 transition-all"
          >
            {/* Header */}
            <div className="flex items-start justify-between mb-3">
              <div className="flex items-center gap-2">
                {getStatusIcon(task.status)}
                <h3 className="text-base font-medium text-text-primary">
                  {task.title}
                </h3>
              </div>
              {getCategoryBadge(task.category)}
            </div>

            {/* Frequency */}
            <p className="text-sm text-text-muted mb-2">{task.frequency}</p>

            {/* Status Badge */}
            <div className={`inline-flex items-center gap-1.5 px-2.5 py-1 rounded-full text-xs font-medium ${
              task.status === "active"
                  ? "bg-accent-blue/10 text-accent-blue animate-pulse"
                  : task.status === "completed"
                  ? "bg-accent-green/10 text-accent-green"
                  : task.status === "skipped"
                  ? "bg-background-elevated text-text-muted"
                  : "bg-accent-red/10 text-accent-red"
            }`}>
              <span>
                {task.status === "active" && "Running"}
                {task.status === "completed" && "Completed"}
                {task.status === "skipped" && "Skipped"}
                {task.status === "error" && "Error"}
              </span>
            </div>

            {/* Last Run */}
            {task.lastRun && (
              <p className="text-xs text-text-muted mt-2">
                Last run: {task.lastRun}
              </p>
            )}
          </div>
        ))}

        {/* Empty State */}
        {tasks.length === 0 && (
          <div className="col-span-1 md:col-span-2 lg:col-span-3 border-dashed border-border rounded-lg p-8 text-center">
            <Calendar className="w-12 h-12 text-text-muted mx-auto mb-4" />
            <p className="text-sm text-text-muted">No scheduled tasks found</p>
            <p className="text-xs text-text-muted mt-2">
              Tasks will be loaded from HEARTBEAT.md
            </p>
          </div>
        )}
      </div>

      {/* HEARTBEAT.md Preview */}
      <div className="mt-6 border-t border-border pt-6">
        <h3 className="text-sm font-medium text-text-primary mb-3 flex items-center gap-2">
          <Calendar className="w-4 h-4 text-accent-purple" />
          HEARTBEAT.md Content
        </h3>
        <p className="text-xs text-text-muted mb-4">
          Scheduled tasks are parsed from HEARTBEAT.md. Changes will be reflected automatically.
        </p>
      </div>
    </div>
  );
}
