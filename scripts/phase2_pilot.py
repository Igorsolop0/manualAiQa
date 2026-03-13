#!/usr/bin/env python3
"""Phase 2 pilot helper: run-centric scaffolding + legacy dual-write sync."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import shutil
import subprocess
import time
from pathlib import Path


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def rel_path(root: Path, path: Path) -> str:
    try:
        return str(path.resolve().relative_to(root.resolve()))
    except ValueError:
        return str(path.resolve())


def ensure_json_file(path: Path, default_data: dict) -> dict:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(default_data, indent=2) + "\n", encoding="utf-8")
        return default_data
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"Invalid JSON at {path}: {exc}") from exc


def save_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


def next_run_id(runs_dir: Path, ticket_id: str) -> str:
    date_code = dt.datetime.now().strftime("%Y%m%d")
    prefix = f"{ticket_id}-{date_code}-"
    max_seq = 0
    if runs_dir.exists():
        for child in runs_dir.iterdir():
            if not child.is_dir():
                continue
            name = child.name
            if not name.startswith(prefix):
                continue
            suffix = name[len(prefix) :]
            if suffix.isdigit():
                max_seq = max(max_seq, int(suffix))
    return f"{prefix}{max_seq + 1:02d}"


def build_manifest(
    root: Path,
    ticket_id: str,
    run_id: str,
    project: str,
    legacy_task_file: Path | None,
    legacy_results_dir: Path,
) -> dict:
    run_dir = root / "shared" / "runs" / run_id
    return {
        "run_id": run_id,
        "ticket_id": ticket_id,
        "project": project,
        "mode": "phase2-dual-write-pilot",
        "created_at": utc_now(),
        "status": "initialized",
        "legacy": {
            "task_file_ref": rel_path(root, legacy_task_file) if legacy_task_file else None,
            "results_dir_ref": rel_path(root, legacy_results_dir),
        },
        "run_paths": {
            "intake": rel_path(root, run_dir / "intake"),
            "plan": rel_path(root, run_dir / "plan"),
            "handoffs": rel_path(root, run_dir / "handoffs"),
            "sessions": rel_path(root, run_dir / "sessions"),
            "evidence_ui": rel_path(root, run_dir / "evidence" / "ui"),
            "evidence_api": rel_path(root, run_dir / "evidence" / "api"),
            "evidence_legacy_mirror": rel_path(root, run_dir / "evidence" / "legacy-mirror"),
            "results": rel_path(root, run_dir / "results"),
            "learning": rel_path(root, run_dir / "learning"),
        },
    }


def build_task_charter(ticket_id: str, run_id: str, project: str) -> dict:
    return {
        "task_id": ticket_id,
        "run_id": run_id,
        "project": project,
        "title": f"{ticket_id} - Phase 2 pilot dual-write run",
        "goal": "Execute one ticket with run-centric ledger while preserving legacy outputs.",
        "source": {"jira_key": ticket_id},
        "scope": {"ui": True, "api": True, "research": False},
        "preconditions": [
            "Legacy workspace paths remain active.",
            "Pilot run initialized via scripts/phase2_pilot.py.",
        ],
        "data_needs": [],
        "assertions": [
            "Legacy evidence is present under workspace/shared/test-results/<ticket>.",
            "Mirrored evidence exists under shared/runs/<run_id>/evidence/legacy-mirror/.",
        ],
        "success_criteria": [
            "Nexus can review ticket from run folder.",
            "Legacy workflow remains unbroken.",
        ],
        "status": "planned",
        "owner": "nexus",
        "next_owner": "qa-agent",
    }


def build_handoff(
    run_id: str, receiver: str, state_ref: str, expected_next_step: str, notes: list[str]
) -> dict:
    return {
        "run_id": run_id,
        "from": "nexus",
        "to": receiver,
        "state_refs": [state_ref],
        "session_refs": [],
        "entity_ids": {},
        "pending_assertions": [],
        "expected_next_step": expected_next_step,
        "recommended_owner": receiver,
        "notes": notes,
    }


def choose_task_file(legacy_tasks_dir: Path, ticket_id: str, explicit: str | None) -> Path | None:
    if explicit:
        candidate = Path(explicit).expanduser()
        if not candidate.exists():
            raise SystemExit(f"Task file not found: {candidate}")
        return candidate
    default_candidate = legacy_tasks_dir / f"{ticket_id}.md"
    if default_candidate.exists():
        return default_candidate
    return None


def copy_file_if_present(src: Path, dst: Path) -> bool:
    if not src.exists():
        return False
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return True


def copy_tree_incremental(src_dir: Path, dst_dir: Path) -> tuple[int, int]:
    copied = 0
    skipped = 0
    if not src_dir.exists():
        return copied, skipped

    for src_path in src_dir.rglob("*"):
        rel = src_path.relative_to(src_dir)
        dst_path = dst_dir / rel
        if src_path.is_dir():
            dst_path.mkdir(parents=True, exist_ok=True)
            continue

        dst_path.parent.mkdir(parents=True, exist_ok=True)
        should_copy = True
        if dst_path.exists():
            src_stat = src_path.stat()
            dst_stat = dst_path.stat()
            should_copy = not (
                src_stat.st_size == dst_stat.st_size
                and int(src_stat.st_mtime) == int(dst_stat.st_mtime)
            )

        if should_copy:
            shutil.copy2(src_path, dst_path)
            copied += 1
        else:
            skipped += 1
    return copied, skipped


def export_run_contracts_to_legacy(run_dir: Path, legacy_results_dir: Path) -> list[str]:
    exported: list[str] = []
    legacy_contracts_dir = legacy_results_dir / "contracts"
    run_copy_dir = legacy_contracts_dir / "run-copy"

    primary_files = [
        ("plan/task-charter.json", "task-charter.json"),
        ("handoffs/nexus-to-clawver.json", "handoff-nexus-to-clawver.json"),
        ("handoffs/nexus-to-cipher.json", "handoff-nexus-to-cipher.json"),
    ]
    for src_rel, dst_name in primary_files:
        src = run_dir / src_rel
        dst = legacy_contracts_dir / dst_name
        if copy_file_if_present(src, dst):
            exported.append(str(dst))

    for folder in ("plan", "handoffs", "results", "sessions"):
        src_folder = run_dir / folder
        if not src_folder.exists():
            continue
        for src in src_folder.rglob("*.json"):
            rel = src.relative_to(run_dir)
            dst = run_copy_dir / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            exported.append(str(dst))

    return exported


def update_active_pilot_registry(
    registry_path: Path,
    ticket_id: str,
    run_id: str,
    legacy_results_dir: Path,
    task_file: Path | None,
    root: Path,
) -> None:
    data = ensure_json_file(
        registry_path,
        {
            "updated_at": utc_now(),
            "tickets": {},
        },
    )
    tickets = data.setdefault("tickets", {})
    tickets[ticket_id] = {
        "active_run_id": run_id,
        "mode": "dual-write",
        "status": "active",
        "legacy_results_ref": rel_path(root, legacy_results_dir),
        "task_file_ref": rel_path(root, task_file) if task_file else None,
        "updated_at": utc_now(),
    }
    data["updated_at"] = utc_now()
    save_json(registry_path, data)


def ensure_sessions_registry(path: Path, run_id: str) -> None:
    data = ensure_json_file(
        path,
        {
            "version": 1,
            "updated_at": utc_now(),
            "sessions": [],
            "by_run": {},
        },
    )
    by_run = data.setdefault("by_run", {})
    by_run.setdefault(run_id, [])
    data["updated_at"] = utc_now()
    save_json(path, data)


def normalize_ref(root: Path, raw_ref: str) -> str:
    candidate = Path(raw_ref).expanduser()
    if candidate.is_absolute():
        return rel_path(root, candidate)
    return raw_ref


def sanitize_id(value: str) -> str:
    safe = re.sub(r"[^a-zA-Z0-9._-]+", "-", value.strip())
    safe = safe.strip("-")
    return safe or "unknown"


def register_session_record(
    root: Path,
    run_id: str,
    project: str,
    subject_type: str,
    owner: str,
    storage_state_ref: str,
    token_ref: str,
    status: str,
    refresh_strategy: str,
    expires_at: str | None,
    session_id: str | None,
) -> tuple[str, Path]:
    created_at = utc_now()
    final_session_id = session_id or (
        f"sess-{sanitize_id(subject_type)}-{sanitize_id(run_id.lower())}-{dt.datetime.now().strftime('%H%M%S')}"
    )

    record = {
        "session_id": final_session_id,
        "project": project,
        "subject_type": subject_type,
        "owner": owner,
        "storage_state_ref": normalize_ref(root, storage_state_ref),
        "token_ref": normalize_ref(root, token_ref),
        "created_at": created_at,
        "status": status,
        "refresh_strategy": refresh_strategy,
    }
    if expires_at:
        record["expires_at"] = expires_at

    shared_record_path = root / "shared" / "sessions" / f"{final_session_id}.json"
    save_json(shared_record_path, record)

    run_record_path = root / "shared" / "runs" / run_id / "sessions" / f"{final_session_id}.json"
    save_json(run_record_path, record)

    registry_path = root / "shared" / "sessions" / "registry.json"
    registry = ensure_json_file(
        registry_path,
        {
            "version": 1,
            "updated_at": utc_now(),
            "sessions": [],
            "by_run": {},
        },
    )
    sessions = registry.setdefault("sessions", [])
    by_run = registry.setdefault("by_run", {})
    run_items = by_run.setdefault(run_id, [])

    index_item = {
        "session_id": final_session_id,
        "run_id": run_id,
        "owner": owner,
        "subject_type": subject_type,
        "status": status,
        "record_ref": rel_path(root, shared_record_path),
        "updated_at": utc_now(),
    }

    replaced = False
    for idx, item in enumerate(sessions):
        if item.get("session_id") == final_session_id:
            sessions[idx] = index_item
            replaced = True
            break
    if not replaced:
        sessions.append(index_item)

    if final_session_id not in run_items:
        run_items.append(final_session_id)

    registry["updated_at"] = utc_now()
    save_json(registry_path, registry)

    return final_session_id, shared_record_path


def write_result_packet(
    root: Path,
    run_id: str,
    agent: str,
    status: str,
    assertions_passed: list[str],
    assertions_failed: list[str],
    blockers: list[str],
    evidence_refs: list[str],
    confidence: str,
    recommended_next_owner: str,
    notes: list[str],
) -> Path:
    packet = {
        "run_id": run_id,
        "agent": agent,
        "status": status,
        "assertions_passed": assertions_passed,
        "assertions_failed": assertions_failed,
        "blockers": blockers,
        "evidence_refs": [normalize_ref(root, ref) for ref in evidence_refs],
        "confidence": confidence,
        "recommended_next_owner": recommended_next_owner,
    }
    if notes:
        packet["notes"] = notes

    safe_agent = sanitize_id(agent.lower())
    out_path = root / "shared" / "runs" / run_id / "results" / f"{safe_agent}-result.json"
    save_json(out_path, packet)
    return out_path


def build_dispatch_block(root: Path, ticket_id: str, run_id: str, agent: str) -> str:
    agent_safe = sanitize_id(agent.lower())
    if agent == "qa-agent":
        session_owner = "qa-agent"
        refresh_strategy = "ui_login"
        default_evidence = f"workspace/shared/test-results/{ticket_id}/results.json"
        session_hint = (
            "If auth/session was used in this run, register session-record (reference-only handoff):"
        )
    else:
        session_owner = "api-docs-agent"
        refresh_strategy = "api_refresh"
        default_evidence = f"workspace/shared/test-results/{ticket_id}/backend-oauth-test-results.json"
        session_hint = (
            "If this run used player/admin token artifacts, register session-record (reference-only handoff):"
        )

    lines = [
        "## Phase 2 Pilot Dispatch Hooks (Auto-generated)",
        "",
        f"- **run_id:** `{run_id}`",
        f"- **agent:** `{agent}`",
        "- **mode:** `dual-write` (legacy + run mirror)",
        "",
        "After execution, run mirror sync:",
        "```bash",
        f"python3 {root / 'scripts' / 'phase2_pilot.py'} sync-legacy --ticket {ticket_id}",
        "```",
        "",
        session_hint,
        "```bash",
        (
            f"python3 {root / 'scripts' / 'phase2_pilot.py'} register-session --ticket {ticket_id} "
            f"--project minebit --subject-type player --owner {session_owner} "
            "--storage-state-ref workspace/shared/test-auth/prod-player-auth.json "
            "--token-ref workspace/shared/test-auth/token.txt --status active "
            f"--refresh-strategy {refresh_strategy}"
        ),
        "```",
        "",
        "Emit result packet for Nexus review:",
        "```bash",
        (
            f"python3 {root / 'scripts' / 'phase2_pilot.py'} emit-result --ticket {ticket_id} "
            f"--agent {agent_safe} --status completed --confidence medium --next-owner nexus "
            f"--evidence-ref {default_evidence}"
        ),
        "```",
        "",
        "Nexus pre-summary gate (wait for stable results + validate contracts):",
        "```bash",
        f"python3 {root / 'scripts' / 'phase2_pilot.py'} pre-summary-gate --ticket {ticket_id}",
        "```",
    ]
    return "\n".join(lines) + "\n"


def upsert_dispatch_block(task_content: str, block: str) -> str:
    start_marker = "<!-- PHASE2_DISPATCH_BLOCK_START -->"
    end_marker = "<!-- PHASE2_DISPATCH_BLOCK_END -->"
    wrapped = f"{start_marker}\n{block}{end_marker}\n"

    if start_marker in task_content and end_marker in task_content:
        pattern = re.compile(
            rf"{re.escape(start_marker)}.*?{re.escape(end_marker)}\n?",
            re.DOTALL,
        )
        return pattern.sub(wrapped, task_content)

    if task_content and not task_content.endswith("\n"):
        task_content += "\n"
    if task_content:
        task_content += "\n"
    return task_content + wrapped


def resolve_run_ticket(
    root: Path, run_id: str | None, ticket_id: str | None
) -> tuple[str, str]:
    registry_path = root / "shared" / "runs" / "active-pilot-runs.json"
    registry = ensure_json_file(registry_path, {"updated_at": utc_now(), "tickets": {}})

    if run_id and ticket_id:
        return run_id, ticket_id

    if ticket_id and not run_id:
        ticket_entry = registry.get("tickets", {}).get(ticket_id)
        if not ticket_entry:
            raise SystemExit(
                f"No active pilot run registered for ticket {ticket_id}. "
                "Run init first."
            )
        return str(ticket_entry["active_run_id"]), ticket_id

    if run_id and not ticket_id:
        for tid, entry in registry.get("tickets", {}).items():
            if entry.get("active_run_id") == run_id:
                return run_id, tid
        raise SystemExit(
            f"Run ID {run_id} is not registered in active-pilot-runs.json. "
            "Provide --ticket as well."
        )

    raise SystemExit("Provide --ticket or --run-id.")


def find_active_run_for_ticket(root: Path, ticket_id: str) -> str | None:
    registry_path = root / "shared" / "runs" / "active-pilot-runs.json"
    registry = ensure_json_file(registry_path, {"updated_at": utc_now(), "tickets": {}})
    entry = registry.get("tickets", {}).get(ticket_id)
    if not entry:
        return None
    active = entry.get("active_run_id")
    if not active:
        return None
    return str(active)


def init_run(
    root: Path,
    ticket_id: str,
    project: str,
    task_file_explicit: str | None,
    run_id_explicit: str | None,
    sync_legacy: bool,
) -> tuple[str, Path | None]:
    shared_dir = root / "shared"
    runs_dir = shared_dir / "runs"
    sessions_registry = shared_dir / "sessions" / "registry.json"

    run_id = run_id_explicit.strip() if run_id_explicit else next_run_id(runs_dir, ticket_id)
    run_dir = runs_dir / run_id

    legacy_tasks_dir = root / "workspace" / "shared" / "tasks"
    legacy_results_dir = root / "workspace" / "shared" / "test-results" / ticket_id
    legacy_results_dir.mkdir(parents=True, exist_ok=True)

    task_file = choose_task_file(legacy_tasks_dir, ticket_id, task_file_explicit)

    for rel in (
        "intake",
        "plan",
        "handoffs",
        "sessions",
        "evidence/ui",
        "evidence/api",
        "evidence/legacy-mirror",
        "results",
        "learning",
        "meta",
    ):
        (run_dir / rel).mkdir(parents=True, exist_ok=True)

    manifest = build_manifest(
        root=root,
        ticket_id=ticket_id,
        run_id=run_id,
        project=project,
        legacy_task_file=task_file,
        legacy_results_dir=legacy_results_dir,
    )
    save_json(run_dir / "meta" / "run-manifest.json", manifest)

    if task_file:
        shutil.copy2(task_file, run_dir / "plan" / "task-source.md")

    charter = build_task_charter(ticket_id, run_id, project)
    save_json(run_dir / "plan" / "task-charter.json", charter)

    state_ref = rel_path(root, run_dir / "plan" / "task-charter.json")
    handoff_clawver = build_handoff(
        run_id=run_id,
        receiver="qa-agent",
        state_ref=state_ref,
        expected_next_step="Execute UI flow and write result packet + evidence.",
        notes=[
            "Pilot dual-write mode is active.",
            "Keep writing legacy evidence path and sync to run folder.",
        ],
    )
    save_json(run_dir / "handoffs" / "nexus-to-clawver.json", handoff_clawver)

    handoff_cipher = build_handoff(
        run_id=run_id,
        receiver="api-docs-agent",
        state_ref=state_ref,
        expected_next_step="Execute API checks/data prep and write result packet + evidence.",
        notes=[
            "Pilot dual-write mode is active.",
            "Keep writing legacy evidence path and sync to run folder.",
        ],
    )
    save_json(run_dir / "handoffs" / "nexus-to-cipher.json", handoff_cipher)

    exported = export_run_contracts_to_legacy(run_dir, legacy_results_dir)

    run_marker = (
        f"run_id={run_id}\n"
        f"run_path={run_dir}\n"
        "mode=phase2-dual-write-pilot\n"
        f"updated_at={utc_now()}\n"
    )
    (legacy_results_dir / "RUN_ID.txt").write_text(run_marker, encoding="utf-8")

    update_active_pilot_registry(
        registry_path=runs_dir / "active-pilot-runs.json",
        ticket_id=ticket_id,
        run_id=run_id,
        legacy_results_dir=legacy_results_dir,
        task_file=task_file,
        root=root,
    )
    ensure_sessions_registry(sessions_registry, run_id)

    sync_report = None
    if sync_legacy:
        copied, skipped, sync_report = sync_legacy_into_run(root, run_id, ticket_id)
        print(f"[sync] mirrored legacy evidence: copied={copied}, skipped={skipped}")

    print(f"[init] ticket={ticket_id}")
    print(f"[init] run_id={run_id}")
    print(f"[init] run_dir={run_dir}")
    print(f"[init] legacy_results={legacy_results_dir}")
    if task_file:
        print(f"[init] task_file={task_file}")
    print(f"[init] contracts exported to legacy={len(exported)}")
    if sync_report:
        print(f"[init] sync_report={sync_report}")

    return run_id, task_file


def cmd_init(args: argparse.Namespace) -> int:
    root = repo_root()
    ticket_id = args.ticket.strip()
    init_run(
        root=root,
        ticket_id=ticket_id,
        project=args.project,
        task_file_explicit=args.task_file,
        run_id_explicit=args.run_id,
        sync_legacy=args.sync_legacy,
    )
    return 0


def sync_legacy_into_run(root: Path, run_id: str, ticket_id: str) -> tuple[int, int, Path]:
    run_dir = root / "shared" / "runs" / run_id
    if not run_dir.exists():
        raise SystemExit(f"Run directory does not exist: {run_dir}")

    legacy_results_dir = root / "workspace" / "shared" / "test-results" / ticket_id
    if not legacy_results_dir.exists():
        raise SystemExit(f"Legacy results directory does not exist: {legacy_results_dir}")

    mirror_dir = run_dir / "evidence" / "legacy-mirror"
    copied, skipped = copy_tree_incremental(legacy_results_dir, mirror_dir)
    exported = export_run_contracts_to_legacy(run_dir, legacy_results_dir)

    report = {
        "run_id": run_id,
        "ticket_id": ticket_id,
        "timestamp": utc_now(),
        "legacy_results_ref": rel_path(root, legacy_results_dir),
        "run_mirror_ref": rel_path(root, mirror_dir),
        "files_copied": copied,
        "files_skipped": skipped,
        "contracts_exported_count": len(exported),
    }
    report_path = run_dir / "meta" / "legacy-sync-report.json"
    save_json(report_path, report)
    save_json(legacy_results_dir / "contracts" / "last-sync-report.json", report)
    return copied, skipped, report_path


def cmd_sync_legacy(args: argparse.Namespace) -> int:
    root = repo_root()
    run_id, ticket_id = resolve_run_ticket(root, args.run_id, args.ticket)
    copied, skipped, report_path = sync_legacy_into_run(root, run_id, ticket_id)
    print(f"[sync] ticket={ticket_id}")
    print(f"[sync] run_id={run_id}")
    print(f"[sync] copied={copied} skipped={skipped}")
    print(f"[sync] report={report_path}")
    return 0


def cmd_register_session(args: argparse.Namespace) -> int:
    root = repo_root()
    run_id, ticket_id = resolve_run_ticket(root, args.run_id, args.ticket)

    run_dir = root / "shared" / "runs" / run_id
    if not run_dir.exists():
        raise SystemExit(f"Run directory does not exist: {run_dir}")

    session_id, session_path = register_session_record(
        root=root,
        run_id=run_id,
        project=args.project,
        subject_type=args.subject_type,
        owner=args.owner,
        storage_state_ref=args.storage_state_ref,
        token_ref=args.token_ref,
        status=args.status,
        refresh_strategy=args.refresh_strategy,
        expires_at=args.expires_at,
        session_id=args.session_id,
    )

    legacy_results_dir = root / "workspace" / "shared" / "test-results" / ticket_id
    export_run_contracts_to_legacy(run_dir, legacy_results_dir)

    print(f"[session] ticket={ticket_id}")
    print(f"[session] run_id={run_id}")
    print(f"[session] session_id={session_id}")
    print(f"[session] record={session_path}")
    return 0


def cmd_emit_result(args: argparse.Namespace) -> int:
    root = repo_root()
    run_id, ticket_id = resolve_run_ticket(root, args.run_id, args.ticket)
    run_dir = root / "shared" / "runs" / run_id
    if not run_dir.exists():
        raise SystemExit(f"Run directory does not exist: {run_dir}")

    out_path = write_result_packet(
        root=root,
        run_id=run_id,
        agent=args.agent,
        status=args.status,
        assertions_passed=args.assertion_passed or [],
        assertions_failed=args.assertion_failed or [],
        blockers=args.blocker or [],
        evidence_refs=args.evidence_ref or [],
        confidence=args.confidence,
        recommended_next_owner=args.next_owner,
        notes=args.note or [],
    )

    legacy_results_dir = root / "workspace" / "shared" / "test-results" / ticket_id
    export_run_contracts_to_legacy(run_dir, legacy_results_dir)

    print(f"[result] ticket={ticket_id}")
    print(f"[result] run_id={run_id}")
    print(f"[result] packet={out_path}")
    return 0


def prepare_dispatch_for_agent(
    root: Path,
    run_id: str,
    ticket_id: str,
    agent: str,
    task_file_raw: str,
) -> Path:
    if agent not in ("qa-agent", "api-docs-agent"):
        raise SystemExit("Unsupported agent. Use qa-agent or api-docs-agent.")

    task_file = Path(task_file_raw).expanduser()
    if not task_file.is_absolute():
        task_file = root / task_file
    task_file.parent.mkdir(parents=True, exist_ok=True)

    if task_file.exists():
        content = task_file.read_text(encoding="utf-8")
    else:
        content = f"# Task: {ticket_id}\n\n"

    dispatch_block = build_dispatch_block(root=root, ticket_id=ticket_id, run_id=run_id, agent=agent)
    updated = upsert_dispatch_block(content, dispatch_block)
    task_file.write_text(updated, encoding="utf-8")
    return task_file


def wait_for_result_file(
    result_file: Path,
    timeout_sec: int,
    poll_sec: float,
    stable_polls: int,
) -> tuple[bool, dict]:
    start = time.monotonic()
    attempts = 0
    same_signature_hits = 0
    last_signature: tuple[int, int] | None = None
    last_seen_at: str | None = None

    while (time.monotonic() - start) <= timeout_sec:
        attempts += 1
        if result_file.exists() and result_file.is_file():
            stat = result_file.stat()
            signature = (stat.st_size, int(stat.st_mtime))
            last_seen_at = dt.datetime.fromtimestamp(stat.st_mtime, tz=dt.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            )

            if signature == last_signature:
                same_signature_hits += 1
            else:
                last_signature = signature
                same_signature_hits = 1

            if same_signature_hits >= stable_polls:
                elapsed = round(time.monotonic() - start, 3)
                return True, {
                    "result_file": str(result_file),
                    "elapsed_sec": elapsed,
                    "attempts": attempts,
                    "size_bytes": signature[0],
                    "mtime_utc": last_seen_at,
                }

        time.sleep(poll_sec)

    elapsed = round(time.monotonic() - start, 3)
    return False, {
        "result_file": str(result_file),
        "elapsed_sec": elapsed,
        "attempts": attempts,
        "last_seen_mtime_utc": last_seen_at,
    }


def ajv_validate_file(schema_path: Path, data_path: Path) -> tuple[bool, str]:
    cmd = [
        "npx",
        "--yes",
        "ajv-cli",
        "validate",
        "-s",
        str(schema_path),
        "-d",
        str(data_path),
    ]
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=False,
        )
    except FileNotFoundError:
        return False, "npx not found; install Node.js to run contract validation."
    output = (proc.stdout or "").strip()
    error = (proc.stderr or "").strip()
    details = error or output or f"exit_code={proc.returncode}"
    return proc.returncode == 0, details


def validate_run_contracts(root: Path, run_id: str) -> dict:
    run_dir = root / "shared" / "runs" / run_id
    result_schema = root / "contracts" / "result-packet.schema.json"
    session_schema = root / "contracts" / "session-record.schema.json"

    result_files = sorted((run_dir / "results").glob("*.json"))
    session_files = sorted((run_dir / "sessions").glob("*.json"))

    result_validation = {
        "required_min_files": 1,
        "found": len(result_files),
        "valid": 0,
        "invalid": [],
    }
    session_validation = {
        "found": len(session_files),
        "valid": 0,
        "invalid": [],
        "skipped": len(session_files) == 0,
    }

    for result_file in result_files:
        is_valid, details = ajv_validate_file(result_schema, result_file)
        if is_valid:
            result_validation["valid"] += 1
        else:
            result_validation["invalid"].append(
                {
                    "file": str(result_file),
                    "error": details,
                }
            )

    for session_file in session_files:
        is_valid, details = ajv_validate_file(session_schema, session_file)
        if is_valid:
            session_validation["valid"] += 1
        else:
            session_validation["invalid"].append(
                {
                    "file": str(session_file),
                    "error": details,
                }
            )

    result_ok = (
        result_validation["found"] >= result_validation["required_min_files"]
        and len(result_validation["invalid"]) == 0
    )
    session_ok = len(session_validation["invalid"]) == 0

    return {
        "tool": "ajv-cli",
        "result_packets": result_validation,
        "session_records": session_validation,
        "ok": result_ok and session_ok,
    }


def cmd_pre_summary_gate(args: argparse.Namespace) -> int:
    root = repo_root()
    run_id, ticket_id = resolve_run_ticket(root, args.run_id, args.ticket)

    registry_path = root / "shared" / "runs" / "active-pilot-runs.json"
    registry = ensure_json_file(registry_path, {"updated_at": utc_now(), "tickets": {}})
    ticket_entry = registry.get("tickets", {}).get(ticket_id, {})

    if args.result_file:
        result_file = Path(args.result_file).expanduser()
        if not result_file.is_absolute():
            result_file = root / result_file
    else:
        legacy_ref = ticket_entry.get(
            "legacy_results_ref", f"workspace/shared/test-results/{ticket_id}"
        )
        result_file = root / legacy_ref / "results.json"

    ready, result_wait = wait_for_result_file(
        result_file=result_file,
        timeout_sec=args.timeout_sec,
        poll_sec=args.poll_sec,
        stable_polls=args.stable_polls,
    )

    sync_report_ref = None
    contracts = None
    copied = 0
    skipped = 0
    if ready:
        copied, skipped, sync_report = sync_legacy_into_run(root, run_id, ticket_id)
        sync_report_ref = rel_path(root, sync_report)
        contracts = validate_run_contracts(root, run_id)

    status = "ready" if (ready and contracts and contracts.get("ok")) else "partial"
    report = {
        "ticket_id": ticket_id,
        "run_id": run_id,
        "generated_at": utc_now(),
        "status": status,
        "result_ready": ready,
        "result_wait": result_wait,
        "sync": {
            "copied": copied,
            "skipped": skipped,
            "report_ref": sync_report_ref,
        },
        "contracts": contracts,
    }
    if not ready:
        report["reason"] = "result_file_not_ready"
    elif contracts and not contracts.get("ok"):
        report["reason"] = "contract_validation_failed"

    run_report_path = root / "shared" / "runs" / run_id / "meta" / "pre-summary-gate.json"
    save_json(run_report_path, report)

    legacy_dir = root / "workspace" / "shared" / "test-results" / ticket_id / "contracts"
    save_json(legacy_dir / "pre-summary-gate.json", report)

    print(f"[gate] ticket={ticket_id}")
    print(f"[gate] run_id={run_id}")
    print(f"[gate] status={status}")
    print(f"[gate] result_ready={ready}")
    print(f"[gate] report={run_report_path}")
    if report.get("reason"):
        print(f"[gate] reason={report['reason']}")
    return 0 if status == "ready" else 2


def cmd_bootstrap_dispatch(args: argparse.Namespace) -> int:
    root = repo_root()
    ticket_id = args.ticket.strip()

    run_id = find_active_run_for_ticket(root, ticket_id)
    if not run_id:
        run_id, _ = init_run(
            root=root,
            ticket_id=ticket_id,
            project=args.project,
            task_file_explicit=args.task_file,
            run_id_explicit=args.run_id,
            sync_legacy=args.sync_legacy,
        )

    agents = args.agent or ["qa-agent"]
    for agent in agents:
        task_file = prepare_dispatch_for_agent(
            root=root,
            run_id=run_id,
            ticket_id=ticket_id,
            agent=agent,
            task_file_raw=args.task_file,
        )
        print(f"[bootstrap] ticket={ticket_id} run_id={run_id} agent={agent} task_file={task_file}")

    return 0


def cmd_prepare_dispatch(args: argparse.Namespace) -> int:
    root = repo_root()
    run_id, ticket_id = resolve_run_ticket(root, args.run_id, args.ticket)
    task_file = prepare_dispatch_for_agent(
        root=root,
        run_id=run_id,
        ticket_id=ticket_id,
        agent=args.agent,
        task_file_raw=args.task_file,
    )

    print(f"[dispatch] ticket={ticket_id}")
    print(f"[dispatch] run_id={run_id}")
    print(f"[dispatch] agent={args.agent}")
    print(f"[dispatch] task_file={task_file}")
    return 0


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Phase 2 pilot helper for dual-write run-centric migration."
    )
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser(
        "init", help="Initialize pilot run folder and dual-write metadata for a ticket."
    )
    init_cmd.add_argument("--ticket", required=True, help="Ticket key (e.g. CT-901).")
    init_cmd.add_argument("--project", default="minebit", help="Project slug.")
    init_cmd.add_argument(
        "--task-file",
        default=None,
        help="Optional explicit path to legacy task file.",
    )
    init_cmd.add_argument(
        "--run-id",
        default=None,
        help="Optional explicit run_id. If omitted, generated automatically.",
    )
    init_cmd.add_argument(
        "--sync-legacy",
        action="store_true",
        help="After init, mirror current legacy evidence into run folder.",
    )

    sync_cmd = sub.add_parser(
        "sync-legacy",
        help="Mirror legacy test-results/<ticket> into shared/runs/<run_id>/evidence/legacy-mirror.",
    )
    sync_cmd.add_argument("--ticket", default=None, help="Ticket key (e.g. CT-901).")
    sync_cmd.add_argument("--run-id", default=None, help="Run ID (e.g. CT-901-YYYYMMDD-01).")

    session_cmd = sub.add_parser(
        "register-session",
        help="Create session-record in shared/sessions and run/sessions (no raw token in prose).",
    )
    session_cmd.add_argument("--ticket", default=None, help="Ticket key (e.g. CT-901).")
    session_cmd.add_argument("--run-id", default=None, help="Run ID.")
    session_cmd.add_argument("--project", default="minebit", help="Project slug.")
    session_cmd.add_argument(
        "--subject-type",
        required=True,
        choices=["player", "admin", "service", "api"],
        help="Session subject type.",
    )
    session_cmd.add_argument("--owner", required=True, help="Session owner (qa-agent/api-docs-agent).")
    session_cmd.add_argument(
        "--storage-state-ref",
        required=True,
        help="Path/ref to storage state JSON (relative ref preferred).",
    )
    session_cmd.add_argument(
        "--token-ref",
        required=True,
        help="Path/ref to token artifact file (relative ref preferred).",
    )
    session_cmd.add_argument(
        "--status",
        default="active",
        choices=["active", "expired", "revoked", "invalid", "pending"],
        help="Session status.",
    )
    session_cmd.add_argument(
        "--refresh-strategy",
        default="manual",
        choices=["ui_login", "api_refresh", "manual", "not_applicable"],
        help="Session refresh strategy.",
    )
    session_cmd.add_argument(
        "--expires-at",
        default=None,
        help="Optional expiry in UTC format YYYY-MM-DDTHH:MM:SSZ.",
    )
    session_cmd.add_argument(
        "--session-id",
        default=None,
        help="Optional explicit session id. If omitted, auto-generated.",
    )

    result_cmd = sub.add_parser(
        "emit-result",
        help="Write result-packet into run/results and export contracts to legacy.",
    )
    result_cmd.add_argument("--ticket", default=None, help="Ticket key (e.g. CT-901).")
    result_cmd.add_argument("--run-id", default=None, help="Run ID.")
    result_cmd.add_argument("--agent", required=True, help="Agent id (qa-agent/api-docs-agent/nexus).")
    result_cmd.add_argument(
        "--status",
        required=True,
        choices=["completed", "partial", "blocked", "failed"],
        help="Result status.",
    )
    result_cmd.add_argument(
        "--confidence",
        required=True,
        choices=["low", "medium", "high"],
        help="Result confidence.",
    )
    result_cmd.add_argument(
        "--next-owner",
        required=True,
        help="Recommended next owner.",
    )
    result_cmd.add_argument(
        "--assertion-passed",
        action="append",
        default=[],
        help="Passed assertion (repeatable).",
    )
    result_cmd.add_argument(
        "--assertion-failed",
        action="append",
        default=[],
        help="Failed assertion (repeatable).",
    )
    result_cmd.add_argument(
        "--blocker",
        action="append",
        default=[],
        help="Blocker text (repeatable).",
    )
    result_cmd.add_argument(
        "--evidence-ref",
        action="append",
        default=[],
        help="Evidence path/ref (repeatable).",
    )
    result_cmd.add_argument(
        "--note",
        action="append",
        default=[],
        help="Optional note (repeatable).",
    )

    dispatch_cmd = sub.add_parser(
        "prepare-dispatch",
        help="Insert/update Phase 2 dispatch hook block in a task markdown file.",
    )
    dispatch_cmd.add_argument("--ticket", default=None, help="Ticket key (e.g. CT-901).")
    dispatch_cmd.add_argument("--run-id", default=None, help="Run ID.")
    dispatch_cmd.add_argument(
        "--agent",
        required=True,
        choices=["qa-agent", "api-docs-agent"],
        help="Target executor agent.",
    )
    dispatch_cmd.add_argument(
        "--task-file",
        required=True,
        help="Path to task markdown file (absolute or repo-relative).",
    )

    bootstrap_cmd = sub.add_parser(
        "bootstrap-dispatch",
        help="Ensure pilot init exists for ticket and upsert dispatch hooks for selected agents.",
    )
    bootstrap_cmd.add_argument("--ticket", required=True, help="Ticket key (e.g. CT-901).")
    bootstrap_cmd.add_argument("--project", default="minebit", help="Project slug for init if needed.")
    bootstrap_cmd.add_argument(
        "--task-file",
        required=True,
        help="Path to task markdown file (absolute or repo-relative).",
    )
    bootstrap_cmd.add_argument("--run-id", default=None, help="Optional explicit run_id if init is needed.")
    bootstrap_cmd.add_argument(
        "--sync-legacy",
        action="store_true",
        help="When init is performed, mirror current legacy evidence immediately.",
    )
    bootstrap_cmd.add_argument(
        "--agent",
        action="append",
        choices=["qa-agent", "api-docs-agent"],
        default=[],
        help="Agent to inject dispatch block for (repeatable). Defaults to qa-agent.",
    )

    gate_cmd = sub.add_parser(
        "pre-summary-gate",
        help="Wait for legacy results.json, sync legacy mirror, validate run contracts before summary.",
    )
    gate_cmd.add_argument("--ticket", default=None, help="Ticket key (e.g. CT-901).")
    gate_cmd.add_argument("--run-id", default=None, help="Run ID.")
    gate_cmd.add_argument(
        "--result-file",
        default=None,
        help="Optional explicit result file path to wait for.",
    )
    gate_cmd.add_argument(
        "--timeout-sec",
        type=int,
        default=180,
        help="Max wait time for results.json readiness.",
    )
    gate_cmd.add_argument(
        "--poll-sec",
        type=float,
        default=2.0,
        help="Polling interval while waiting for results.json.",
    )
    gate_cmd.add_argument(
        "--stable-polls",
        type=int,
        default=2,
        help="How many consecutive identical size+mtime polls are required.",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.command == "init":
        return cmd_init(args)
    if args.command == "sync-legacy":
        return cmd_sync_legacy(args)
    if args.command == "register-session":
        return cmd_register_session(args)
    if args.command == "emit-result":
        return cmd_emit_result(args)
    if args.command == "prepare-dispatch":
        return cmd_prepare_dispatch(args)
    if args.command == "bootstrap-dispatch":
        return cmd_bootstrap_dispatch(args)
    if args.command == "pre-summary-gate":
        return cmd_pre_summary_gate(args)
    raise SystemExit(f"Unknown command: {args.command}")


if __name__ == "__main__":
    raise SystemExit(main())
