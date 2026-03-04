import { Brain, FileText, Hash, Lightbulb } from "lucide-react";

interface MemoryViewerProps {
  data: any;
}

export default function MemoryViewer({ data }: MemoryViewerProps) {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-text-primary flex items-center gap-2">
          <span>🧠</span>
          <span>Memory Base</span>
        </h2>
        <span className="text-xs text-text-muted bg-background-elevated px-2 py-1 rounded-full">
          Long-term storage
        </span>
      </div>

      {/* Memory Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
        <div className="border border-border bg-background rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <FileText className="w-5 h-5 text-accent-blue" />
            <h3 className="text-sm font-medium text-text-primary">
              Gmail Integration
            </h3>
          </div>
          <p className="text-xs text-text-muted">
            Status: <span className="text-accent-green">✅ Active</span>
          </p>
        </div>

        <div className="border border-border bg-background rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <Hash className="w-5 h-5 text-accent-purple" />
            <h3 className="text-sm font-medium text-text-primary">
              Jira API
            </h3>
          </div>
          <p className="text-xs text-text-muted">
            Status: <span className="text-accent-green">✅ Active</span>
          </p>
        </div>

        <div className="border border-border bg-background rounded-lg p-4">
          <div className="flex items-center gap-2 mb-3">
            <Brain className="w-5 h-5 text-accent-green" />
            <h3 className="text-sm font-medium text-text-primary">
              Test Data Scripts
            </h3>
          </div>
          <p className="text-xs text-text-muted">
            Status: <span className="text-accent-green">✅ Ready</span>
          </p>
        </div>
      </div>

      {/* Raw MEMORY.md Display */}
      {data && (
        <div className="border-t border-border pt-6">
          <div className="flex items-center gap-2 mb-3">
            <Lightbulb className="w-4 h-4 text-accent-blue" />
            <h3 className="text-sm font-medium text-text-primary">
              MEMORY.md Content
            </h3>
          </div>
          <pre className="bg-background-elevated border border-border rounded-lg p-4 text-xs text-text-secondary font-mono overflow-auto max-h-96 whitespace-pre-wrap">
            {typeof data === "object" ? JSON.stringify(data, null, 2) : data}
          </pre>
        </div>
      )}
    </div>
  );
}
