"use client";

import { useState, useMemo } from "react";
import { Search, Plus, Calendar as CalendarIcon, FileText, Trash2, Edit2, ChevronDown, ChevronRight } from "lucide-react";

interface MemoryEntry {
  date: string;
  category: "work" | "personal" | "learning" | "idea" | "config";
  title: string;
  content: string;
  tags?: string[];
}

interface MemoryViewerProps {
  entries: MemoryEntry[];
  todayDate: string;
  onAddEntry?: (entry: Omit<MemoryEntry, "id">) => void;
}

const categoryConfig = {
  work: {
    color: "text-accent-blue",
    bg: "bg-accent-blue/10",
    label: "Work",
    icon: "💼",
  },
  personal: {
    color: "text-accent-purple",
    bg: "bg-accent-purple/10",
    label: "Personal",
    icon: "👤",
  },
  learning: {
    color: "text-accent-green",
    bg: "bg-accent-green/10",
    label: "Learning",
    icon: "📚",
  },
  idea: {
    color: "text-accent-orange",
    bg: "bg-accent-orange/10",
    label: "Idea",
    icon: "💡",
  },
  config: {
    color: "text-text-muted",
    bg: "bg-background",
    label: "Config",
    icon: "⚙️",
  },
};

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr);
  return date.toLocaleDateString("en-US", {
    month: "short",
    day: "numeric",
    year: "numeric",
  });
};

const sortEntries = (entries: MemoryEntry[], sortBy: "date" | "category") => {
  const sorted = [...entries];

  if (sortBy === "date") {
    sorted.sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime());
  } else if (sortBy === "category") {
    sorted.sort((a, b) => a.category.localeCompare(b.category));
  }

  return sorted;
};

