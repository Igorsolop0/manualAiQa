# 🎛️ Mission Control Dashboard

Next.js-based dashboard for managing work, tasks, and knowledge base. Styled after Linear.

## Features

- **🚀 Missions Tab** - Track ongoing projects with progress tracking
- **💓 Heartbeat Tab** - Monitor automated tasks (Gmail, Jira, ConfAdapt)
- **🧠 Memory Tab** - View long-term knowledge base (MEMORY.md)
- **📝 Daily Tab** - Browse daily notes from memory/ directory

## Tech Stack

- **Next.js 14** - App Router, React Server Components
- **TypeScript** - Type safety
- **Tailwind CSS** - Linear-inspired dark theme
- **Lucide React** - Icon library

## Getting Started

### Install Dependencies

```bash
npm install
```

### Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) in your browser.

### Build for Production

```bash
npm run build
npm start
```

## File Structure

```
mission-control/
├── app/
│   ├── api/           # API routes (read MEMORY.md, HEARTBEAT.md)
│   ├── layout.tsx     # Root layout with fonts
│   ├── page.tsx       # Main page with tab switching
│   └── globals.css    # Global styles
├── components/
│   ├── Sidebar.tsx     # Navigation tabs
│   ├── MissionCard.tsx # Project cards with progress
│   ├── HeartbeatTasks.tsx # Automated task monitoring
│   ├── MemoryViewer.tsx   # MEMORY.md display
│   └── DailyNotes.tsx    # Daily notes grid
├── lib/
│   └── file-reader.ts # Frontend API client (placeholder)
└── public/             # Static assets
```

## API Endpoints

- `GET /api/memory` - Returns MEMORY.md content as JSON
- `GET /api/heartbeat` - Returns HEARTBEAT.md content as text
- `GET /api/daily-notes` - Returns last 7 days of daily notes

## Data Sources

The dashboard reads from these files in the workspace:

- `MEMORY.md` - Long-term knowledge base
- `HEARTBEAT.md` - Automated task schedules
- `memory/YYYY-MM-DD.md` - Daily notes

## Styling

Uses a Linear-inspired dark theme:

- **Background**: `#08080A` (deep black)
- **Border**: `#2A2A2D` (subtle)
- **Text Primary**: `#F3F4F6` (off-white)
- **Accent Blue**: `#5E6AD2` (primary)
- **Accent Green**: `#34D399` (success)
- **Accent Red**: `#F87171` (error)

## Future Improvements

- [ ] Real-time file watching (no need to refresh)
- [ ] Edit MEMORY.md directly from dashboard
- [ ] Add/complete heartbeat tasks
- [ ] Connect to Jira/TestRail API directly
- [ ] Mission creation and management
- [ ] Search across all data sources

---

*Built with Next.js, Tailwind CSS, and TypeScript.*
