# Kế hoạch sửa paper MASGym (21–24/11/2026)

Múi giờ: Asia/Bangkok (UTC+07:00). Hạn cuối: **Thứ Ba 24/11, 22:00**.

**Chú thích**
- Ưu tiên: **P0** = bắt buộc, **P1** = nên làm, **P2** = làm nếu còn thời gian.
- R1/R2/R3 = nhận xét 1/2/3; số đi kèm là số thứ tự điểm (Con = Concern).
- `←` chỉ task phải xong trước.

---

## Tối nay (Thứ Sáu 20/11), hạn 00:15

- [ ] **T01 · P0 · Lập bảng nhận xét → hành động** (0.3h) — R1, R2, R3
  Mỗi điểm gán một nhãn: Chạy thí nghiệm / Viết lại / Hạ claim / Chấp nhận là limitation.
- [ ] **T02 · P0 · Bật chạy qua đêm baseline không-phòng-thủ cho 4 backbone** (0.3h) — R3-Con2
  Cùng protocol, task, attack template và seed với bản có phòng thủ hiện tại.

---

## Ngày 1, Thứ Bảy 21/11: Số liệu và thí nghiệm lõi

**Sáng (hạn 12:00)**
- [ ] **T03 · P0 · Thu kết quả baseline không-phòng-thủ** (1.0h) — R3-Con2 — `← T02`
  Nếu chưa chạy xong: dùng subset và ghi rõ phạm vi vào Limitations.
- [ ] **T04 · P0 · Sửa mâu thuẫn dãy 41.6 → 31.8 → 27.6** (1.5h) — R3-Con7
  Gán đúng nhãn action-channel (không phải system-level) trong bài chính; cập nhật CI trong bảng chính cho khớp supplementary.

**Chiều (hạn 18:00)**
- [ ] **T05 · P0 · Tính lại CI cluster-aware** (3.0h) — R3-Con6 — `← T03`
  Bootstrap theo episode; thêm hiệu chỉnh đa so sánh (Holm hoặc BH); cập nhật mọi bảng và hình dùng CI.
- [ ] **T06 · P0 · Ablation availability rule** (3.0h) — R3-Con1
  Báo cáo kết quả có và không có luật "orchestrator bị compromise ở star/tree → fail". Tách "fail theo định nghĩa" khỏi "fail do hành vi mô hình".

**Tối (hạn 22:00)**
- [ ] **T07 · P0 · Bổ sung script thiếu vào supplementary** (1.5h) — R2-4 — `← T05`
  Đưa `make_defense_table.py` và mọi script được nhắc trong bài; chạy lại để xác nhận tái tạo đúng các bảng.

---

## Ngày 2, Chủ Nhật 22/11: Thí nghiệm bổ sung và lý thuyết

**Sáng (hạn 12:00)**
- [ ] **T08 · P0 · Thí nghiệm collusion có kiểm soát (simulator)** (3.0h) — R3-Con3
  Cố định số attacker và vị trí, chỉ thay đổi mức phối hợp; chạy trên 4 topology (star, chain, tree, mesh).
- [ ] **T09 · P1 · Độ nhạy θ + mô hình lan truyền thay thế** (2.5h) — R2-2
  Quét θ; thêm một mô hình lan truyền khác (xác suất/cascade). Mô tả mô hình ngưỡng là cách điệu, không tuyên bố phản ánh thực tế.

**Chiều (hạn 18:00)**
- [ ] **T10 · P0 · Rà định lý và ghi tường minh giả định** (3.0h) — R3-Con3, R3-Con4
  Liệt kê homogeneity/determinism và các điều kiện còn thiếu cho từng định lý. Viết lại Thm 9.7 thành "ảnh hưởng của vị trí seed", không gọi là collusion.
- [ ] **T11 · P1 · Viết lại phần metric characterization / evaluator integrity** (1.5h) — R3-Con4 — `← T10`
  Nêu rõ kết quả này không chứng minh predicate đúng hay tương tác mô phỏng thực tế.

**Tối (hạn 22:00)**
- [ ] **T12 · P2 · (Tùy chọn) Kiểm tay 30–50 trace đối chiếu với checker** (2.0h) — R3-Con4
  Ghi tỉ lệ khớp làm bằng chứng cho tính đúng của security predicate.

---

## Ngày 3, Thứ Hai 23/11: Viết lại cấu trúc

**Sáng (hạn 12:00)**
- [ ] **T13 · P0 · Dựng dàn ý mới 9 mục** (1.0h) — R1, R2
  Intro → Overview MASGym → Notation → Threat model → Metric → Lý thuyết → Thực nghiệm → Related work → Limitations.
