"""Two-panel binned RD display; bins and local linear fits use underlying rows."""
from __future__ import annotations
import argparse
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties, findfont

# Edit these IDs, labels and within-panel windows for another two-outcome study.
PANELS = (
    {"id": "outcome_a", "en": "(A) Outcome A", "zh": "（A）结果 A", "bandwidth": 16.0,
     "ymin": -.008, "ymax": .26, "bins_per_side": 10},
    {"id": "outcome_b", "en": "(B) Outcome B", "zh": "（B）结果 B", "bandwidth": 25.0,
     "ymin": -.008, "ymax": .26, "bins_per_side": 10},
)
TEXT = {"en": {"x": "Running variable relative to cutoff", "y": "Outcome probability", "title": "Binned outcomes around a cutoff"},
        "zh": {"x": "相对断点的运行变量", "y": "结果发生概率", "title": "断点两侧的分箱结果"}}

def bin_index(x: np.ndarray, side: str, bandwidth: float, nbins: int) -> np.ndarray:
    """Equal-width bins: -bw is left bin 1, zero is right bin 1, +bw right bin B."""
    width = bandwidth / nbins
    raw = (x + bandwidth)/width if side == "left" else x/width
    return np.minimum(np.floor(raw).astype(int), nbins-1) + 1

def font(lang: str) -> None:
    if lang == "zh":
        for family in ("Microsoft YaHei", "SimHei", "Noto Sans CJK SC", "Source Han Sans SC"):
            try:
                findfont(FontProperties(family=family), fallback_to_default=False)
                plt.rcParams["font.family"] = family
                break
            except ValueError:
                continue
        else:
            raise RuntimeError("A Chinese font is required")
    else:
        plt.rcParams["font.family"] = "DejaVu Sans"
    plt.rcParams["axes.unicode_minus"] = False

