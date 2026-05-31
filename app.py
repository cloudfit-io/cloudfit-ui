"""Gradio demo UI for cloudfit.

Loads a bundled GCP machine-type snapshot at startup and scores it against
the user's workload profile using cloudfit-core in-process. No API calls,
no provider credentials, no database.
"""

from __future__ import annotations

import json
from pathlib import Path

import gradio as gr

from cloudfit import (
    Archetype,
    GPUSpec,
    MachineType,
    OptimizeFor,
    WorkloadProfile,
    rank,
)

SNAPSHOT_PATH = Path(__file__).parent / "data" / "gcp_snapshot.json"
CANDIDATES: list[MachineType] = [
    MachineType(**row) for row in json.loads(SNAPSHOT_PATH.read_text())
]
REGIONS = ["Any"] + sorted({c.region for c in CANDIDATES})
HOURS_PER_MONTH = 730  # AWS / GCP convention


EXAMPLES: dict[str, dict] = {
    "BWA-MEM2 alignment (I/O bound)": {
        "vcpu": 32, "ram_gb": 64, "archetype": "io",
        "optimize_for": "balanced", "tool": "bwa-mem2",
    },
    "Cell Ranger (memory bound)": {
        "vcpu": 16, "ram_gb": 128, "archetype": "mem",
        "optimize_for": "performance", "tool": "cellranger",
    },
    "AlphaFold inference (GPU)": {
        "vcpu": 12, "ram_gb": 85, "archetype": "gpu",
        "optimize_for": "performance", "gpu_required": True, "gpu_vram": 40,
        "tool": "alphafold",
    },
    "Nextflow burst (parallel)": {
        "vcpu": 16, "ram_gb": 64, "archetype": "burst",
        "optimize_for": "cost", "tool": "nextflow",
    },
    "Spark ETL (CPU bound)": {
        "vcpu": 64, "ram_gb": 256, "archetype": "cpu",
        "optimize_for": "balanced", "tool": "spark",
    },
}


def recommend(
    vcpu: int,
    ram_gb: float,
    archetype: str,
    optimize_for: str,
    region: str,
    gpu_required: bool,
    gpu_vram: int,
    workload: str,
    tool: str,
    top_k: int,
):
    """Rank the snapshot for the given profile, return (summary md, table rows)."""
    try:
        profile = WorkloadProfile(
            vcpu=int(vcpu),
            ram_gb=float(ram_gb),
            archetype=Archetype(archetype),
            optimize_for=OptimizeFor(optimize_for),
            region=None if region == "Any" else region,
            gpu=GPUSpec(
                required=bool(gpu_required),
                vram_gb=int(gpu_vram) if gpu_required and gpu_vram else None,
            ),
            workload=workload.strip() or "generic",
            tool=tool.strip() or None,
        )
    except Exception as e:
        return f"**Invalid input:** {e}", []

    ranked = rank(profile, CANDIDATES)
    qualified = [r for r in ranked if not r.disqualified][: int(top_k)]

    if not qualified:
        first_dq = next((r for r in ranked if r.disqualified), None)
        reason = first_dq.disqualify_reason if first_dq else "no matching instances"
        return (
            f"**No instances pass the hard floor for this profile.**\n\n"
            f"Closest mismatch: {reason}",
            [],
        )

    top = qualified[0]
    summary = (
        f"### Top pick: `{top.instance.id}`\n\n"
        f"**{top.instance.vcpu} vCPU · {top.instance.ram_gb:g} GB RAM · "
        f"{top.instance.provider.upper()} · {top.instance.region}**\n\n"
        f"**${top.instance.price_hr:.3f}/hr** "
        f"(~${top.instance.price_hr * HOURS_PER_MONTH:,.0f}/month at 24/7)\n\n"
        f"Score `{top.score:.3f}` — "
        f"cost `{top.cost_score:.2f}` · perf `{top.perf_score:.2f}` · "
        f"avail `{top.avail_score:.2f}`"
    )

    rows = [
        [
            s.instance.id,
            s.instance.provider,
            s.instance.region,
            s.instance.vcpu,
            f"{s.instance.ram_gb:g}",
            f"${s.instance.price_hr:.3f}",
            f"${s.instance.price_hr * HOURS_PER_MONTH:,.0f}",
            f"{s.score:.3f}",
        ]
        for s in qualified
    ]

    return summary, rows


