"use client";

import { useState, DragEvent } from "react";
import { Plus, MoreHorizontal, Trash2, Clock } from "lucide-react";

type TaskStatus = "backlog" | "in-progress" | "review" | "done";
type TaskAssignee = "me" | "bmw-m5" | "unassigned";

interface TaskItem {
  id: string;
  title: string;
  description: string;
  status: TaskStatus;
  assignee: TaskAssignee;
  dueDate?: string;
  priority?: "high" | "medium" | "low";
}

interface TaskBoardProps {
  tasks?: TaskItem[];
}

const statusConfig = {
  backlog: {
    color: "text-text-muted",
    bg: "bg-background",
    label: "Backlog",
    icon: "○",
  },
  "in-progress": {
    color: "text-accent-blue",
    bg: "bg-accent-blue/10",
    label: "In Progress",
    icon: "Clock",
  },
  review: {
    color: "text-accent-purple",
    bg: "bg-accent-purple/10",
    label: "Review",
    icon: "○",
  },
  done: {
    color: "text-accent-green",
    bg: "bg-accent-green/10",
    label: "Done",
    icon: "●",
  },
};

const defaultTasks: TaskItem[] = [
  {
    id: "1",
    title: "Test Data Scripts - скрипти 04-05",
    description: "Отримання інформації про гравця, створення тестових бонусів",
    status: "in-progress",
    assignee: "me",
    priority: "high",
  },
  {
    id: "2",
    title: "Task Board Activity Feed інтеграція",
    description: "Додати live activity feed на лівому боці дошки",
    status: "backlog",
    assignee: "me",
    priority: "medium",
  },
  {
    id: "3",
    title: "NextCode QA Automation",
    description: "Автоматизація Playwright E2E тестів для Minebit",
    status: "done",
    assignee: "bmw-m5",
    priority: "high",
  },
  {
    id: "4",
    title: "Deposit Streak Testing",
    description: "E2E тестування бонусу Deposit Streak",
    status: "review",
    assignee: "bmw-m5",
    priority: "high",
  },
  {
    id: "5",
    title: "Mission Control UI покращення",
    description: "Додати drag & drop для задач",
    status: "backlog",
    assignee: "unassigned",
    priority: "low",
  },
];

export default function TaskBoard({ tasks = defaultTasks }: TaskBoardProps) {
  const [localTasks, setLocalTasks] = useState<TaskItem[]>(defaultTasks);
  const [draggedTask, setDraggedTask] = useState<TaskItem | null>(null);

  const handleDragStart = (task: TaskItem) => {
    setDraggedTask(task);
  };

  const handleDragOver = (e: DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: DragEvent, status: TaskStatus) => {
    e.preventDefault();
    if (!draggedTask) return;

    const task = localTasks.find((t) => t.id === draggedTask.id);
    if (!task) return;

    const updatedTasks = localTasks.map((t) =>
      t.id === task.id ? { ...t, status } : t
    );
    setLocalTasks(updatedTasks);
    setDraggedTask(null);

    // Save to localStorage
    localStorage.setItem("taskboard-tasks", JSON.stringify(updatedTasks));
  };

  const moveToStatus = (taskId: string, newStatus: TaskStatus) => {
    const updatedTasks = localTasks.map((t) =>
      t.id === taskId ? { ...t, status: newStatus } : t
    );
    setLocalTasks(updatedTasks);
    localStorage.setItem("taskboard-tasks", JSON.stringify(updatedTasks));
  };

  const deleteTask = (taskId: string) => {
    const updatedTasks = localTasks.filter((t) => t.id !== taskId);
    setLocalTasks(updatedTasks);
    localStorage.setItem("taskboard-tasks", JSON.stringify(updatedTasks));
  };

  return (
    <div className="flex h-full">
      {/* Main Kanban Board */}
      <div className="flex-1 overflow-auto">
        <div className="max-w-7xl mx-auto p-8">
          <header className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-semibold text-text-primary flex items-center gap-2">
              <span>📋</span>
              <span>Task Board</span>
            </h2>
            <button className="flex items-center gap-2 px-3 py-2 rounded-lg bg-accent-blue/10 text-accent-blue hover:bg-accent-blue/20 text-sm font-medium transition-colors">
              <Plus className="w-4 h-4" />
              <span>New Task</span>
            </button>
          </header>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {Object.entries(statusConfig).map(([statusKey, config]) => (
              <div
                key={statusKey}
                className="border border-border bg-background rounded-lg p-4"
                onDragOver={handleDragOver}
                onDrop={(e) => handleDrop(e, statusKey as TaskStatus)}
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className={`text-sm font-medium ${config.color} flex items-center gap-2`}>
                    <span className="text-base">{config.icon}</span>
                    <span>{config.label}</span>
                  </h3>
                  <span className="text-xs text-text-muted">
                    {localTasks.filter((t) => t.status === statusKey).length} tasks
                  </span>
                </div>

                <div className="space-y-3">
                  {localTasks
                    .filter((t) => t.status === statusKey)
                    .map((task) => (
                      <div
                        key={task.id}
                        draggable
                        onDragStart={() => handleDragStart(task)}
                        className={`border border-border ${config.bg} rounded-lg p-4 transition-all hover:border-border-focus cursor-grab ${
                          draggedTask?.id === task.id ? "opacity-50" : ""
                        }`}
                      >
                        <div className="flex items-start justify-between mb-2">
                          <div>
                            <h4 className="text-sm font-medium text-text-primary mb-1">
                              {task.title}
                            </h4>
                            <p className="text-xs text-text-muted line-clamp-2">
                              {task.description}
                            </p>
                          </div>
                          <div className="flex items-center gap-2">
                            {task.priority === "high" && (
                              <span className="text-xs bg-accent-red/10 text-accent-red px-2 py-1 rounded-full">
                                High
                              </span>
                            )}
                            {task.assignee === "me" && (
                              <span className="text-xs bg-background-elevated text-text-muted px-2 py-1 rounded-full">
                                Me
                              </span>
                            )}
                            {task.assignee === "bmw-m5" && (
                              <span className="text-xs bg-accent-blue/10 text-accent-blue px-2 py-1 rounded-full">
                                BMW M5
                              </span>
                            )}
                          </div>
                        </div>

                        {/* Actions */}
                        <div className="flex items-center gap-1 mt-3 pt-3 border-t border-border">
                          {statusKey !== "done" && (
                            <button
                              onClick={() => moveToStatus(task.id, "done")}
                              className="p-1.5 rounded hover:bg-background-elevated transition-colors"
                              title="Mark as done"
                            >
                              <Clock className="w-4 h-4 text-accent-green" />
                            </button>
                          )}
                          <button
                            onClick={() => deleteTask(task.id)}
                            className="p-1.5 rounded hover:bg-accent-red/10 transition-colors"
                            title="Delete task"
                          >
                            <Trash2 className="w-4 h-4 text-accent-red" />
                          </button>
                        </div>
                      </div>
                    ))}
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
