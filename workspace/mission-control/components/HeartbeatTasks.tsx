import { CheckCircle2, Clock, X } from "lucide-react";

interface HeartbeatTasksProps {
  data: string;
}

interface TaskItem {
  id: string;
  title: string;
  status: "active" | "completed" | "disabled";
  frequency?: string;
}

export default function HeartbeatTasks({ data }: HeartbeatTasksProps) {
  // Parse HEARTBEAT.md data (simplified for now)
  const tasks: TaskItem[] = [
    {
      id: "gmail-check",
      title: "Gmail Check (NextCode)",
      status: "active",
      frequency: "Every 30 min (9:00-18:00 CET)",
    },
    {
      id: "confadapt-monitor",
      title: "ConfAdapt Technology Monitor",
      status: "active",
      frequency: "Weekly (Mondays 10:00 AM)",
    },
    {
      id: "qa-workflow",
      title: "QA Workflow Check (Jira → TestRail)",
      status: "active",
      frequency: "Every 30 min (9:00-18:00 CET)",
    },
  ];

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "active":
        return <Clock className="w-4 h-4 text-accent-blue" />;
      case "completed":
        return <CheckCircle2 className="w-4 h-4 text-accent-green" />;
      case "disabled":
        return <X className="w-4 h-4 text-text-muted" />;
    }
  };

  return (
    <div className="space-y-4">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-text-primary flex items-center gap-2">
          <span>💓</span>
          <span>Heartbeat Tasks</span>
        </h2>
        <span className="text-xs text-text-muted bg-background-elevated px-2 py-1 rounded-full">
          Auto-monitored
        </span>
      </div>

      {tasks.map((task) => (
        <div
          key={task.id}
          className="border border-border bg-background hover:bg-background-hover rounded-lg p-4 transition-colors"
        >
          <div className="flex items-start gap-3">
            <div className="mt-0.5">{getStatusIcon(task.status)}</div>
            <div className="flex-1">
              <h3 className="text-sm font-medium text-text-primary mb-1">
                {task.title}
              </h3>
              {task.frequency && (
                <p className="text-xs text-text-muted">{task.frequency}</p>
              )}
            </div>
          </div>
        </div>
      ))}

      {/* Raw HEARTBEAT.md display */}
      {data && (
        <div className="mt-6 border-t border-border pt-6">
          <h3 className="text-sm font-medium text-text-primary mb-3">
            HEARTBEAT.md Content
          </h3>
          <pre className="bg-background-elevated border border-border rounded-lg p-4 text-xs text-text-secondary font-mono overflow-auto max-h-64">
            {data}
          </pre>
        </div>
      )}
    </div>
  );
}
