# Phản hồi review — chỉ sửa trong SUPPLEMENT

Ràng buộc của yêu cầu: **không đụng vào main paper**. Mọi thay đổi dưới đây nằm trong
`main_supplement.tex` và `appendix/*`. `check_sources.py` xác nhận: *main files unchanged*.

- Nguồn main đã ở đúng trạng thái commit `40e6fd7` (git sạch, không file nào lệch HEAD) — tôi
  **không** khôi phục/ghi đè gì lên `sections/*`, `preamble.tex`, `main.tex`, `figures/*`.
- Kiểm tra tĩnh: `python aamas2027\check_sources.py` → **all static checks pass** (0 label
  trùng, 0 `\Cref` không giải trong supplement, 0 cite thiếu trong `.bib`, 0 environment chưa
  đóng, main không đổi). Chỉ còn 1 ref hỏng **có sẵn từ trước trong main** — xem §3.

## 1. Đã đưa vào supplement

### `main_supplement.tex`
- **Đánh số float của supplement có prefix S**: `\renewcommand{\thetable}{S\arabic{table}}`,
  `\thefigure` tương tự. Đặt ngay trong `main_supplement.tex` (không sửa `preamble.tex` dùng
  chung), nên "Table 1" của supplement không còn trùng nghĩa với "Table 1" của main.
- Thêm `\input{appendix/clarifications.tex}`.

### `appendix/clarifications.tex` (MỚI — phần lớn nội dung review)
| Mục | Nội dung |
|---|---|
| §"The harness's trace projection and sabotage rule" (`app:harness`) | **Definition (Security-relevant projection π(τ))**: checker chỉ đọc các sự kiện cấu trúc (tool call, transition đã ghi, memory version, role, cạnh topology, identity map), bỏ toàn bộ text tự do ⇒ giải quyết mâu thuẫn "đổi message là đổi τ" của Thm 9.4/Prop 9.5, và nói rõ đây là mệnh đề về *thiết kế*, câu hỏi thực nghiệm nằm ở §10.2. **Definition (Availability sabotage)**: quy tắc chính xác của harness — sabotage khi (a) < k agent còn honest, hoặc (b) topology hub-critical (star/tree) và orchestrator bị compromise; không có LLM trong vòng lặp. Kèm 3 hệ quả: (1) chính quy tắc này làm ASR_sys bão hoà, không phải bound lan truyền; (2) đây là lý do **chain khác star/tree** và vì sao Prop 9.8(b) không mô tả sweep (chain dễ bị sabotage nhất *theo giả thiết của prop*, nhưng dễ nhất *trong đo đạc*); (3) đây là lý do defense 0 compliance vẫn ASR_sys = 1. |
| §"The placement result, stated exactly" (`app:placement`, `prop:placement`) | Phát biểu đầy đủ + chứng minh định lý collusion-advantage, **đổi tên đại lượng thành Δ_place** để không lẫn với Δ_coll (xác suất) của Def 6.5; nói rõ cạnh hai chiều và hướng ngược lại thì advantage còn lớn hơn; nói rõ **thực nghiệm không xác nhận chuỗi dấu** (5 giá trị đổi dấu, đều trong ±ε). |
| §"Resolution of the reported differences" (`app:power`) | M=738 ⇔ ±2ε≈0.1; bảng degradation: ưu thế guardrail 0.244/0.178/0.149 là thật, nhưng **shrinkage dựa trên margin 0.039 và 0.008 nên không resolved**, và baseline no-defense cũng giảm; 5 giá trị Δ_coll đều trong ±0.05; Bonferroni G=21 ⇒ **M ≥ 1347** nên sweep là mô tả, không phải 21 phát biểu 95% đồng thời; 1075 decision **không độc lập** (greedy + prompt gần như trùng + cluster trong 30 episode) nên Wilson bound chỉ mô tả mẫu; sửa **khoảng Wilson đúng hai phía**: [0,0.114], [0.886,1], [0.274,0.608] (bản cũ dùng cận một phía [0,0.10], [0.90,1] và [0.26,0.62] khác quy ước). |
| §"Terminology and a citation caveat" (`app:terms`) | NRP = **net resilient performance**, PNA = performance under no attack (đối chiếu ASB); tách NRP_sys vs NRP_act; **cảnh báo trung thực về κ≈0.48**: không xác nhận lại được con số này trong kết quả của ToolEmu (họ báo cáo tỉ lệ đồng thuận evaluator–human và tỉ lệ realism), nên đọc nó như caveat kế thừa, không phải đo đạc của bài. |