- [ ] **T14 · P0 · Viết Overview MASGym** (2.5h) — R1-1, R1-4 — `← T13`
  Một hình tổng quan, một task chạy mẫu, và quy trình của nhà nghiên cứu (chọn task → topology → adversary → chạy → đọc báo cáo). Đưa lên trước các phần cơ chế chi tiết.

**Chiều (hạn 18:00)**
- [ ] **T15 · P0 · Bảng notation/thuật ngữ + định nghĩa tại lần dùng đầu** (2.0h) — R2-6, R2-7, R2-8, R2-9 — `← T13`
  NRP, PNA, ASR, Φ, Ψ, TCB. Không dùng ký hiệu trước khi định nghĩa (đặc biệt câu mở đầu Intro và Mục 3.2).
- [ ] **T16 · P0 · Làm rõ threat model: orchestrator trusted vs compromised** (1.0h) — R2-10 — `← T13`
  Nêu rõ ở bối cảnh nào orchestrator được xem là trusted (TCB) và ở bối cảnh nào bị compromise.

**Tối (hạn 22:00)**
- [ ] **T17 · P0 · Rút gọn lý thuyết và giảm phụ thuộc supplementary** (3.0h) — R2-3, R2-5 — `← T10`
  Giữ 3–4 định lý chính, phát biểu bằng lời đơn giản kèm ý tưởng chứng minh; phần còn lại sang appendix. Giảm số lần dẫn supplementary từ 21 xuống khoảng 5.
- [ ] **T18 · P0 · Viết lại Related work + bảng so sánh benchmark** (2.5h) — R1-2, R1-3 — `← T13`
  Bảng so sánh: multi-agent? forced coordination? topology? adversary model? global checker? Cắt trùng lặp giữa abstract/intro/related work; bỏ bớt phần "MASGym không phải là gì".
- [ ] **T19 · P0 · Hạ claim CoRB và viết Limitations / threats to validity** (1.5h) — R3-Con5
  CoRB = giao thức đề xuất, minh họa trên simulator. Nêu rõ: một task family, một attack template, một defense, chưa có tool backend thật.
- [ ] **T20 · P2 · (Tùy chọn) Pareto security–cost nhỏ trên simulator** (2.0h) — R3-Con5 — `← T19`
  Chỉ làm nếu T17–T19 đã xong.

---

## Ngày 4, Thứ Ba 24/11: Chuẩn hóa và nộp

**Sáng (hạn 12:00)**
- [ ] **T21 · P0 · Viết lại abstract** (1.0h) — R2-6 — `← T19`
  Không dùng viết tắt chưa định nghĩa; không dùng ký hiệu có subscript; khớp với claim đã hạ.
- [ ] **T22 · P0 · Kiểm tra claim – bằng chứng** (1.5h) — R3-Con7 — `← T21`
  Mọi con số và câu khẳng định trong abstract/intro phải khớp bảng và supplementary.

**Chiều (hạn 18:00)**
- [ ] **T23 · P0 · Chạy lại toàn bộ script trong môi trường sạch** (1.5h) — R2-4 — `← T07, T22`
  Xác nhận tái tạo được mọi bảng và hình trong bài.
- [ ] **T24 · P0 · Soạn bảng phản hồi reviewer** (2.0h) — R1, R2, R3 — `← T22`
  Mỗi nhận xét → thay đổi đã làm → vị trí trong bài. Điểm không làm được thì nêu rõ và trỏ tới Limitations.

**Tối**
- [ ] **T25 · P1 · Nhờ người chưa đọc bản cũ đọc lướt Mục 1–3** (1.0h, hạn 21:00) — R1, R2 — `← T21`
  Ghi lại chỗ còn khó hiểu và sửa nhanh.
- [ ] **T26 · P0 · Rà lần cuối và nộp** (1.0h, hạn 22:00) — `← T23, T24, T25`
  Kiểm tra định dạng, tham chiếu chéo, số trang; nộp bản sửa và bảng phản hồi.

---

## Phương án dự phòng

- **Chạy LLM thật chậm hoặc tốn:** chạy baseline trên subset và nêu rõ phạm vi. Nếu vẫn không đủ, đổi câu khẳng định từ "phòng thủ cải thiện" thành "quan sát 0/1075 dưới phòng thủ" và không gán nguyên nhân.
- **Thiếu thời gian cuối ngày 3:** ưu tiên cấu trúc và sửa số liệu hơn Pareto của CoRB (T20).
- **Phản biện lý thuyết:** đừng làm lý thuyết phức tạp hơn; làm rõ giả định và đơn giản hóa cách phát biểu.