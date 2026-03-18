#!/usr/bin/env python3
"""
Memory Reindex — Auto-discover insights and update RAG memory index.

Scans workspace/memory/insights/ for all .md files, updates
openclaw.json extraPaths with any new discoveries, and triggers
a memory reindex.

Usage:
    python3 scripts/memory_reindex.py              # discover + reindex
    python3 scripts/memory_reindex.py --dry-run    # show what would change
    python3 scripts/memory_reindex.py --discover   # only update extraPaths, no reindex
"""

import argparse
import json
import subprocess
import sys
from pathlib import Path


def repo_root() -> Path:
    """Find .openclaw repo root."""
    current = Path(__file__).resolve().parent.parent
    if (current / "openclaw.json").exists():
        return current
    # fallback
    return Path.home() / ".openclaw"


def discover_insight_files(root: Path) -> list[str]:
    """Find all insight .md files that should be indexed."""
    insights_dir = root / "workspace" / "memory" / "insights"
    files = []
    if insights_dir.exists():
        for f in sorted(insights_dir.glob("*.md")):
            if f.name == "README.md":
                continue
            files.append(str(f))
    return files


def get_static_extra_paths(root: Path) -> list[str]:
    """Return static files that should always be in extraPaths."""
    return [
        str(root / "workspace" / "PROJECT_KNOWLEDGE.md"),
        str(root / "workspace" / "shared" / "DAILY_INSIGHTS.md"),
    ]


def load_openclaw_json(root: Path) -> dict:
    """Load openclaw.json."""
    config_path = root / "openclaw.json"
    with open(config_path) as f:
        return json.load(f)


def save_openclaw_json(root: Path, config: dict):
    """Save openclaw.json preserving formatting."""
    config_path = root / "openclaw.json"
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
        f.write("\n")


def get_current_extra_paths(config: dict) -> list[str]:
    """Extract current extraPaths from memorySearch defaults."""
    defaults = config.get("agents", {}).get("defaults", {})
    memory_search = defaults.get("memorySearch", {})
    return memory_search.get("extraPaths", [])


def set_extra_paths(config: dict, paths: list[str]) -> dict:
    """Set extraPaths in memorySearch defaults."""
    config.setdefault("agents", {}).setdefault("defaults", {}).setdefault("memorySearch", {})
    config["agents"]["defaults"]["memorySearch"]["extraPaths"] = paths
    return config


def run_reindex(force: bool = False) -> int:
    """Run openclaw memory index."""
    cmd = ["openclaw", "memory", "index"]
    if force:
        cmd.append("--force")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[reindex] ERROR: {result.stderr.strip()}")
        return result.returncode
    # Count updated agents
    updated = result.stdout.count("Memory index updated")
    print(f"[reindex] {updated} agent(s) reindexed")
    return 0


def main():
    parser = argparse.ArgumentParser(description="Auto-discover insights and reindex RAG memory")
    parser.add_argument("--dry-run", action="store_true", help="Show what would change without modifying anything")
    parser.add_argument("--discover", action="store_true", help="Only update extraPaths, skip reindex")
    parser.add_argument("--force", action="store_true", help="Force full reindex (not just dirty files)")
    args = parser.parse_args()

    root = repo_root()
    config = load_openclaw_json(root)

    # Build desired extraPaths
    static_paths = get_static_extra_paths(root)
    insight_files = discover_insight_files(root)
    desired_paths = static_paths + insight_files

    # Compare with current
    current_paths = get_current_extra_paths(config)
    current_set = set(current_paths)
    desired_set = set(desired_paths)

    added = desired_set - current_set
    removed = current_set - desired_set

    if not added and not removed:
        print("[discover] extraPaths up to date")
        print(f"[discover] {len(desired_paths)} paths ({len(static_paths)} static + {len(insight_files)} insights)")
        if not args.dry_run and not args.discover:
            print("[reindex] running incremental reindex...")
            return run_reindex(force=args.force)
        return 0

    # Show changes
    if added:
        print(f"[discover] +{len(added)} new paths:")
        for p in sorted(added):
            print(f"  + {p}")
    if removed:
        print(f"[discover] -{len(removed)} removed paths:")
        for p in sorted(removed):
            print(f"  - {p}")

    if args.dry_run:
        print("[dry-run] would update openclaw.json and reindex")
        return 0

    # Update config
    config = set_extra_paths(config, desired_paths)
    save_openclaw_json(root, config)
    print(f"[discover] updated openclaw.json ({len(desired_paths)} extraPaths)")

    if args.discover:
        print("[discover] skipping reindex (--discover mode)")
        return 0

    # Reindex
    print("[reindex] running full reindex after discovery...")
    return run_reindex(force=True)


if __name__ == "__main__":
    raise SystemExit(main())
