"""F42: render an explicit or anchored intermittent-monitoring calendar."""
from __future__ import annotations
import argparse
import calendar
from datetime import date
import json
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.patches import Rectangle, Patch
import pandas as pd

KINDS = {"3_day", "6_day"}
_fonts = {font.name for font in font_manager.fontManager.ttflist}
plt.rcParams["font.family"] = next((name for name in
    ["Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "DejaVu Sans"] if name in _fonts), "DejaVu Sans")
plt.rcParams["axes.unicode_minus"] = False


def parse_date(raw: object) -> date:
    try:
        return date.fromisoformat(str(raw))
    except (TypeError, ValueError) as exc:
        raise ValueError(f"Expected exact ISO date YYYY-MM-DD, got {raw!r}") from exc


def dates_from_file(path: Path, year: int) -> set[tuple[date, str]]:
    frame = pd.read_csv(path, dtype=str)
    if not {"date", "schedule"}.issubset(frame):
        raise ValueError("Schedule CSV needs date,schedule")
    if frame.empty or frame[["date", "schedule"]].isna().any().any():
        raise ValueError("Schedule rows must be complete")
    out = set()
    for row in frame.itertuples(index=False):
        d, kind = parse_date(row.date), row.schedule.strip()
        if d.year != year or kind not in KINDS:
            raise ValueError("Schedule date outside year or unknown schedule")
        if (d, kind) in out:
            raise ValueError("Duplicate scheduled date and frequency")
        out.add((d, kind))
    return out


def build(year: int, *, schedule_file: Path | None = None,
          anchor_3: str | None = None, anchor_6: str | None = None,
          observed_file: Path | None = None) -> pd.DataFrame:
    if not 1800 <= year <= 2200:
        raise ValueError("year out of supported range")
    if schedule_file and (anchor_3 or anchor_6):
        raise ValueError("Choose schedule CSV or explicit anchors")
    if not schedule_file and not (anchor_3 or anchor_6):
        raise ValueError("Supply schedule CSV or at least one anchor")
    days = pd.date_range(f"{year}-01-01", f"{year}-12-31", freq="D")
    if schedule_file:
        scheduled = dates_from_file(schedule_file, year)
    else:
        scheduled = set()
        for kind, raw, period in [("3_day", anchor_3, 3), ("6_day", anchor_6, 6)]:
            if raw:
                anchor = parse_date(raw)
                scheduled.update((d.date(), kind) for d in days if (d.date()-anchor).days % period == 0)
    observed = dates_from_file(observed_file, year) if observed_file else set()
    rows = []
    for ts in days:
        d = ts.date()
        for kind in sorted(KINDS):
            rows.append({"date": d.isoformat(), "schedule": kind,
                         "scheduled": int((d, kind) in scheduled),
                         "observed": int((d, kind) in observed)})
    return pd.DataFrame(rows)


def render(checked: pd.DataFrame, prefix: Path, title: str | None) -> None:
    year = int(checked.date.iloc[0][:4])
    lookup = {(parse_date(r.date), r.schedule): (r.scheduled, r.observed)
              for r in checked.itertuples(index=False)}
    fig, axes = plt.subplots(4, 3, figsize=(12.3, 12), squeeze=False)
    cal = calendar.Calendar(firstweekday=6)  # Sunday first, as in source.
    for month, ax in enumerate(axes.flat, start=1):
        ax.set_xlim(-.5, 6.5)
        ax.set_ylim(6.6, -.85)
        ax.set_xticks(range(7), ["Su", "M", "Tu", "W", "Th", "F", "Sa"])
        ax.xaxis.tick_top()
        ax.set_yticks([])
        ax.set_title(calendar.month_name[month], fontsize=12, pad=17)
        for row, week in enumerate(cal.monthdayscalendar(year, month)):
            for col, day in enumerate(week):
                if not day:
                    continue
                d = date(year, month, day)
                three = lookup[(d, "3_day")]
                six = lookup[(d, "6_day")]
                if three[0] or six[0]:
                    ax.add_patch(Rectangle((col-.42, row-.42), .84, .84,
                        facecolor="#C5E5EE" if three[0] else "white",
                        edgecolor="#222222" if six[0] else "none", linewidth=1.2))
                ax.text(col, row, str(day), ha="center", va="center", fontsize=9)
                if three[1] or six[1]:
                    ax.plot(col+.32, row-.31, marker="o", color="#D55E00", ms=3.4)
        ax.spines[["top", "right", "bottom", "left"]].set_color("#777777")
    fig.legend(handles=[Patch(facecolor="#C5E5EE", label="Scheduled every 3 days"),
        Patch(facecolor="white", edgecolor="#222222", label="Scheduled every 6 days"),
        plt.Line2D([], [], marker="o", linestyle="", color="#D55E00", label="Observed")],
        loc="lower center", ncol=3, frameon=False, bbox_to_anchor=(.5, .005))
    if title:
        fig.suptitle(title, fontsize=14)
    fig.tight_layout(rect=(0, .04, 1, .98))
    prefix.parent.mkdir(parents=True, exist_ok=True)
    for ext in ("png", "pdf"):
        fig.savefig(prefix.with_suffix("."+ext), dpi=300, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--year", type=int, required=True)
    ap.add_argument("--schedule", type=Path)
    ap.add_argument("--anchor-3")
    ap.add_argument("--anchor-6")
    ap.add_argument("--observed", type=Path)
    ap.add_argument("--output-prefix", type=Path, required=True)
    ap.add_argument("--title")
    a = ap.parse_args()
    checked = build(a.year, schedule_file=a.schedule, anchor_3=a.anchor_3,
                    anchor_6=a.anchor_6, observed_file=a.observed)
    render(checked, a.output_prefix, a.title)
    checked.to_csv(a.output_prefix.with_name(a.output_prefix.name+"_checked.csv"), index=False)
    print(json.dumps({"status": "OK", "year": a.year, "days": len(checked)//2,
        "scheduled_3": int(checked.query("schedule == '3_day'").scheduled.sum()),
        "scheduled_6": int(checked.query("schedule == '6_day'").scheduled.sum()),
        "observed": int(checked.observed.sum()), "output": str(a.output_prefix)}))


if __name__ == "__main__":
    main()
