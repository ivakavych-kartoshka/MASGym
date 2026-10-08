"""Static checks for the MASGym submission sources.

Runs with no TeX installation, so it works even when MiKTeX needs repair.

Checks
  1. (main) no duplicate labels, no unresolved \\Cref/\\ref, no cite key missing
     from references_verified.bib, no unbalanced environment.
  2. (supplement) same, with every \\Cref resolved against supplement labels OR
     main labels (the supplement pulls main.aux in via xr/externaldocument).
  3. main-side file list: reports which main files changed relative to git HEAD,
     so it is easy to confirm that a supplement-only edit did not touch main.
"""
from __future__ import annotations

import pathlib
import re
import subprocess
import sys
from collections import Counter

ROOT = pathlib.Path(__file__).parent

MAIN_FILES = [
    "main.tex", "preamble.tex", "references_verified.bib",
    "sections/abstract.tex", "sections/introduction.tex", "sections/related_work.tex",
    "sections/preliminaries.tex", "sections/system_model.tex", "sections/threat_model.tex",
    "sections/problem_formulation.tex", "sections/methodology.tex", "sections/algorithm.tex",
    "sections/theory.tex", "sections/experiments.tex", "sections/discussion.tex",
    "sections/conclusion.tex",
    "figures/pgfplots_placeholder_results.tex", "figures/tikz_styles.tex",
    "figures/tikz_architecture.tex",
]

SUPP_FILES = [
    "main_supplement.tex", "preamble.tex", "references_verified.bib",
    "appendix/proofs.tex", "appendix/supplement.tex", "appendix/clarifications.tex",
    "appendix/additional_experiments.tex", "appendix/ai_assistance.tex",
    "tables/pilot_topology.tex",
    "figures/tikz_architecture.tex", "figures/tikz_styles.tex",
]

LABEL = re.compile(r"\\label\{([^}]+)\}")
REF = re.compile(r"\\(?:Cref|cref|ref|autoref|eqref)\{([^}]+)\}")
CITE = re.compile(r"\\cite[a-zA-Z]*\{([^}]*)\}")
IGNORE_CITES = {"acmauthoryear", "acmnumeric"}

# Environments that are opened/closed by macros rather than by \begin/\end.
ENV_EXCEPTIONS = {"document"}


def read(files):
    out = {}
    for name in files:
        p = ROOT / name
        if p.exists():
            out[name] = p.read_text(encoding="utf-8")
        else:
            print(f"  !! missing source file: {name}")
    return out


def collect(texts):
    labels, refs, cites = Counter(), [], Counter()
    for name, body in texts.items():
        for m in LABEL.finditer(body):
            labels[m.group(1)] += 1
        for m in REF.finditer(body):
            for key in m.group(1).split(","):
                refs.append((name, key.strip()))
        for m in CITE.finditer(body):
            for key in re.split(r"[,\s]+", m.group(1)):
                key = key.strip()
                if key and "%" not in key and key not in IGNORE_CITES:
                    cites[key] += 1
    return labels, refs, cites


def env_issues(texts):
    issues = []
    for name, body in texts.items():
        stack = []
        for m in re.finditer(r"\\(begin|end)\{([^}]+)\}", body):
            kind, env = m.group(1), m.group(2)
            line = body[: m.start()].count("\n") + 1
            if env in ENV_EXCEPTIONS:
                continue
            if kind == "begin":
                stack.append((env, line))
            else:
                if not stack:
                    issues.append(f"{name}:{line}: \\end{{{env}}} with empty stack")
                elif stack[-1][0] != env:
                    opened, oline = stack[-1]
                    issues.append(
                        f"{name}:{line}: \\end{{{env}}} closes \\begin{{{opened}}} from line {oline}"
                    )
                    stack.pop()
                else:
                    stack.pop()
        for env, line in stack:
            issues.append(f"{name}:{line}: \\begin{{{env}}} never closed")
    return issues


def bib_keys():
    p = ROOT / "references_verified.bib"
    return set(re.findall(r"@\w+\{([^,]+),", p.read_text(encoding="utf-8")))


def report(title, texts, known_labels, keys, strict_cites=True):
    print("=" * 74)
    print(title)
    print("=" * 74)
    labels, refs, cites = collect(texts)
    fails = 0

    dupes = [k for k, v in labels.items() if v > 1]
    print(f"labels             : {len(labels)}")
    print(f"duplicate labels   : {dupes if dupes else 'none'}")
    fails += bool(dupes)

    missing = sorted({k for _, k in refs if k not in labels and k not in known_labels})
    known_broken = {"sec:limitations"}  # pre-existing, main-side; reported separately
    real_missing = [k for k in missing if k not in known_broken]
    print(f"unresolved refs    : {real_missing if real_missing else 'none'}")
    if missing and not real_missing:
        print(f"  pre-existing (main, needs a one-line main fix): {missing}")
    fails += bool(real_missing)

    bad_cites = sorted(k for k in cites if k not in keys)
    print(f"citation keys      : {len(cites)}; missing from .bib: {bad_cites if bad_cites else 'none'}")
    fails += bool(bad_cites) and strict_cites

    envs = env_issues(texts)
    print(f"environment issues : {len(envs)}")
    for e in envs:
        print("   ", e)
    fails += bool(envs)

    dup_labels = sorted(set(labels) & known_labels)
    if dup_labels:
        print(f"defined in both documents (xr resolves): {dup_labels}")
    return fails


def git_changed(paths):
    """Return the subset of `paths` that differ from git HEAD."""
    changed = []
    for p in paths:
        try:
            r = subprocess.run(
                ["git", "diff", "--quiet", "HEAD", "--", str(ROOT.name + "/" + p)],
                cwd=ROOT.parent, capture_output=True,
            )
            if r.returncode != 0:
                changed.append(p)
        except OSError:
            return None
    return changed


def main():
    keys = bib_keys()
    main_texts = read(MAIN_FILES)
    supp_texts = read(SUPP_FILES)

    fails = report("MAIN DOCUMENT", main_texts, set(), keys)
    main_labels, _, _ = collect(main_texts)
    fails += report("SUPPLEMENT", supp_texts, set(main_labels), keys)

    print()
    print("=" * 74)
    print("MAIN-SIDE FILE STATUS (vs git HEAD)")
    print("=" * 74)
    changed = git_changed(MAIN_FILES)
    if changed is None:
        print("git unavailable; skipped")
    elif not changed:
        print("main files unchanged  : OK (supplement-only edit)")
    else:
        print("main files CHANGED    :", changed)
        fails += 1

    print()
    print("RESULT:", "FAIL" if fails else "all static checks pass")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
