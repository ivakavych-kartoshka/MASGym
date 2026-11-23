# Figure Quality Audit — MASGym

All six figures were compiled, rendered to PNG (`figure_previews/figN_*_pP-*.png` at 130 dpi),
and **visually inspected**. Two figures (Fig. 4, Fig. 5) had overlaps on first render and were
revised and re-inspected; all six now pass. Visual grammar (blue = honest, red = adversarial,
green = defense/TCB, purple = theory, gray = infrastructure) is shared via
`figures/tikz_styles.tex` and is consistent across figures. All icons are pure TikZ (no external
images). Color is backed by shape/dashing for grayscale readability.

| # | File | Label | Page | Icons | Arrows routed | Arrow over text? | Text overlap? | Labels readable | Colors consistent | Grayscale OK | Caption informative | Rendered+inspected | Final |
|---|------|-------|------|-------|---------------|------------------|---------------|-----------------|-------------------|--------------|---------------------|--------------------|-------|
| 1 | `tikz_architecture.tex` | `fig:architecture` | 4 | yes (orchestrator, agent, sybil, tool, memory, emulator, checker, theorem) | yes (lanes; `to[out,in]`, shorten) | no | no | yes | yes | yes (dashed adv, distinct shapes) | yes | yes | **PASS** |
| 2 | `tikz_threat_privacy_robustness.tex` | `fig:threat` | 11 | yes (orch-bad, attacker, tool-bad, mem-bad, sybil) | yes (horizontal lanes) | no | no | yes | yes | yes | yes | yes | **PASS** |
| 3 | `tikz_method_pipeline.tex` | `fig:pipeline` | 15 | yes (attacker, agent, checker, shield, theorem) | yes (forward + bottom feedback lane) | no | no | yes | yes | yes | yes | yes | **PASS** |
| 4 | `tikz_theory_diagram.tex` | `fig:theory` | 22 | n/a (concept boxes) | yes (routed `to[out,in]`) | no | **fixed** (was overlapping; now no) | yes | yes | yes | yes | yes | **PASS** |
| 5 | `tikz_experimental_setup.tex` | `fig:expsetup` | 26 | n/a (labeled bands) | yes (band-to-band) | no | **fixed** (metric box overflow + touching boxes resolved) | yes | yes | yes | yes | yes | **PASS** |
| 6 | `pgfplots_placeholder_results.tex` | `fig:results` | 27 | n/a (plots) | n/a | no | no | yes | yes | yes (dashed vs solid series) | yes (marked conceptual) | yes | **PASS** |

## Revisions made during inspection
- **Fig. 1:** legend items were touching ("trace/evaluation" vs "red=adversarial"); respaced the
  legend and replaced the redundant last item with a "scored via checker" swatch. Icons moved to the
  left of named nodes (the initial `\pic (name)`-as-anchor approach did not create referenceable
  shapes and was replaced by the node + adjacent-`\pic` pattern).
- **Fig. 4:** the six center result boxes overlapped vertically (one label was clipped). Increased
  vertical spacing, capped each box to two lines, widened the canvas via `\resizebox{0.98\textwidth}`.
  Re-inspected: no overlap, arrows routed cleanly, aligned with the insight column.
- **Fig. 5:** the Metrics box text overflowed and the swept-variables / systems boxes touched.
  Widened the metrics box and reformatted its content into short lines; increased inter-box spacing;
  shortened "orch. trusted / compromised" to two lines. Re-inspected: fits, no overlap.

## Readability rules (spec §"STRICT FIGURE READABILITY RULES") — status
1–7 (no arrow through text/label/equation/icon; no text/node overlap; arrowheads shortened): **PASS**
(arrows use `.east/.west/.north/.south` anchors with `to[out,in]` routing and `shorten` via the
`>={Latex}` styles). 8 routed arrows: **PASS**. 9 separate lanes (data/control/adversarial/
evaluation/theory): **PASS**. 10 white-background arrow labels (`arlbl` style): **PASS** (used on
trace/ASR labels). 11 short node labels, detail in captions: **PASS**. 12 consistent `text width`/
`minimum height`: **PASS**. 13 shared style file: **PASS**. 14–15 fixed visual grammar + grayscale via
shape/dash: **PASS**. 16 dense diagrams split (theory + threat separated from architecture): **PASS**.
17 every figure has caption + label + legend + in-text reference: **PASS**. 18 rendered to PNG and
inspected, revised on overlap: **PASS**.

## Verdict
All six figures **PASS** the overlap/readability audit and are marked final. PNG previews are in
`figure_previews/` (`fig1_architecture_p4`, `fig2_threat_p11`, `fig3_pipeline_p15`,
`fig4_theory_p22`, `fig5_expsetup_p26`, `fig6_results_p27`).