export default function MemoryViewer({ entries, todayDate, onAddEntry }: MemoryViewerProps) {
  const [searchQuery, setSearchQuery] = useState("");
  const [sortBy, setSortBy] = useState<"date" | "category">("date");
  const [showAddModal, setShowAddModal] = useState(false);
  const [newEntry, setNewEntry] = useState<Partial<MemoryEntry>>({
    category: "work",
    title: "",
    content: "",
  });

  // Filter entries by search query
  const filteredEntries = useMemo(() => {
    if (!searchQuery) return entries;

    const query = searchQuery.toLowerCase();
    return entries.filter((entry) =>
      entry.title.toLowerCase().includes(query) ||
      entry.content.toLowerCase().includes(query) ||
      entry.tags?.some((tag) => tag.toLowerCase().includes(query))
    );
  }, [entries, searchQuery]);

  // Sort entries
  const sortedEntries = useMemo(() => {
    return sortEntries(filteredEntries, sortBy);
  }, [filteredEntries, sortBy]);

  // Group entries by date
  const entriesByDate = useMemo(() => {
    const grouped: { [key: string]: MemoryEntry[] } = {};

    sortedEntries.forEach((entry) => {
      const dateKey = new Date(entry.date).toDateString();
      if (!grouped[dateKey]) {
        grouped[dateKey] = [];
      }
      grouped[dateKey].push(entry);
    });

    return grouped;
  }, [sortedEntries]);

  // Find today's daily notes file
  const todayEntry = entries.find((e) => e.date === todayDate);
  const isTodayDailyNote = todayEntry?.category === "daily" || false;

  // Add new entry handler
  const handleAddEntry = () => {
    if (!newEntry.title || !newEntry.content) return;

    const entry: MemoryEntry = {
      id: Date.now().toString(),
      date: new Date().toISOString(),
      ...newEntry,
      tags: newEntry.tags || [],
    };

    onAddEntry(entry);
    setShowAddModal(false);
    setNewEntry({ category: "work", title: "", content: "", tags: [] });
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h2 className="text-xl font-semibold text-text-primary flex items-center gap-2">
          <FileText className="w-5 h-5 text-accent-purple" />
          <span>Memory Base</span>
        </h2>
        <div className="flex items-center gap-3">
          {/* Search */}
          <div className="relative">
            <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-text-muted" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search memory..."
              className="w-64 bg-background-elevated border border-border rounded-lg pl-10 pr-4 py-2.5 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent-purple focus:ring-1 focus:ring-accent-purple/20"
            />
          </div>

          {/* Sort */}
          <div className="flex items-center gap-2">
            <span className="text-xs text-text-muted">Sort:</span>
            <select
              value={sortBy}
              onChange={(e) => setSortBy(e.target.value as "date" | "category")}
              className="bg-background-elevated border border-border rounded-lg px-3 py-2 text-sm text-text-primary focus:outline-none focus:border-accent-purple"
            >
              <option value="date">Date</option>
              <option value="category">Category</option>
            </select>
          </div>

          {/* Add Entry Button */}
          <button
            onClick={() => setShowAddModal(true)}
            className="flex items-center gap-2 px-3 py-2 rounded-lg bg-accent-purple/10 text-accent-purple hover:bg-accent-purple/20 font-medium text-sm transition-colors"
          >
            <Plus className="w-4 h-4" />
            <span>Add Entry</span>
          </button>
        </div>
      </div>

      {/* Today's Daily Note Indicator */}
      {isTodayDailyNote && (
        <div className="bg-accent-green/10 border border-accent-green/20 rounded-lg p-4 mb-6">
          <div className="flex items-center gap-2">
            <CalendarIcon className="w-4 h-4 text-accent-green" />
            <span className="text-sm font-medium text-text-primary">
              Today's Daily Notes ({todayDate})
            </span>
          </div>
          <p className="text-xs text-text-muted mt-1">
            Click to view or edit your daily notes file
          </p>
        </div>
      )}

      {/* Memory Entries Grouped by Date */}
      <div className="space-y-6">
        {Object.entries(entriesByDate)
          .sort(([dateA], [dateB]) => new Date(dateB).getTime() - new Date(dateA).getTime())
          .map(([dateKey, dateEntries]) => (
            <div key={dateKey} className="border border-border bg-background rounded-lg p-5">
              {/* Date Header */}
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-base font-medium text-text-primary flex items-center gap-2">
                  <CalendarIcon className="w-4 h-4 text-accent-blue" />
                  <span>{formatDate(dateKey)}</span>
                </h3>
                <span className="text-xs text-text-muted">
                  {dateEntries.length} {dateEntries.length === 1 ? "entry" : "entries"}
                </span>
              </div>

              {/* Entries */}
              <div className="space-y-3">
                {dateEntries.map((entry) => {
                  const config = categoryConfig[entry.category];

                  return (
                    <div
                      key={entry.id}
                      className={`border-l-2 ${config.bg} rounded-lg p-4 hover:bg-background-hover transition-all`}
                    >
                      {/* Entry Header */}
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center gap-2">
                          <span className={`text-base ${config.color}`}>{config.icon}</span>
                          <h4 className="text-sm font-medium text-text-primary">{entry.title}</h4>
                        </div>
                        <span className="text-xs text-text-muted">{config.label}</span>
                      </div>

                      {/* Content */}
                      <p className="text-sm text-text-secondary leading-relaxed mb-3">
                        {entry.content}
                      </p>

                      {/* Tags */}
                      {entry.tags && entry.tags.length > 0 && (
                        <div className="flex flex-wrap gap-1">
                          {entry.tags.map((tag) => (
                            <span
                              key={tag}
                              className="text-xs bg-background-elevated text-text-muted px-2 py-1 rounded-full"
                            >
                              #{tag}
                            </span>
                          ))}
                        </div>
                      )}

                      {/* Actions */}
                      <div className="flex items-center gap-2 mt-3 pt-3 border-t border-border">
                        <button
                          className="p-1.5 rounded hover:bg-background-elevated transition-colors"
                          title="View details"
                        >
                          <ChevronRight className="w-4 h-4 text-text-muted" />
                        </button>
                        <button
                          className="p-1.5 rounded hover:bg-accent-red/10 hover:text-accent-red transition-colors"
                          title="Delete entry"
                        >
                          <Trash2 className="w-4 h-4 text-accent-red" />
                        </button>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          ))}

        {/* Empty State */}
        {sortedEntries.length === 0 && (
          <div className="border-dashed border-border rounded-lg p-8 text-center">
            <FileText className="w-12 h-12 text-text-muted mx-auto mb-4" />
            <p className="text-sm text-text-muted">No memory entries found</p>
            <p className="text-xs text-text-muted mt-2">
              Add entries via MEMORY.md or use the Add Entry button above
            </p>
          </div>
        )}
      </div>

      {/* Add Entry Modal */}
      {showAddModal && (
        <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
          <div className="bg-background border border-border rounded-lg p-6 w-full max-w-2xl">
            <div className="flex items-center justify-between mb-6">
              <h3 className="text-lg font-semibold text-text-primary">Add Memory Entry</h3>
              <button
                onClick={() => setShowAddModal(false)}
                className="p-1.5 rounded hover:bg-background-elevated transition-colors"
              >
                ✕
              </button>
            </div>

            {/* Form */}
            <div className="space-y-4">
              {/* Category */}
              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">Category</label>
                <select
                  value={newEntry.category}
                  onChange={(e) => setNewEntry({ ...newEntry, category: e.target.value as MemoryEntry["category"] })}
                  className="w-full bg-background-elevated border border-border rounded-lg px-3 py-2.5 text-sm text-text-primary focus:outline-none focus:border-accent-purple"
                >
                  {Object.entries(categoryConfig).map(([key, config]) => (
                    <option key={key} value={key}>
                      {config.icon} {config.label}
                    </option>
                  ))}
                </select>
              </div>

              {/* Title */}
              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">Title</label>
                <input
                  type="text"
                  value={newEntry.title}
                  onChange={(e) => setNewEntry({ ...newEntry, title: e.target.value })}
                  placeholder="e.g., Test Data Scripts completed"
                  className="w-full bg-background-elevated border border-border rounded-lg px-3 py-2.5 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent-purple"
                />
              </div>

              {/* Content */}
              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">Content</label>
                <textarea
                  value={newEntry.content}
                  onChange={(e) => setNewEntry({ ...newEntry, content: e.target.value })}
                  placeholder="Describe what happened, what you learned, or ideas..."
                  rows={4}
                  className="w-full bg-background-elevated border border-border rounded-lg px-3 py-2.5 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent-purple resize-none"
                />
              </div>

              {/* Tags */}
              <div>
                <label className="block text-sm font-medium text-text-primary mb-2">Tags (comma separated)</label>
                <input
                  type="text"
                  value={newEntry.tags?.join(", ")}
                  onChange={(e) => setNewEntry({ ...newEntry, tags: e.target.value.split(",").map((t) => t.trim()) })}
                  placeholder="work, nextcode, qa, testing, bonus..."
                  className="w-full bg-background-elevated border border-border rounded-lg px-3 py-2.5 text-sm text-text-primary placeholder:text-text-muted focus:outline-none focus:border-accent-purple"
                />
              </div>
            </div>

            {/* Actions */}
            <div className="flex justify-end gap-3">
              <button
                onClick={() => setShowAddModal(false)}
                className="px-4 py-2 rounded-lg border border-border text-sm text-text-primary hover:bg-background-elevated transition-colors"
              >
                Cancel
              </button>
              <button
                onClick={handleAddEntry}
                disabled={!newEntry.title || !newEntry.content}
                className="px-4 py-2 rounded-lg bg-accent-purple text-white font-medium text-sm hover:bg-accent-purple/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
              >
                <Plus className="w-4 h-4" />
                Add Entry
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
