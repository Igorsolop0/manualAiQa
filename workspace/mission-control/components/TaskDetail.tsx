import { ArrowRight, ChevronRight, MoreHorizontal } from "lucide-react";

interface TaskDetailProps {
  title: string;
  description: string;
  lastUpdated?: string;
  onAction?: () => void;
}

export default function TaskDetail({ title, description, lastUpdated, onAction }: TaskDetailProps) {
  return (
    <div className="border border-border bg-background rounded-lg p-5 transition-all hover:border-border-focus">
      {/* Header */}
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="text-base font-medium text-text-primary mb-1">{title}</h3>
          {lastUpdated && (
            <p className="text-xs text-text-muted">{lastUpdated}</p>
          )}
        </div>
        <button
          onClick={onAction}
          className="p-1.5 rounded-md hover:bg-background-elevated transition-colors"
        >
          <MoreHorizontal className="w-4 h-4 text-text-muted" />
        </button>
      </div>

      {/* Description */}
      <p className="text-sm text-text-secondary leading-relaxed mb-4">{description}</p>

      {/* Action Button */}
      {onAction && (
        <button
          onClick={onAction}
          className="w-full flex items-center justify-center gap-2 px-4 py-2.5 rounded-lg bg-accent-blue/10 text-accent-blue hover:bg-accent-blue/20 font-medium text-sm transition-colors"
        >
          <span>View Details</span>
          <ArrowRight className="w-4 h-4" />
        </button>
      )}
    </div>
  );
}