def load_example(name: str):
    """Populate the form with an example workload."""
    ex = EXAMPLES[name]
    return (
        ex.get("vcpu", 16),
        ex.get("ram_gb", 64),
        ex.get("archetype", "cpu"),
        ex.get("optimize_for", "balanced"),
        ex.get("gpu_required", False),
        ex.get("gpu_vram", 0),
        ex.get("tool", ""),
    )


with gr.Blocks(title="cloudfit demo", theme=gr.themes.Soft()) as demo:
    gr.Markdown(
        """
        # cloudfit
        ### Pick a workload, get a cloud machine-type recommendation.

        This is a demo UI over [cloudfit-core](https://github.com/cloudfit-io/cloudfit-core).
        It scores a bundled GCP snapshot (875 instance types across 5 regions)
        against your workload profile. For programmatic access, see the
        [HTTP API](https://chaitanyakasaraneni-cloudfit-api.hf.space/docs).
        """
    )

    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("#### Workload profile")
            vcpu = gr.Slider(1, 128, value=16, step=1, label="vCPU")
            ram_gb = gr.Slider(1, 512, value=64, step=1, label="RAM (GB)")
            archetype = gr.Dropdown(
                choices=[a.value for a in Archetype],
                value="cpu",
                label="Archetype",
                info="io · cpu · mem · gpu · burst",
            )
            optimize_for = gr.Radio(
                choices=[o.value for o in OptimizeFor],
                value="balanced",
                label="Optimize for",
            )
            region = gr.Dropdown(
                choices=REGIONS, value="Any", label="Region (optional)"
            )

            with gr.Accordion("GPU and metadata (optional)", open=False):
                gpu_required = gr.Checkbox(value=False, label="GPU required")
                gpu_vram = gr.Slider(0, 80, value=0, step=4, label="Min GPU VRAM (GB)")
                workload = gr.Textbox(value="", label="Workload name", placeholder="generic")
                tool = gr.Textbox(value="", label="Tool", placeholder="bwa-mem2, cellranger, ...")

            top_k = gr.Slider(1, 10, value=5, step=1, label="How many to show")

            with gr.Row():
                submit = gr.Button("Recommend", variant="primary")
                clear = gr.ClearButton(value="Reset")

            gr.Markdown("#### Try an example")
            example_picker = gr.Radio(
                choices=list(EXAMPLES.keys()),
                label=None,
                show_label=False,
            )

        with gr.Column(scale=2):
            summary_md = gr.Markdown("Fill out the form on the left and click **Recommend**.")
            table = gr.Dataframe(
                headers=["instance", "provider", "region", "vCPU", "RAM (GB)",
                         "price/hr", "~ $/mo (24/7)", "score"],
                interactive=False,
                wrap=True,
                label="Ranked recommendations",
            )

    inputs = [vcpu, ram_gb, archetype, optimize_for, region,
              gpu_required, gpu_vram, workload, tool, top_k]

    submit.click(recommend, inputs=inputs, outputs=[summary_md, table])
    clear.add([summary_md, table])

    example_picker.change(
        load_example,
        inputs=[example_picker],
        outputs=[vcpu, ram_gb, archetype, optimize_for, gpu_required, gpu_vram, tool],
    )

    gr.Markdown(
        """
        ---
        **About the snapshot.** Representative sample of GCP Compute Engine across
        `us-central1`, `us-east1`, `us-west1`, `europe-west4`, `asia-southeast1`.
        Not live pricing — use [cloudfit-provider-gcp](https://github.com/cloudfit-io/cloudfit-provider-gcp)
        to regenerate from your own GCP project.

        **Source code.** [cloudfit-ui](https://github.com/cloudfit-io/cloudfit-ui) ·
        [cloudfit-core](https://github.com/cloudfit-io/cloudfit-core) ·
        [cloudfit-api](https://github.com/cloudfit-io/cloudfit-api)
        """
    )


if __name__ == "__main__":
    demo.launch()