### `appendix/supplement.tex`
- Bỏ **toàn bộ câu meta về page limit** ("so the main paper stays within its page limit" ×3).
- §Threats to validity viết lại thành **5 limitation có số liệu**: (i) defense effect **không được nhận diện** (thiếu arm no-defense cùng protocol; Qwen 4 size + Llama-3B refuse khi *không* có defense ⇒ 0/1075 là floor effect; Llama-1B refuse nothing; Mistral comply cả khi undefended ⇒ không có contrast sạch); (ii) predicate có thể bị discharge không cần model (kèm M=738/±0.1 và Bonferroni 1347); (iii) scale/coverage (N≤10, 1 task, 1 template, 1 defense, M=30, greedy ⇒ phụ thuộc; mesh + N∈{20,50} chưa chạy; tool/mem không có kết quả tách riêng; Pareto chưa vẽ); (iv) emulation fidelity (sweep là synthetic effect model, không real tool backend, ablation chưa chạy); (v) instrument scope.
- Bảng notation: thêm `π(τ)`, `ASR_act`, `B_∞`, `c°`, `k`, `M` vs `M` (memory viết hoa), và ghi rõ `G` topology **không** phải số cấu hình.
- §Desiderata D1–D5: nói rõ **D2/D4 là axiom vận hành**, D1/D3 là hệ quả, D5 = Prop reduction; **g(0,σ)=0 là dư** (suy ra từ D4, λ=0); **D4 là giả định, không phải dẫn xuất** — kèm chứng minh ngắn rằng min và u^wσ^{1−w} (w<1) vi phạm D4 (và D2), nên "uniqueness" không còn vòng quanh.
- Bảng topology: **bỏ hàng mesh placeholder** (0.000/0.000/1.000) → dùng số pilot **CPR 0.627, ASR_sys 0.688, NRP_sys 0.312**, ô chưa instrument để trống; thêm đơn vị "Time-to-detect (steps)"; ghi rõ bounds ở các operating point khác nhau nên chỉ là pattern.
- §Cost: sweep đổi Θ → **O**, ghi rõ hệ số 2 lần chấm điểm mỗi round, nói rõ đây là **sufficient budget**.
- Bảng backbone: "both hosted cells" → **một cell hosted duy nhất (Mistral/AWS Bedrock)**; prompt block giữ nguyên `<<<BEGIN…>>>`; architecture chỉ vẽ một lần và gộp chung mục với notation.

### `appendix/proofs.tex`
- Sửa câu sai "**no conclusion of this paper depends on this appendix**": nay nói rõ **không kết luận *lý thuyết* nào** phụ thuộc appendix, nhưng **phần thực nghiệm thì có** (RQ1/RQ3/RQ4, collusion sweep, pilot no-defense, quy tắc sabotage, model/decoding) và main có trỏ tới.
- Prop chain/star/tree/mesh: nêu rõ **reach ≠ compromise**, edges **hai chiều** khi nói influence; Prop tree: gọi đúng là **critical branching mean** (transition chỉ đúng ở giới hạn d→∞); Prop mesh: **đẳng thức** thay vì "at least" + nói rõ không cần bất đẳng thức.
- §"Why the hub topologies are the environment's critical ones": thêm 3 qualification — (1) cơ chế là **quy tắc availability của harness** không phải influence bound; (2) "one injection reaches all workers" chỉ đúng khi ρ→1, với ρ<1 thì mỗi worker bị lây với xác suất ρ; (3) ordering chain<tree<star là **pattern thực nghiệm**, không có định lý so sánh ba topology ở cùng N và ρ.

### `appendix/additional_experiments.tex`
- Thêm đoạn **giải thích quan hệ 138 / 81 / 21 / 12 config**.
- Bảng degradation: đổi `ASR_sys† → ASR_act†` (đây là **predicate single-agent**, không phải system metric), nói rõ dưới full system predicate **mọi** defense (kể cả oracle) đều = 1.0, định nghĩa **system-level policy = fixed-threshold flag/defer** (yếu hơn guardrail nên nằm giữa) và **oracle = tham chiếu giả định**, bổ sung margin 0.039/0.008.
- Bảng Sybil: nói rõ count-0 là nhánh **independent**, và vì sao khác bảng collusion (0.775 vs 1.000) — hết mâu thuẫn Table 6 vs Table 8.
- Bảng adaptivity: **bỏ "Algorithm 2"** (không tồn tại), diễn giải lại đúng dữ liệu (static red mạnh hơn adaptive dưới system predicate; adaptivity chỉ thấy ở action channel; chuỗi không đơn điệu và M=60 không phân giải).
- Bảng collusion sweep: **thêm cột ASR_sys independent** (0.783/0.780/0.883/0.846/0.946) + header 2 cấp, xoá khối bảng cũ đã comment, sửa cách diễn giải ("shrinks with β" không được dữ liệu ủng hộ, mọi giá trị trong ±ε).
- Bảng cost: token cost là **output của model kinh tế tuyến tính**, không phải runtime đo được; latency có đơn vị **(a.u.)**; "138 configs" nói rõ là matrix 138 cấu hình.
- Pilot: "unlike the six backbones" → **"unlike five of the six"** (Qwen 4 size + Llama-3B refuse; Llama-1B comply); "(almost all parse failures 0)" → câu rõ nghĩa (parse failures được log, bằng 0 ở các ô này); **giải thích hàng Qwen2.5-3B (10/3878)**: các decision này nằm trong episode đã bị sabotage kết luận nên không đổi cell mean — không phải "hai backbone giống hệt"; mục topology study: bỏ "RQ4" và bỏ câu meta 8-page.
- Sensitivity: nói rõ ties (mid-rank Spearman) vì phần lớn NRP=0; "80/80 judge" ghi rõ **đúng theo cấu trúc nên không bound gì**; axiom là D2/D4; κ trỏ sang `app:terms`.

