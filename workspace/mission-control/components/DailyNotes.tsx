import { FileText, Calendar } from "lucide-react";

interface DailyNotesProps {
  notes: any[];
}

export default function DailyNotes({ notes }: DailyNotesProps) {
  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-text-primary flex items-center gap-2">
          <span>📝</span>
          <span>Daily Notes</span>
        </h2>
        <span className="text-xs text-text-muted bg-background-elevated px-2 py-1 rounded-full">
          Auto-organized
        </span>
      </div>

      {/* Notes Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
        {notes.map((note, index) => (
          <div
            key={index}
            className="border border-border bg-background hover:bg-background-hover rounded-lg p-5 transition-colors"
          >
            {/* Header */}
            <div className="flex items-center justify-between mb-3">
              <div className="flex items-center gap-2">
                <Calendar className="w-4 h-4 text-text-muted" />
                <span className="text-sm font-medium text-text-primary">{note.date}</span>
              </div>
              <span className="text-xs text-accent-blue bg-accent-blue/10 px-2 py-1 rounded-full">
                {notes.length - index} days ago
              </span>
            </div>

            {/* Title */}
            <h3 className="text-base font-medium text-text-primary mb-2 flex items-center gap-2">
              <FileText className="w-4 h-4 text-accent-purple" />
              {note.title}
            </h3>

            {/* Content Preview */}
            <p className="text-sm text-text-secondary leading-relaxed line-clamp-3">
              {note.content}
            </p>

            {/* Action Items */}
            <div className="mt-4 pt-4 border-t border-border">
              <span className="text-xs text-text-muted">Stored in memory/</span>
            </div>
          </div>
        ))}

        {/* Empty State */}
        {notes.length === 0 && (
          <div className="col-span-1 md:col-span-2 border border-dashed border-border rounded-lg p-8 text-center">
            <FileText className="w-12 h-12 text-text-muted mx-auto mb-4" />
            <p className="text-sm text-text-muted">No daily notes found</p>
          </div>
        )}
      </div>
    </div>
  );
}
