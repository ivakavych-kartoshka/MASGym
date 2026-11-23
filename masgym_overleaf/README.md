# MASGym — AAMAS 2027 main paper (Overleaf-ready)

Upload **this whole folder** to Overleaf (Menu → Upload → select `masgym_overleaf`).
Everything is self-contained; no file references anything outside this folder.

---

## Cài đặt trên Overleaf (2 bước)

1. **Main document = `main.tex`**
   Menu → *Main document* → chọn `main.tex`.
   *(Chọn `preamble.tex` giờ cũng chạy được — xem "Đã vá gì" — nhưng khi đó file
   PDF xuất ra mang tên `preamble.pdf`.)*

2. **Compiler = pdfLaTeX**
   Menu → *Settings* → *Compiler* → **pdfLaTeX**.

   ⚠️ **Không dùng XeLaTeX hay LuaLaTeX.** Bài dùng `\usepackage[utf8]{inputenc}` +
   `[T1]{fontenc}` + newtxmath, là bộ chỉ chạy đúng với pdfLaTeX. Chọn sai compiler
   sẽ ra lỗi font (`Missing character`, `LaTeX Font Warning`).

Bấm **Recompile** là xong. Overleaf tự chạy đúng chuỗi
`pdflatex → bibtex → pdflatex → pdflatex` nên không cần can thiệp.

**Đã kiểm chứng cả hai kịch bản, compile từ số 0:**

| Main document | Kết quả |
|---|---|
| `main.tex` | 10 trang, 0 undefined, 0 error |
| `preamble.tex` | tự chuyển sang `main.tex`, 10 trang, 0 undefined, 0 error |

---

## Cấu trúc

```
main.tex                            ← MAIN DOCUMENT, đặt làm root
preamble.tex                        ← \documentclass + packages + title/author + \input x2
references_verified.bib             ← 57 refs
ACM-Reference-Format.bst            ← \bibliographystyle cần đúng file này
aamas.cls                           ← class chính thức AAMAS 2027
by.pdf / by.eps                     ← logo CC-BY, BẮT BUỘC (dùng trong copyright block)
main.pdf                            ← bản build sẵn, 10 trang

sections/
  abstract.tex              introduction.tex        related_work.tex
  preliminaries.tex         system_model.tex        threat_model.tex
  problem_formulation.tex   methodology.tex          algorithm.tex
  theory.tex                experiments.tex          discussion.tex
  conclusion.tex

figures/
  tikz_styles.tex                   ← palette màu + TikZ icon (khai báo trong preamble)
  pgfplots_placeholder_results.tex  ← HÌNH 1: 4 panel kết quả

tables/
  defense_table.tex                 ← BẢNG 1 (tab:defense)
```

---

## Đã vá gì (3 chỗ, không đổi nội dung khoa học của bài)

### 1. `tables/defense_table.tex` — đường dẫn thoát ra ngoài project

Bản gốc nằm ở `../MASGym/outputs/defense_table/defense_table.tex`. Overleaf không có
`MASGym/` nên sẽ hỏng. Đã copy vào `tables/` và sửa dòng 103 của
`sections/experiments.tex` thành `\input{tables/defense_table.tex}`.

### 2. Root guard — sửa lỗi "no legal `\end` found"

Overleaf tự chọn làm "Main document" file nào chứa `\documentclass`. Trong project này
`\documentclass` nằm ở **`preamble.tex`**, không phải `main.tex`, nên Overleaf auto-pick
`preamble.tex` — file đó không có `\begin{document}`/`\end{document}` → báo
`job aborted, no legal \end found`.

Cách vá (không so sánh chuỗi nên chắc chắn đúng trên mọi bản TeX):

- `main.tex` đóng dấu `\@masgym@root` ngay trước `\input{preamble.tex}`
- `preamble.tex` kiểm tra dấu đó; nếu thấy mình *không* được ai `\input` thì
  `\input{main.tex}` rồi `\endinput`

Kết quả: chọn file nào cũng ra PDF đúng, và class chỉ load đúng một lần.

### 3. `by.eps` thêm vào

Phương án dự phòng cho `\includegraphics{by}` phòng khi ai đó đổi compiler.

---

## Nếu sau này thêm `main_supplement.tex` vào package

File đó cũng `\input{preamble.tex}` mà **không** có dấu `\@masgym@root`, nên sẽ bị
chuyển nhầm sang `main.tex`. Thêm đúng một dòng vào `main_supplement.tex`, ngay trước
`\input{preamble.tex}`:

```latex
\makeatletter\def\@masgym@root{main_supplement.tex}\makeatother
```

---

## Không có gì trong package này (có chủ đích)

- **Supplement / appendix** — nằm ở PDF riêng (`main_supplement.pdf`) vì AAMAS 2027
  main track chỉ được vượt 8 trang ở phần *bibliographic references*.
- `figures/tikz_architecture.tex`, `tikz_threat_privacy_robustness.tex`,
  `tikz_theory_diagram.tex`, `tikz_method_pipeline.tex`,
  `tikz_experimental_setup.tex` — 5 hình này đã chuyển sang supplement;
  `\input` của chúng đã bị comment trong `sections/methodology.tex`.
- `tables/pilot_topology.tex` — không file nào `\input` nó.
- `sections/threat_model.tex` — rỗng (2 dòng comment); Threat Model đã merge vào
  `sections/system_model.tex` (label `sec:threat` nằm ở đó).

## Lưu ý về giới hạn trang

AAMAS 2027 main track: **tối đa 8 trang** + phần references không giới hạn.
PDF hiện tại là **10 trang** → vẫn cần cắt bớt ~2 trang trước khi nộp.
Không được sửa tham số style/layout của `aamas.cls`.
