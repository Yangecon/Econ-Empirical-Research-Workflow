"""Shared ordered-path drawing, with no statistical transformations."""
from __future__ import annotations

import numpy as np


def draw_trace(ax, x, y, *, kind="line", color="#0173B2", linestyle="-",
               linewidth=2.0, marker=None, markersize=3.5, label=None,
               zorder=2, lower=None, upper=None, band_alpha=.12):
    """Draw supplied coordinates in their existing order; NaNs remain line breaks.

    `step` is right-continuous. CI arrays, when provided, are already computed
    upstream and are never estimated or reinterpreted here.
    """
    if kind not in ("line", "step"):
        raise ValueError("kind must be line or step")
    if len(x) != len(y):
        raise ValueError("x and y lengths differ")
    if (lower is None) != (upper is None):
        raise ValueError("Both lower and upper bands must be supplied together")
    if lower is not None and (len(lower) != len(y) or len(upper) != len(y)):
        raise ValueError("Band and y lengths differ")
    kw = dict(color=color, linestyle=linestyle, linewidth=linewidth,
              marker=marker, markersize=markersize, label=label, zorder=zorder)
    if kind == "line":
        artist, = ax.plot(x, y, **kw)
    else:
        artist, = ax.step(x, y, where="post", **kw)
    if lower is not None:
        lo, hi = np.asarray(lower, dtype=float), np.asarray(upper, dtype=float)
        if not np.isfinite(lo).all() or not np.isfinite(hi).all() or (lo > hi).any():
            raise ValueError("Band endpoints must be finite and ordered")
        ax.fill_between(x, lo, hi, step="post" if kind == "step" else None,
                        color=color, alpha=band_alpha, zorder=zorder-1)
    return artist
