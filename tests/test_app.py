"""Smoke tests for the demo: the bundled snapshot loads, ranks, and prices correctly."""

from typing import Any

import app


def _recommend(**over: Any) -> tuple[str, list[list[Any]]]:
    args: dict[str, Any] = {
        "vcpu": 16, "ram_gb": 64, "archetype": "burst", "optimize_for": "cost",
        "headroom": 0.0, "headroom_mode": "hard", "regions": [], "providers": app.PROVIDERS,
        "gpu_required": False,
        "gpu_vram": 0, "workload": "", "tool": "", "top_k": 3, "pricing_mode": "auto",
    }
    args.update(over)
    return app.recommend(**args)


def _instance(row: list[Any]) -> Any:
    return next(c for c in app.CANDIDATES if c.id == row[0] and c.region == row[2])


def test_snapshot_loads_with_prices() -> None:
    assert app.CANDIDATES
    assert all(c.price_hr > 0 for c in app.CANDIDATES)
    assert {c.provider for c in app.CANDIDATES} == {"gcp", "aws"}


def test_providers_filter_limits_the_clouds() -> None:
    _, rows = _recommend(providers=["aws"], top_k=10)
    assert rows
    assert {r[1] for r in rows} == {"aws"}


def test_recommend_returns_ranked_rows() -> None:
    summary, rows = _recommend()
    assert summary.startswith("### Top pick:")
    assert 0 < len(rows) <= 3
    scores = [float(r[7]) for r in rows]
    assert scores == sorted(scores, reverse=True)


def test_each_instance_type_appears_once() -> None:
    _, rows = _recommend(archetype="cpu", optimize_for="balanced", top_k=10)
    keys = [(r[1], r[0]) for r in rows]
    assert len(keys) == len(set(keys))


def test_burst_auto_shows_spot_price() -> None:
    summary, rows = _recommend(providers=["gcp"])   # AWS has no spot prices
    inst = _instance(rows[0])
    assert inst.spot_price_hr
    assert rows[0][5] == f"${inst.spot_price_hr:.3f}"
    assert " spot " in summary


def test_on_demand_shows_list_price() -> None:
    _, rows = _recommend(pricing_mode="on_demand")
    assert rows[0][5] == f"${_instance(rows[0]).price_hr:.3f}"


def test_gpu_spot_falls_back_to_on_demand() -> None:
    summary, rows = _recommend(vcpu=12, ram_gb=85, archetype="gpu", optimize_for="performance",
                               gpu_required=True, gpu_vram=40, pricing_mode="spot")
    assert rows
    assert rows[0][5] == f"${_instance(rows[0]).price_hr:.3f}"
    assert " on_demand " in summary


def test_invalid_input_is_reported() -> None:
    summary, rows = _recommend(vcpu=0)
    assert summary.startswith("**Invalid input:**")
    assert rows == []
