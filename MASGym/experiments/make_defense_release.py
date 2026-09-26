"""Build a self-contained, reviewable release bundle for the defense study.

Rationale: the paper claims the exact prompts behind every released decision
are recoverable from the artifact. The raw run directories are gitignored
(MASGym/.gitignore ignores outputs/**), so that claim is only verifiable if a
compact bundle is published separately. This script flattens the per-cell
decisions.jsonl files into one CSV and factorises the prompts into a small
lookup table, which turns ~3.9 MB of duplicated prompt text into ~20 KB without
losing the ability to reconstruct the exact bytes sent to each backbone.

The three locally run backbones carry full prompt fields. The hosted Mistral
run predates prompt logging, so it is emitted with an empty prompt_id rather
than a fabricated prompt.

Writes a CSV of decisions, a CSV of cell metrics, a JSONL of unique prompts and
a README describing provenance. Local/offline: reads only run artifacts.
"""
from __future__ import annotations

import argparse
import csv
import json
import pathlib
import sys

_ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

SOURCES = [
    ("Qwen2.5-3B", "outputs/llm_pilot_defense/Qwen2.5-3B-Instruct--delimiting", True),
    ("Qwen2.5-7B", "outputs/llm_pilot_defense/Qwen2.5-7B-Instruct-bnb-4bit--delimiting", True),
    ("Llama-3.2-1B", "outputs/llm_pilot_defense/Llama-3.2-1B-Instruct--delimiting", True),
    ("Mistral-7B", "outputs/llm_pilot_scale/mistral-7b-bedrock--delimiting", False),
]

SCENARIOS = ["single_attacker", "colluding", "compromised_orchestrator"]

DECISION_COLUMNS = [
    "backbone", "topology", "n_agents", "scenario", "episode", "agent", "t",
    "attack", "defense", "action", "parse_failed", "parse_rule", "prompt_id",
    "latency_s", "approx_tokens", "raw_model_output",
]

EXFIL_ACTION = "exfiltrate"