## 2. Những gì **không thể** sửa nếu không đụng main (cần bạn quyết)

Đây là các câu nằm trong main và đã được review nêu; tôi **không** sửa vì yêu cầu. Mỗi cái kèm mức độ:

| # | Vị trí (main) | Vấn đề | Ghi chú |
|---|---|---|---|
| M1 | `sections/introduction.tex:74`, `preliminaries.tex:36` | `\Cref{sec:limitations}` **không tồn tại** → PDF in ra `(??)` và LaTeX warning "undefined reference" | **Nên sửa**: thêm `\label{sec:limitations}` vào `\paragraph{Limitations.}` của `discussion.tex`, hoặc đổi thành `\Cref{sec:discussion}`. Đây là lỗi *có sẵn từ trước*, không do tôi. |
| M2 | `abstract.tex`, `introduction.tex` | "a prompt-level defense drives compliance to 0/1075 … A fourth backbone ignores the defense" được đọc như *defense có tác dụng* | Supplement §Threats (i) + `app:power` đã nói rõ floor effect; nếu muốn chắc chắn reviewer thấy, cần 1 câu trong Abstract/§10.3 (main). |
| M3 | `experiments.tex` (Bảng defense) | Bảng trong main **không có** cột control no-defense | Tôi đã không thêm bảng vào main; bằng chứng control nằm ở bảng pilot trong supplement (đã thêm phần giải thích). |
| M4 | `theory.tex` | (a) `\Cref{as:cont}` (Assumption 5 continuity) thừa và bị dùng sai trong chứng minh Thm 9.2; (b) `g(0,σ)=0` dư; (c) Thm 9.9(c) nói "Bonferroni/FDR" còn Cor 9.10 nói "family-wise" (FDR ≠ FWER) và Θ vs O; (d) Prop 9.5/Thm 9.4 phát biểu theo τ đầy đủ | Supplement đã cung cấp π(τ), quy tắc sabotage, M≥1347, Wilson đúng, và Δ_place; nhưng **câu chữ trong main vẫn như cũ**. Muốn khép hẳn thì cần ~6 dòng sửa trong `theory.tex`. |
| M5 | `related_work.tex` | vẫn còn "**first** environment purpose-built" | Supplement chỉ cảnh báo κ; chưa hạ giọng claim "first" (thuộc main). |

Tôi **không** đụng vào 5 mục này. Nếu bạn muốn, tôi có thể làm **bản diff tối thiểu** cho main (chỉ M1 bắt buộc để hết `(??)`, phần còn lại tuỳ bạn) — chỉ cần bạn cho phép sửa main.

## 3. Việc còn lại (ngoài source)

- **Build lại PDF**: `main.pdf` / `main_supplement.pdf` chưa build lại trong phiên này vì MiKTeX
  trên máy đang hỏng sau lần update (`pdflatex.fmt` thiếu, `kpsewhich latex.ltx` trả rỗng dù file
  tồn tại, `initexmf --dump=pdflatex` fail, mỗi lệnh TeX cố auto-install qua mạng rồi treo).
  Cần: MiKTeX Console → *Update package database* → *Refresh file name database* → *Rebuild
  formats*, rồi chạy `aamas2027\build_all.bat`.
- Sau khi build: kiểm tra supplement hiện **Table S1…, Figure S1…** (prefix S) và chạy lại
  `check_sources.py`.
- Còn 2 việc nội dung ngoài source: chèn **URL repo ẩn danh**, và đối chiếu CFP AAMAS 2027 về
  ethics / acks / AI-usage disclosure (appendix `AI-Assisted Preparation` đã có sẵn).

## 4. File thay đổi trong lần này

Chỉ supplement: `main_supplement.tex`, `appendix/supplement.tex`, `appendix/proofs.tex`,
`appendix/additional_experiments.tex`, `appendix/clarifications.tex` (mới),
`check_sources.py` (công cụ kiểm tra).
Không đổi: `main.tex`, `preamble.tex`, `sections/*`, `figures/*`, `tables/*`,
`references_verified.bib`.
