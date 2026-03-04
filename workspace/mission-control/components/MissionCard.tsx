import { Clock, CheckCircle2, AlertCircle, PlayCircle } from "lucide-react";

interface MissionCardProps {
  title: string;
  status: "completed" | "in-progress" | "planned" | "blocked";
  progress: number;
  description: string;
}

const statusConfig = {
  completed: {
    icon: CheckCircle2,
    color: "text-accent-green",
    bg: "bg-accent-green/10",
    label: "Completed",
  },
  "in-progress": {
    icon: Clock,
    color: "text-accent-blue",
    bg: "bg-accent-blue/10",
    label: "In Progress",
  },
  planned: {
    icon: PlayCircle,
    color: "text-text-muted",
    bg: "bg-text-muted/10",
    label: "Planned",
  },
  blocked: {
    icon: AlertCircle,
    color: "text-accent-red",
    bg: "bg-accent-red/10",
    label: "Blocked",
  },
};

export default function MissionCard({
  title,
  status,
  progress,
  description,
}: MissionCardProps) {
  const config = statusConfig[status];
  const StatusIcon = config.icon;

  return (
    <div className="group border border-border bg-background hover:bg-background-hover rounded-lg p-5 transition-all hover:border-border-focus">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <h3 className="text-base font-medium text-text-primary group-hover:text-accent-blue transition-colors">
          {title}
        </h3>
        <div className={`flex items-center gap-1.5 px-2 py-1 rounded-full ${config.bg} ${config.color}`}>
          <StatusIcon className="w-3.5 h-3.5" />
          <span className="text-xs font-medium">{config.label}</span>
        </div>
      </div>

      {/* Progress Bar */}
      {status !== "planned" && (
        <div className="mb-3">
          <div className="flex items-center justify-between text-xs text-text-muted mb-1">
            <span>Progress</span>
            <span>{progress}%</span>
          </div>
          <div className="h-1.5 bg-background-elevated rounded-full overflow-hidden">
            <div
              className={`h-full rounded-full transition-all ${
                status === "completed"
                  ? "bg-accent-green"
                  : status === "in-progress"
                  ? "bg-accent-blue"
                  : status === "blocked"
                  ? "bg-accent-red"
                  : "bg-text-muted"
              }`}
              style={{ width: `${progress}%` }}
            ></div>
          </div>
        </div>
      )}

      {/* Description */}
      <p className="text-sm text-text-secondary leading-relaxed">{description}</p>
    </div>
  );
}