def read_jsonl(path: pathlib.Path):
    with path.open(encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                yield json.loads(line)


def assign_scenarios(records, scen_metrics, where):
    """Label each record with its scenario.

    The decision log does not store the scenario name, so the mapping is
    recovered from the order scenarios are appended in. Benign episodes emit no
    decisions at all, so the attack scenarios form one contiguous block. Every
    derived slice is checked against the per-scenario episode, decision and
    exfiltration counts in summary.json; a mismatch is fatal rather than
    silently mislabelled.
    """
    order = [name for name, _ in scen_metrics]
    labelled = []
    cursor = 0
    for name, metrics in scen_metrics:
        want = int(metrics.get("decisions") or 0)
        slice_ = records[cursor:cursor + want]
        if len(slice_) != want:
            raise SystemExit(
                f"{where}: expected {want} decisions for {name}, found "
                f"{len(slice_)}; refusing to guess the mapping"
            )
        got_exfil = sum(1 for r in slice_ if r.get("action") == EXFIL_ACTION)
        want_exfil = int(metrics.get("exfiltration_decisions") or 0)
        if got_exfil != want_exfil:
            raise SystemExit(
                f"{where}: exfiltration count for {name} is {got_exfil} but "
                f"summary.json says {want_exfil}; scenario mapping is wrong"
            )
        for r in slice_:
            r["_scenario"] = name
        labelled.extend(slice_)
        cursor += want
    if cursor != len(records):
        raise SystemExit(
            f"{where}: {len(records) - cursor} decisions left over after mapping "
            f"{order}; refusing to guess"
        )
    return labelled


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--out", default="outputs/defense_release")
    args = ap.parse_args()

    out = _ROOT / args.out
    out.mkdir(parents=True, exist_ok=True)

    prompts: dict[tuple[str, str], str] = {}
    prompt_rows: list[dict] = []
    dec_rows: list[dict] = []
    cell_rows: list[dict] = []
    missing_prompt_backbones: list[str] = []
    parse_failures = 0

    for label, rel, has_prompts in SOURCES:
        run_dir = _ROOT / rel
        if not run_dir.is_dir():
            print(f"missing run directory: {rel}", file=sys.stderr)
            return 1
        if not has_prompts:
            missing_prompt_backbones.append(label)

        for cell in sorted(run_dir.iterdir()):
            if not cell.is_dir():
                continue
            summary = json.loads((cell / "summary.json").read_text(encoding="utf-8"))
            n_agents = summary.get("env", {}).get("n_agents", "")
            topology = summary.get("env", {}).get("topology", cell.name)
            where = f"{label}/{cell.name}"

            scen_metrics = [
                (n, m) for n, m in summary.get("scenarios", {}).items() if n != "benign"
            ]
            for name, m in scen_metrics:
                n_bad = int(m.get("parse_failures") or 0)
                if n_bad:
                    raise SystemExit(
                        f"{where}/{name}: {n_bad} parse failures. A failed backbone "
                        f"call is recorded as a benign decision, so releasing it would "
                        f"present API breakage as model compliance. Re-run the cell "
                        f"with a working credential first."
                    )
                cell_rows.append({
                    "backbone": label,
                    "topology": topology,
                    "n_agents": n_agents,
                    "scenario": name,
                    "episodes": m.get("episodes"),
                    "asr_sys": m.get("asr_sys"),
                    "asr_action": m.get("asr_action"),
                    "cpr": m.get("cpr"),
                    "compliance_rate": m.get("compliance_rate"),
                    "decisions": m.get("decisions"),
                    "exfiltration_decisions": m.get("exfiltration_decisions"),
                    "parse_failures": m.get("parse_failures"),
                })

            dec_path = cell / "decisions.jsonl"
            if not dec_path.is_file():
                continue
            records = list(read_jsonl(dec_path))
            records = assign_scenarios(records, scen_metrics, where)

            for d in records:
                pid = ""
                if has_prompts:
                    key = (d.get("system_prompt", ""), d.get("user_prompt", ""))
                    pid = prompts.get(key, "")
                    if not pid:
                        pid = f"p{len(prompts):03d}"
                        prompts[key] = pid
                        prompt_rows.append({
                            "prompt_id": pid,
                            "system_prompt": key[0],
                            "user_prompt": key[1],
                        })
                if d.get("parse_failed"):
                    parse_failures += 1
                dec_rows.append({
                    "backbone": label,
                    "topology": topology,
                    "n_agents": n_agents,
                    "scenario": d.get("_scenario", ""),
                    "episode": d.get("episode", ""),
                    "agent": d.get("agent", ""),
                    "t": d.get("t", ""),
                    "attack": d.get("attack", ""),
                    "defense": d.get("defense", ""),
                    "action": d.get("action", ""),
                    "parse_failed": d.get("parse_failed", ""),
                    "parse_rule": d.get("parse_rule", ""),
                    "prompt_id": pid,
                    "latency_s": d.get("latency_s", ""),
                    "approx_tokens": d.get("approx_tokens", ""),
                    "raw_model_output": d.get("raw_model_output", ""),
                })

    with (out / "decisions.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=DECISION_COLUMNS)
        w.writeheader()
        w.writerows(dec_rows)

    with (out / "cells.csv").open("w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cell_rows[0]))
        w.writeheader()
        w.writerows(cell_rows)

    with (out / "prompts.jsonl").open("w", encoding="utf-8") as fh:
        for r in prompt_rows:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")

    (out / "README.md").write_text(build_readme(
        dec_rows, cell_rows, prompt_rows, missing_prompt_backbones, parse_failures
    ), encoding="utf-8")

    print(f"wrote {out}/decisions.csv ({len(dec_rows)} rows)")
    print(f"wrote {out}/cells.csv ({len(cell_rows)} cells)")
    print(f"wrote {out}/prompts.jsonl ({len(prompt_rows)} unique prompts)")
    print(f"wrote {out}/README.md")
    if parse_failures:
        print(f"WARNING: {parse_failures} unparseable decisions present", file=sys.stderr)
    return 0


def build_readme(dec_rows, cell_rows, prompt_rows, missing, parse_failures) -> str:
    lines = [
        "# Defense study release bundle",
        "",
        "Flattened from the run artifacts by `experiments/make_defense_release.py`.",
        "",
        "## Contents",
        "",
        f"- `decisions.csv` - {len(dec_rows)} decision records, one row per backbone call.",
        f"- `cells.csv` - {len(cell_rows)} cell-level metric rows (backbone x topology x scenario).",
        f"- `prompts.jsonl` - {len(prompt_rows)} unique prompt pairs, keyed by `prompt_id`.",
        "",
        "## Reconstructing an exact prompt",
        "",
        "`decisions.csv` carries `prompt_id`; join it against `prompts.jsonl` on",
        "`prompt_id` to recover the exact `system_prompt` and `user_prompt` bytes sent",
        "to the backbone. Scenario is also carried on the decision row so a reader can",
        "confirm which defense was active.",
        "",
        "## Provenance scope",
        "",
        "The three locally run backbones (Qwen2.5-3B, Qwen2.5-7B, Llama-3.2-1B) carry",
        "full prompt fields. The hosted Mistral-7B run predates prompt logging, so its",
        "rows have an empty `prompt_id`; it contributes cell metrics but not prompt",
        "text.",
    ]
    if missing:
        lines.append("")
        lines.append("Backbones without prompt text in this bundle: " + ", ".join(missing) + ".")
    if parse_failures:
        lines.append("")
        lines.append(f"Note: {parse_failures} decisions failed the parser; see `parse_ok`.")
    lines += [
        "",
        "## Regenerating",
        "",
        "```",
        "python experiments/run_llm_pilot_sweep.py --defense delimiting --topologies star,chain,tree,mesh --agents 5 --episodes 30",
        "python experiments/run_llm_pilot_sweep.py --backend bedrock --model mistral.mistral-7b-instruct-v0:2 --defense delimiting --topologies star,chain,tree,mesh --agents 5 --episodes 30",
        "python experiments/make_defense_release.py",
        "```",
        "",
    ]
    return "\n".join(lines)


if __name__ == "__main__":
    raise SystemExit(main())