def calculate(path: Path | pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    df = (path.copy() if isinstance(path, pd.DataFrame) else
          pd.read_csv(path, dtype={"panel": str, "id": str}, encoding="utf-8-sig"))
    need = {"panel", "id", "running", "outcome"}
    if not need.issubset(df):
        raise ValueError(f"required columns: {sorted(need)}")
    if df[list(need)].isna().any().any() or df.id.eq("").any() or df.panel.eq("").any():
        raise ValueError("required values must be nonmissing")
    if set(df.panel) != {p["id"] for p in PANELS} or df.duplicated(["panel", "id"]).any():
        raise ValueError("configured panel IDs and unique within-panel IDs required")
    for col in ("running", "outcome"):
        df[col] = pd.to_numeric(df[col], errors="raise")
        if not np.isfinite(df[col]).all():
            raise ValueError(f"{col} must be finite")
    if not df.outcome.between(0, 1).all():
        raise ValueError("outcome must be a probability/binary rate on [0,1]")
    bin_rows, fit_rows, sample_rows = [], [], []
    for cfg in PANELS:
        panel = cfg["id"]
        original = df[df.panel == panel]
        bw, nb = cfg["bandwidth"], cfg["bins_per_side"]
        if not (bw > 0 and isinstance(nb, int) and nb >= 3):
            raise ValueError("positive bandwidth and >=3 bins per side required")
        work = original[original.running.abs() <= bw].copy()
        work["side"] = np.where(work.running < 0, "left", "right")
        if len(work) < 2*nb*3:
            raise ValueError(f"{panel}: insufficient observations in bandwidth")
        for side in ("left", "right"):
            part = work[work.side == side].copy()
            if len(part) < nb*3 or part.running.nunique() < 2:
                raise ValueError(f"{panel}/{side}: need >=3 per bin on average and varying x")
            part["bin"] = bin_index(part.running.to_numpy(), side, bw, nb)
            assert part.bin.between(1, nb).all()
            means = part.groupby("bin", sort=True).agg(x_mean=("running", "mean"),
                                                      y_mean=("outcome", "mean"), n=("outcome", "size")).reset_index()
            if len(means) != nb or (means.n < 2).any():
                raise ValueError(f"{panel}/{side}: each equal-width bin needs >=2 observations")
            means.insert(0, "side", side); means.insert(0, "panel", panel)
            bin_rows.append(means)
            design = np.column_stack([np.ones(len(part)), part.running.to_numpy()])
            intercept, slope = np.linalg.lstsq(design, part.outcome.to_numpy(), rcond=None)[0]
            endpoints = np.array([-bw, 0]) if side == "left" else np.array([0, bw])
            if not means.y_mean.between(cfg["ymin"], cfg["ymax"]).all() or not np.all(
                (intercept+slope*endpoints >= cfg["ymin"]) & (intercept+slope*endpoints <= cfg["ymax"])
            ):
                raise ValueError(f"{panel}/{side}: bins or fit exceed configured display y range; edit panel limits")
            fit_rows.append({"panel": panel, "side": side, "n": len(part),
                             "intercept_at_cutoff": intercept, "slope": slope,
                             "fit_x_min": -bw if side == "left" else 0,
                             "fit_x_max": 0 if side == "left" else bw})
        sample_rows.append({"panel": panel, "total_input_n": len(original), "window_n": len(work),
                            "excluded_outside_bandwidth_n": len(original)-len(work), "cutoff_zero_n": int((work.running == 0).sum())})
    return (pd.concat(bin_rows, ignore_index=True), pd.DataFrame(fit_rows), pd.DataFrame(sample_rows))

def draw(bins: pd.DataFrame, fits: pd.DataFrame, output: Path, lang: str, title: bool) -> None:
    font(lang)
    fig, axes = plt.subplots(2, 1, figsize=(7.4, 8.8), dpi=160)
    for ax, cfg in zip(axes, PANELS):
        panel, bw = cfg["id"], cfg["bandwidth"]
        for side in ("left", "right"):
            b = bins[(bins.panel == panel) & (bins.side == side)]
            fit = fits[(fits.panel == panel) & (fits.side == side)].iloc[0]
            ax.scatter(b.x_mean, b.y_mean, s=25, color="#9b9b9b", zorder=3)
            x = np.array([fit.fit_x_min, fit.fit_x_max])
            ax.plot(x, fit.intercept_at_cutoff + fit.slope*x, color="#171717", linewidth=1.25)
        ax.axvline(0, color="#303030", linewidth=1.1, linestyle=(0, (6, 4)))
        ax.axhline(0, color="#c65050", linewidth=.8, linestyle=(0, (6, 4)))
        ax.set_xlim(-bw, bw); ax.set_ylim(cfg["ymin"], cfg["ymax"])
        ax.set_title(cfg[lang], fontsize=13, pad=12)
        ax.set_xlabel(TEXT[lang]["x"]); ax.set_ylabel(TEXT[lang]["y"])
        ax.set_yticks(np.arange(0, cfg["ymax"]+.0001, .05))
        ax.grid(axis="y", color="#e4e9ea", linewidth=.6)
        ax.spines[["top", "right"]].set_visible(False)
    if title:
        fig.suptitle(TEXT[lang]["title"], fontsize=14, y=.995)
    fig.tight_layout(rect=(0, 0, 1, .97 if title else 1), h_pad=2)
    output.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(output, dpi=220); fig.savefig(output.with_suffix(".pdf")); plt.close(fig)

def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--input", type=Path, required=True)
    p.add_argument("--output", type=Path, required=True)
    p.add_argument("--lang", choices=TEXT, default="en")
    p.add_argument("--title", action="store_true")
    a = p.parse_args()
    bins, fits, sample = calculate(a.input)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    stem = a.output.stem
    bins.to_csv(a.output.with_name(stem+"_bins.csv"), index=False, float_format="%.12g")
    fits.to_csv(a.output.with_name(stem+"_fits.csv"), index=False, float_format="%.12g")
    sample.to_csv(a.output.with_name(stem+"_sample.csv"), index=False)
    draw(bins, fits, a.output, a.lang, a.title)
    print(f"PYTHON_COMPLETE input_rows={sum(sample.total_input_n)} window_rows={sum(sample.window_n)} bins={len(bins)} fits={len(fits)} output={a.output}")

if __name__ == "__main__":
    main()
