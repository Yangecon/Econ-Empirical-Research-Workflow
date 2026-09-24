"""Read the latest Codex rate-limit snapshot from local session logs.

Only selected rate-limit fields are printed. No authentication data or chat
content is emitted. This is a cached observation, not a live server query.
"""

import argparse
import json
import os
from datetime import datetime, timezone
from pathlib import Path


def candidate_homes(explicit):
    if explicit:
        return [Path(explicit)]
    configured = os.environ.get("CODEX_HOME")
    if configured:
        return [Path(configured)]
    return [Path("C:/codex-home"), Path.home() / ".codex"]


def latest_files(home, limit=60):
    folder = home / "sessions"
    if not folder.is_dir():
        return []
    return sorted(
        folder.rglob("rollout-*.jsonl"),
        key=lambda path: path.stat().st_mtime,
        reverse=True,
    )[:limit]


def find_snapshots(paths):
    newest = {}
    for path in paths:
        try:
            with path.open(encoding="utf-8") as stream:
                for line in stream:
                    if '"rate_limits"' not in line:
                        continue
                    try:
                        event = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    payload = event.get("payload") or {}
                    if event.get("type") != "event_msg" or payload.get("type") != "token_count":
                        continue
                    limits = (payload.get("info") or {}).get("rate_limits") or payload.get("rate_limits")
                    if not isinstance(limits, dict):
                        continue
                    stamp = event.get("timestamp")
                    if not isinstance(stamp, str):
                        continue
                    key = limits.get("limit_id") or "unlabelled"
                    if key not in newest or stamp > newest[key][0]:
                        newest[key] = (stamp, limits, path)
        except OSError:
            continue
    return newest


def window_details(value):
    if not isinstance(value, dict):
        return None
    used = value.get("used_percent")
    reset = value.get("resets_at")
    result = {
        "window_minutes": value.get("window_minutes"),
        "used_percent": used,
        "remaining_percent_approx": round(100 - used, 2) if isinstance(used, (int, float)) else None,
        "resets_at_local": datetime.fromtimestamp(reset, timezone.utc).astimezone().isoformat() if isinstance(reset, (int, float)) else None,
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--home", help="Codex home directory; otherwise detect local homes")
    args = parser.parse_args()
    roots = [path for path in candidate_homes(args.home) if path.is_dir()]
    paths = [path for root in roots for path in latest_files(root)]
    snapshots = find_snapshots(paths)
    now = datetime.now(timezone.utc)
    result = {"checked_at_local": now.astimezone().isoformat(), "limits": []}
    stale = []
    for key, (stamp, limits, path) in sorted(snapshots.items()):
        try:
            observed = datetime.fromisoformat(stamp.replace("Z", "+00:00"))
        except ValueError:
            continue
        age = max(0, round((now - observed).total_seconds()))
        entry = {
            "limit_id": key,
            "observed_at_local": observed.astimezone().isoformat(),
            "age_seconds": age,
            "stale_over_15_minutes": age > 900,
            "session_file": path.name,
            "primary": window_details(limits.get("primary")),
            "secondary": window_details(limits.get("secondary")),
            "credits": limits.get("credits"),
            "plan_type": limits.get("plan_type"),
        }
        if age <= 900:
            result["limits"].append(entry)
        else:
            stale.append(entry)
    if not result["limits"] and stale:
        result["last_stale_snapshot"] = min(stale, key=lambda item: item["age_seconds"])
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["limits"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
