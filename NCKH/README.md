# MASGym — AAMAS 2027 submission (main paper)

**Paper:** MASGym: A Co-Evolving Red/Blue Security Gym for Multi-Agent LLM Systems
with Parameterized Collusion, Orchestrator Compromise, and System-Level Metrics

**Target venue:** AAMAS 2027 (3–7 May 2027, Hanoi, Vietnam), main track.
**Page limit:** 8 pages + unlimited bibliographic references. The current PDF is
**10 pages**, so the paper still needs to be cut down to 8 before submission.

---

## What's in this folder

| File | Purpose |
|---|---|
| `paper_merged.pdf` | Compiled paper, **10 pages**. Read this if you just want to review. |
| `paper_merged.tex` | **Single self-contained source.** All `\input{}` are already resolved inline — no `sections/`, `figures/`, or `tables/` subfolders needed. |
| `aamas.cls` | Official AAMAS 2027 document class. |
| `references_verified.bib` | BibTeX database (57 verified entries). |
| `ACM-Reference-Format.bst` | Required by `\bibliographystyle`. |
| `by.pdf`, `by.eps` | CC-BY logo required by the IFAAMAS copyright block. Do not delete. |
| `aamas27-logo-small.jpg` | Conference logo (kept for reference; unused by the .tex). |

## How to rebuild

```bash
pdflatex paper_merged.tex
bibtex  paper_merged
pdflatex paper_merged
pdflatex paper_merged
```

or simply:

```bash
latexmk -pdf paper_merged.tex
```

Verified clean: **0 undefined references, 0 undefined citations.** Requires
`pdflatex` + `bibtex` + the packages `microtype balance mathtools bm xspace
enumitem booktabs multirow array xcolor float tikz pgfplots xr cleveref`
(all in a standard TeX Live / MiKTeX install).

## Notes for reviewers

- The **supplementary material is a separate PDF** and is *not* in this folder. It
  was excluded on purpose: AAMAS 2027 main-track papers may only exceed 8 pages
  with bibliographic references, so appendices must be uploaded as a technical
  supplement. The main text cross-references it throughout ("Supplementary
  Material").
- The paper is in **anonymous** mode for double-blind review (the `anonymous`
  class option is set in `paper_merged.tex`). For the camera-ready, remove that
  option and keep the `\author` / `\affiliation` / `\email` block that is already
  filled in.
- Experiments are labelled honestly by provenance: panels marked *synthetic* come
  from the controlled emulator, panels marked *pilot* come from real LLM
  backbones. See §Evaluation.
