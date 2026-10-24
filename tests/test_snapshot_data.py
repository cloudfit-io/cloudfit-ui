"""Data-integrity checks on each bundled snapshot.

These run in CI on every pull request, including the weekly automated refresh
PRs, so a refresh that drops rows, loses prices, or ships malformed data fails
before merge instead of reaching the live demo.

The same checks run in cloudfit-api, which bundles identical snapshots.
"""

import json
from collections import Counter
from pathlib import Path

import pytest
from cloudfit import MachineType, cpu_arch_for

DATA = Path(__file__).resolve().parent.parent / "data"

# Expected size of each snapshot. A refresh may add or retire some instance
# types; a drop of more than 10% means a fetch went wrong. Update these when the
# catalog legitimately changes.
BASELINE_ROWS = {"gcp_snapshot.json": 875, "aws_snapshot.json": 6085}
REGIONS = {
    "gcp_snapshot.json": {"us-central1", "us-east1", "us-west1", "europe-west4", "asia-southeast1"},
    "aws_snapshot.json": {"us-east-1", "us-east-2", "us-west-2", "eu-west-1", "ap-southeast-1"},
}


def _load(name):
    return [MachineType(**row) for row in json.loads((DATA / name).read_text())]


@pytest.fixture(scope="module", params=sorted(BASELINE_ROWS))
def snapshot(request):
    return request.param, _load(request.param)


def test_row_count_has_not_dropped(snapshot):
    name, rows = snapshot
    assert len(rows) >= 0.9 * BASELINE_ROWS[name], f"{name}: {len(rows)} rows, baseline {BASELINE_ROWS[name]}"


def test_every_region_is_present(snapshot):
    name, rows = snapshot
    assert {m.region for m in rows} == REGIONS[name]


def test_no_duplicate_instances(snapshot):
    _, rows = snapshot
    dupes = [k for k, n in Counter((m.provider, m.id, m.region) for m in rows).items() if n > 1]
    assert not dupes, dupes[:5]


def test_every_instance_is_priced(snapshot):
    _, rows = snapshot
    unpriced = [(m.id, m.region) for m in rows if m.price_hr <= 0]
    assert not unpriced, unpriced[:5]


def test_discounted_prices_are_below_on_demand(snapshot):
    _, rows = snapshot
    bad = [(m.id, m.region) for m in rows
           if (m.spot_price_hr and m.spot_price_hr >= m.price_hr)
           or (m.cud_1yr_price_hr and m.cud_1yr_price_hr > m.price_hr)]
    assert not bad, bad[:5]


def test_scoring_fields_are_populated(snapshot):
    _, rows = snapshot
    assert all(m.perf_factor is not None for m in rows)
    assert all(m.gpu_vram_gb for m in rows if m.gpu_count)
    assert all(m.status in {"active", "deprecated", "tombstoned"} for m in rows)
    assert all(cpu_arch_for(m.id) is not None for m in rows)
