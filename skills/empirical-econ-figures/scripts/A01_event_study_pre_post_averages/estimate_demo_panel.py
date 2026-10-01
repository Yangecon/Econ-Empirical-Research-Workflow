"""Generate and estimate the balanced common-timing demonstration panel."""
from pathlib import Path
import argparse
import numpy as np
import pandas as pd
from scipy.stats import norm

HERE = Path(__file__).resolve().parent
SEED = 20260930
PERIODS = np.arange(-6, 8)
TERMS = ["ref" if k == -1 else f"lead{-k}" if k < 0 else f"lag{k}" for k in PERIODS]


def generate_panel() -> pd.DataFrame:
    rng = np.random.default_rng(SEED)
    assignment = np.r_[np.ones(35, dtype=int), np.zeros(35, dtype=int)]
    rng.shuffle(assignment)
    unit_effect = rng.normal(0, 0.8, 70)
    rows = []
    for unit in range(70):
        for k in PERIODS:
            effect = (0.08 + 0.02 * k) if k >= 0 else 0.0
            y = 2 + unit_effect[unit] + 0.025 * (k + 6) + 0.004 * (k + 6) ** 2
            y += assignment[unit] * effect + rng.normal(0, 0.30)
            rows.append((unit + 1, int(k), int(assignment[unit]), int(k >= 0), float(y)))
    return pd.DataFrame(rows, columns=["unit", "event_time", "treated", "post", "y"])


def fit(panel: pd.DataFrame, x: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    """Two-way within OLS with unit-cluster CR0 sandwich, no small-sample factor."""
    y = panel.y.to_numpy()
    unit = panel.unit.to_numpy() - 1
    time = panel.event_time.to_numpy() + 6
    # The panel is balanced, so double demeaning projects out both FE sets.
    def within(z):
        z = np.asarray(z, float).reshape(len(panel), -1)
        return z - z.reshape(70, 14, -1).mean(axis=1).repeat(14, axis=0) \
            - np.stack([z[time == k].mean(axis=0) for k in range(14)])[time] + z.mean(axis=0)
    yw, xw = within(y).ravel(), within(x)
    bread = np.linalg.inv(xw.T @ xw)
    beta = bread @ xw.T @ yw
    residual = yw - xw @ beta
    meat = np.zeros((xw.shape[1], xw.shape[1]))
    for i in range(70):
        score = xw[unit == i].T @ residual[unit == i]
        meat += np.outer(score, score)
    return beta, bread @ meat @ bread


def estimate(panel: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    panel = panel.sort_values(["unit", "event_time"]).reset_index(drop=True)
    assert len(panel) == 980 and panel.unit.nunique() == 70
    assert not panel.duplicated(["unit", "event_time"]).any()
    assert set(panel.unit) == set(range(1, 71))
    assert panel.groupby("unit").event_time.apply(lambda s: set(s) == set(PERIODS)).all()
    assert panel.groupby("unit").treated.nunique().eq(1).all()
    assert set(panel.treated) == {0, 1} and panel.treated.sum() == 490
    assert (panel.post.to_numpy() == (panel.event_time.to_numpy() >= 0)).all()
    treated = panel.treated.to_numpy()
    k = panel.event_time.to_numpy()
    static_beta, static_v = fit(panel, (treated * panel.post.to_numpy())[:, None])
    x = np.column_stack([treated * (k == period) for period in PERIODS if period != -1])
    beta13, v13 = fit(panel, x)
    beta = np.insert(beta13, 5, 0.0)
    v = np.insert(np.insert(v13, 5, 0.0, axis=0), 5, 0.0, axis=1)
    pre = np.where(PERIODS < 0, 1 / 6, 0)
    post = np.where(PERIODS >= 0, 1 / 8, 0)
    contrast = post - pre
    pre_b, post_b, did_b = pre @ beta, post @ beta, contrast @ beta
    did_se = float(np.sqrt(contrast @ v @ contrast))
    assert np.isclose(did_b, static_beta[0], atol=1e-12)
    assert np.isclose(did_se, np.sqrt(static_v[0, 0]), atol=1e-12)
    delta = panel.groupby(["unit", "treated", "post"]).y.mean().unstack("post")
    delta["change"] = delta[1] - delta[0]
    dt = delta.xs(1, level="treated").change.to_numpy()
    dc = delta.xs(0, level="treated").change.to_numpy()
    oracle_b = dt.mean() - dc.mean()
    oracle_se = np.sqrt(((dt - dt.mean()) ** 2).sum() / 35**2 +
                        ((dc - dc.mean()) ** 2).sum() / 35**2)
    assert np.isclose(did_b, oracle_b, atol=1e-12)
    assert np.isclose(did_se, oracle_se, atol=1e-12)
    estimates = pd.DataFrame({"term": TERMS, "event_time": PERIODS,
                              "estimate": beta, "is_reference": (PERIODS == -1).astype(int),
                              "weight": np.ones(14)})
    covariance = pd.DataFrame(v, index=TERMS, columns=TERMS)
    covariance.index.name = "term"
    z = norm.ppf(.975)
    results = pd.DataFrame([
        ("pre_mean", pre_b, np.sqrt(pre @ v @ pre)),
        ("post_mean", post_b, np.sqrt(post @ v @ post)),
        ("post_minus_pre", did_b, did_se),
        ("static_did", static_beta[0], np.sqrt(static_v[0, 0])),
        ("unit_change_oracle", oracle_b, oracle_se),
    ], columns=["estimand", "estimate", "se"])
    results["ci_low"] = results.estimate - z * results.se
    results["ci_high"] = results.estimate + z * results.se
    return estimates, covariance, results


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path, default=Path.cwd(),
                        help="Directory for generated panel, coefficient, covariance, and contrast CSVs.")
    output_dir = parser.parse_args().output_dir
    output_dir.mkdir(parents=True, exist_ok=True)
    panel = generate_panel()
    panel.to_csv(output_dir / "demo_panel.csv", index=False, float_format="%.17g")
    estimates, covariance, results = estimate(pd.read_csv(output_dir / "demo_panel.csv"))
    estimates.to_csv(output_dir / "demo_estimates.csv", index=False, float_format="%.17g")
    covariance.to_csv(output_dir / "demo_covariance.csv", float_format="%.17g")
    results.to_csv(output_dir / "demo_contrasts.csv", index=False, float_format="%.17g")
    print(results.to_string(index=False))
    print("PYTHON_PANEL_ESTIMATION_COMPLETE")


if __name__ == "__main__":
    main()
