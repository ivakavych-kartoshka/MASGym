# Bản sửa: architecture vào main, cắt Related Work + proofs xuống supplement

## 1. Kết quả cuối (đã build lại và đo)

| | Giá trị |
|---|---|
| `main.pdf` | **10 trang** |
| Body (phần tính vào giới hạn 8 trang) | **trang 1–8**, kết thúc bằng §12 Conclusion ở cuối trang 8 ✅ |
| References | bắt đầu **trang 9**, hết ở trang 10 |
| Figure trong main | **2: Figure 1 = architecture, Figure 2 = 4 panel kết quả** |
| Table trong main | 1 (defense study) |
| `main_supplement.pdf` | **13 trang** |
| `undefined reference` (main + supplement) | **0** |
| `multiply defined label` | **0** |

Kiểm tra tĩnh: `python aamas2027\check_sources.py` → **all static checks pass**.
Kiểm tra số trang: `python aamas2027\pagecheck.py main.pdf`.

## 2. Đã đưa vào main

- **Architecture** (`figures/tikz_architecture.tex`) — nay là **Figure 1**, `\input` trong
  `main.tex` ngay sau §7; §7 mở đầu bằng `\Cref{fig:architecture}`. Figure kết quả thành **Figure 2**.
- Sửa luôn vài lỗi ở main:
  - `\Cref{sec:limitations}` (label không tồn tại, in ra `(??)`) → `\Cref{sec:discussion}`.
  - Cor 9.10 `Θ(...)` → `O(...)`; Thm 9.9(c) bỏ "FDR"; RQ4 `Θ` → `O`.
  - §11 thay 4 dòng bằng **mục Limitations 5 điểm** (đúng yêu cầu review).
  - §12 Conclusion viết lại, nói rõ defense efficacy **không được nhận diện**.
- Để vừa 8 trang: rút gọn §2 (Related Work), §10.3/§10.4/§10.5, introductory contributions;
  Figure 2 thu nhỏ chiều cao panel `4.0cm → 2.9cm`; caption Bảng 1 gọn lại.

## 3. Đã chuyển xuống supplement

| Nội dung | Từ | Đến |
|---|---|---|
| **Positioning** (§2.4 cũ) | `sections/related_work.tex` | gộp vào `appendix/related_work_supp.tex` |
| **Multi-agent defenses + Byzantine antecedents**, mixing/debating designs | `sections/related_work.tex` | **Appendix C: Related Work in Full** (`appendix/related_work_supp.tex`) |
| **6 chứng minh**: reduction (Prop 9.1), judge hijack (Prop 9.5), collusion (Thm 9.7 bản đầy đủ), forced coordination (Prop 9.8), concentration (Thm 9.9), sweep budget (Cor 9.10) | `sections/theory.tex` | **Appendix B: Proofs of the Main Results** (`appendix/main_results_proofs.tex`), kèm §B.1 về độ phân giải thống kê |
| Chi tiết limitations (bằng chứng floor effect, multiplicity, coverage) | main | `appendix/supplement.tex` (mục Threats to validity) |

Ở main mỗi phát biểu bị chuyển ghi **"Proof in the Supplementary Material."** Giữ trong main 2
chứng minh ngắn và là đóng góp cốt lõi: metric characterization (Thm 9.2) và evaluator integrity
(Thm 9.4).

## 4. Cấu trúc supplement

```
A  Proofs of the Restated Propagation Results
B  Proofs of the Main Results            (chuyển từ main)
C  Related Work in Full                  (chuyển từ main)
D  Supplementary Material: Notation, Desiderata, and Cost
E  Clarifications of Main-Text Statements (π(τ), quy tắc sabotage, Δ_place, thống kê)
F  Extended Protocol and Additional Synthetic-Model Studies
G  AI-Assisted Preparation
```
Float của supplement đánh số **S1, S2, …** (Table S1–S11) nên không lẫn với main.

## 5. Ghi chú

- Nếu mở `main.pdf` bằng Foxit/Adobe thì **đóng viewer trước khi build**, nếu không pdflatex
  báo `I can't write on file 'main.pdf'` và PDF cũ vẫn còn (đã gặp một lần trong phiên này).
- Build: `aamas2027\build_all.bat`.
- Cảnh báo `natbib: Citation ... multiply defined` trong log supplement là do `xr` nạp `main.aux`,
  không phải label trùng, không ảnh hưởng bản in.
