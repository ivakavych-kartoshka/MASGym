# Notation Consistency Check — MASGym

Symbols are declared as macros in `main.tex` and tabulated in Table 1 (`tab:notation`,
Section 3). The manuscript compiles with **no undefined control sequences**, so every macro used
is defined. Checks below are for *semantic* conflicts and completeness.

## 1. No symbol reused for conflicting meanings
**PASS with one cosmetic note.**
- Agent count `N` (italic), naturals `\N`$=\mathbb{N}$, inbound neighbourhood `\Nin`$=\mathcal{N}^-$:
  three "N" glyphs, all in different fonts and roles — unambiguous. (`\N` is defined but effectively
  unused; harmless.)
- **Cosmetic note:** graph edges `\Etop`$=\mathcal{E}$ and the LM emulator `\Emu`$=\mathcal{E}_{\mathrm{LM}}$
  share the calligraphic base $\mathcal{E}$. They are disambiguated by the `LM` subscript and never
  co-occur ambiguously (edges appear only as $\Etop$/$|\Etop|$ in Section 8.1; the emulator only as
  $\Emu$/$\Emu^{\dagger}$). Acceptable; a future revision could rename the emulator to remove even the
  cosmetic overlap. Listed in `TODO_before_submission.md`.
- Configurations `\Configs`$=\mathcal{C}$ vs checker `\Checker`$=\mathsf{C}$: distinct fonts
  (calligraphic vs sans-serif). Config instance `\config`$=c$ (italic). Unambiguous.
- Security predicate `\Predsec`$=\Phi$ vs benign predicate `\Predutil`$=\Psi$: distinct. Judge
  `\Judge`$=\mathsf{J}$ distinct from checker.
- Rates `\CPR`,`\CSR` (upright); red/blue policies `\red`$=\rho$, `\blue`$=\delta$; per-edge prob
  `\pinf`$=p$; threshold `\thresh`$=\theta$; adversary fraction `\betafrac`$=\beta$; agreement
  `\kappaem`$=\kappa$; episodes `M`; horizon `H`. Each has a single meaning throughout.

## 2. All symbols in equations are defined
**PASS.** Eq. (1) NRP/PNA/ASR (ASB, defined in text); Eq. (2) $\config_{\mathrm{adv}}$ components
(all seven defined in the itemized list); Eqs. (3)–(5) $\ASRs,\PNAs,\NRPs$ (Definition 6.2);
Eq. (6) $\CPR$ with $\Advset_0,\Advset_\infty,N$ (Definition 6.4). Theorem constants
$\pinf,\thresh,b,d,n,N,s,M,\epsilon,\alpha,\Delta,G,H$ are defined at first use.

## 3. All equation labels are referenced correctly
**PASS.** `eq:asb-nrp` (Prelim, Prop 9.1), `eq:adv-config` (Threat, Method), `eq:asrsys`,
`eq:pnasys`, `eq:nrpsys` (Method, Theory), `eq:cpr` (Method, Algorithm). Every numbered equation is
referenced at least once; no dangling equation labels.

## 4. Theorem variables match the system-model variables
**PASS.** $N,\Gtop,\Etop,\Advset,\betafrac,\Trace,\Predsec,\Predutil,\Checker,\pinf,\thresh$ used in
Section 9 are exactly the objects defined in Sections 3–7 (Table 1, Definitions 6.1–6.5). The
propagation constants $b$ (branching factor), $d$ (depth), $s$ (seeds) in Props 9.8–9.10 are local to
those statements and defined inline.

## 5. No undefined constants in final theorem statements
**PASS.** Each theorem's constants are bound: Thm 9.13's gap is the explicit
$\pinf(1-\pinf)(N-1)(N-2)/N$; Thm 9.17's rates are explicit in $M,\epsilon,\alpha,G$; Cor 9.18's
budget is explicit in $\Delta,G,N,H,\alpha$. No unquantified "$c$", "$C$", or "constant" appears in a
final theorem statement.

## Summary
Notation is internally consistent; the only issue is a cosmetic $\mathcal{E}$ overlap (edges vs
emulator), disambiguated by subscript and non-co-occurring. No action strictly required; noted for a
future cleanup pass.
