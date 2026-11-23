# Bản Rebuttal AAMAS 2027 (Tiếng Việt — Đối chiếu duyệt trước khi nộp)

> **Lưu ý giới hạn 2.500 ký tự:** Bản tiếng Anh tương ứng tại [rebuttal_EN.md](file:///d:/Documents/NCKH/MASGym/aamas2027/rebuttal_EN.md) đã được căn chuẩn **≤ 2.500 ký tự cho mỗi khối**. Dùng **Phần 1–4** nếu OpenReview có ô trả lời riêng từng reviewer + phản hồi chung, hoặc dùng **Phần 5** nếu OpenReview chỉ có 1 ô rebuttal duy nhất tối đa 2.500 ký tự.

---

## 1. Phản hồi chung (General Response)

Chúng tôi cảm ơn cả ba phản biện đã đóng góp các nhận xét chi tiết và mang tính xây dựng. Thay vì bảo vệ các khẳng định quá mạnh, trong thời gian rebuttal chúng tôi đã chạy bổ sung các thí nghiệm nhắm đúng trọng tâm (baseline LLM không phòng thủ cùng protocol, ablation bỏ luật availability, thí nghiệm collusion cố định vị trí, độ nhạy mô hình lan truyền, khoảng tin cậy cluster-aware và sửa lỗi CoRB) cùng kế hoạch tái cấu trúc bài viết cụ thể.

**Tóm tắt kết quả thực nghiệm mới & đính chính:**
1. **Ablation luật availability (pE9X, Xdct):** Khi tắt luật fail cứng ở hub `star`/`tree`, hiện tượng bão hòa tầm thường 1.000 biến mất nhưng tỷ lệ hỏng hệ thống khác 0 vẫn duy trì do cạn k-quorum: ở chế độ 0% compliance (N=5, M=30), $\text{ASR}_{\text{sys}}$ khi collusion giảm từ 1.000 xuống 0.300 `[0.167, 0.479]` trên `star` và `tree` (`chain` 0.000, `mesh` 0.433). Trên synthetic degradation (M=738, star), bỏ luật hub phân tách rõ các defense (colluding: no-defense 0.657, fixed-threshold 0.539, guardrail 0.424).
2. **Baseline LLM không phòng thủ cùng protocol (pE9X):** Trên đúng seed N=5, M=30 (1.075 quyết định, 0 parse failures), `Llama-3.2-1B` comply 1.075/1.075 khi không defense (trùng bản có defense: ceiling effect). Do AWS Bedrock chuyển `mistral-7b-instruct-v0:2` sang Legacy trong thời gian review, chúng tôi chạy đủ cặp `none` vs `delimiting` trên bản kế nhiệm đang active là `Ministral-3-8B-Instruct`: compliance đều là 0/1.075 ở cả hai chế độ (floor effect), còn `delimiting` làm tăng +26.3% chi phí token (213 → 269 tokens/lượt). Chúng tôi sẽ bỏ cách viết nhân quả "drives compliance to 0/1,075" và nêu rõ phạm vi floor/ceiling effect.
3. **Controlled collusion (pE9X):** Đổi tên Định lý 9.7 thành *Seed Placement Advantage* và tách riêng yếu tố phối hợp khi cố định số attacker ($s=2$) và vị trí đặt seed trên cả 4 topology (M=738): phối hợp hành động tăng $\text{ASR}_{\text{act}}$ thêm +0.270 đến +0.428 và phối hợp tách payload tăng thêm +0.104 đến +0.232 (mọi $p_{\text{Holm}} = 0.0016$).
4. **Cluster-aware CI & đồng bộ số liệu (pE9X):** Xem 360 episode (trung bình 2.986 quyết định/ep) là các cụm với trường hợp thận trọng nhất cho greedy decoding ($\text{ICC}=1$) cho cận trên 95% là 0.0106 (Bonferroni-12: 0.0223) thay vì 0.0036. Đính chính chuỗi 41.6% → 31.8% → 27.6% là trên action-channel ($\text{ASR}_{\text{act}}$), đồng bộ Wilson CI hai phía (`[0,0.114]`, `[0.274,0.608]`, `[0.886,1]`) và nêu rõ mức co hẹp giữa các cột chưa đủ ý nghĩa thống kê ở M=738.
5. **Tái cấu trúc & tự đủ (Go5y, Xdct):** Đưa System Overview + ví dụ task cụ thể lên Mục 2, giảm dẫn chiếu Supplement từ 21 xuống ≤5, định nghĩa mọi ký hiệu ở lần dùng đầu, tách rõ trusted harness (TCB) với tác tử Orchestrator có thể bị compromise, và đóng gói kèm `make_defense_table.py`.

---

## 2. Trả lời Reviewer Go5y

Cảm ơn phản biện đã góp ý rõ ràng và thiết thực về bố cục và tính dễ đọc. Chúng tôi đồng ý rằng cấu trúc hiện tại khiến người đọc phải nhảy qua lại giữa các mục và che khuất quy trình sử dụng thực tế của nhà nghiên cứu đằng sau các định nghĩa hình thức.

**1. Đưa Tổng quan MASGym & Quy trình thực tế lên đầu (Nhận xét 1 & 4):**
Trong bản sửa, chúng tôi sẽ đưa kiến trúc tổng thể và luồng làm việc từ Mục 7 lên **Mục 2 (MASGym Overview & Researcher Workflow)** ngay sau Phần Giới thiệu:
- **Hình kiến trúc end-to-end** đi kèm 5 bước sử dụng cho nhà nghiên cứu: (i) chọn bài toán forced-coordination cùng các vị từ tất định (Psi, Phi), (ii) chọn topology (`star`/`chain`/`tree`/`mesh`) và số agent $N$, (iii) cấu hình vector kẻ tấn công $c_{\text{adv}} = (\beta, \text{coll}, \text{adapt}, \text{orch}, \text{tool}, \text{syb}, \text{mem})$ và phòng thủ blue, (iv) chạy các episode cố định seed qua `LLMBackboneAdapter` hoặc bộ mô phỏng synthetic, và (v) đọc báo cáo theo dấu vết gồm `ASR_act`, `ASR_avail`, `ASR_sys`, `NRP_sys` kèm CI cluster-aware cấp episode.
- **Kịch bản bài toán cụ thể trong bài chính:** Chúng tôi đưa ví dụ mẫu 3-forced "travel-booking" (hiện nằm ở Phụ lục A.7) thẳng vào Mục 2. Ba worker riêng biệt phụ trách tra cứu lịch trình (calendar tool), đặt vé trong ngân sách (booking tool) và thanh toán (payment tool). Bài sẽ minh họa từng bước cách một tool độc chèn lệnh chuyển hướng người nhận tiền, cách Phi chỉ đọc các chuyển trạng thái đã ghi (bỏ qua văn bản hội thoại tự do), và cách một worker/orchestrator bị compromise có thể gây lỗi availability bằng cách giữ lại subtask bắt buộc.

**2. Bỏ trùng lặp & Làm rõ Related Work (Nhận xét 2 & 3):**
- Xóa các nội dung lặp lại giữa Abstract, Introduction và Related Work, đồng thời rút gọn các đoạn dài dòng về "MASGym không phải là gì".
- Thay phần tóm tắt mơ hồ bằng một **bảng so sánh gọn** đặt cạnh ASB, AgentDojo, InjecAgent, ToolEmu và MASGym theo 5 tiêu chí cụ thể: tương tác đa tác tử, forced coordination, topology giao tiếp, mô hình adversary tham số hóa (collusion/orchestrator/Sybil) và bộ kiểm tra trace tất định.
- Mọi ký hiệu đều được giới thiệu tuần tự trước khi dùng, kèm bảng ký hiệu gọn ở Mục 2 để bài chính đọc mạch lạc và tự đủ mà không cần mở Supplement.

---

## 3. Trả lời Reviewer Xdct

Cảm ơn phản biện đã đánh giá kỹ lưỡng. Chúng tôi trả lời trực tiếp từng điểm kỹ thuật và trình bày bằng các thí nghiệm ablation mới và phương án sửa cụ thể.

**1. "Kết quả chỉ phản ánh luật topology định nghĩa sẵn" (Nhận xét 1):**
Phản biện hoàn toàn đúng rằng luật availability cứng tại hub đã ép $\text{ASR}_{\text{sys}} = 1.000$ trên `star`/`tree` mỗi khi hub bị compromise. Chúng tôi đã chạy ablation tách rời lỗi hành động, lỗi cạn quorum và lỗi luật hub:
- Ở N=5, M=30 (chế độ 0% compliance), **bỏ luật hub cứng** làm $\text{ASR}_{\text{sys}}$ khi collusion giảm từ 1.000 xuống **0.300** `[0.167, 0.479]` trên `star` và `tree` (và 0.233 / 0.167 khi orchestrator bị compromise), trong khi `chain` giữ 0.000 và `mesh` 0.433 — cho thấy hỏng hệ thống do cạn k-quorum vẫn tồn tại rõ rệt mà không bị bão hòa.
- Trên synthetic degradation (M=738, star, $\beta=0.3$), bỏ luật hub gỡ hoàn toàn bão hòa 1.000 và phân tách rõ defense: `colluding` cho 0.657 (no-defense), 0.539 (fixed-threshold) và 0.424 (guardrail). Chúng tôi sẽ báo cáo song song cả hai chế độ cùng $\text{ASR}_{\text{act}}$.

**2. Mô hình lan truyền ngưỡng & độ nhạy $\theta$ (Nhận xét 2):**
Chúng tôi đồng ý quy tắc ngưỡng ("bị compromise khi $\ge \theta$ láng giềng vào bị compromise") là mô hình cấu trúc cách điệu, không phải khẳng định về lan truyền LLM ngoài thực tế. Chúng tôi đã chạy khảo sát độ nhạy ($N \in \{5,10\}$, $\beta=0.3$, M=738) so sánh `ThresholdCascade` ($\theta \in \{1,2,3\}$) với `IndependentCascade` ($p \in \{0.1,0.3,0.5\}$) và `LinearThreshold` ngẫu nhiên ($U(0,1)$):
- Với $\theta \ge 2$, đồ thị thưa (`chain`, `tree`, bậc vào tối đa 1) ngừng lan truyền hoàn toàn (CPR=0.000), còn `mesh` dày vẫn lan tới CPR=1.000 (kể cả $\theta=3, N=10$).
- Trên các mô hình ngẫu nhiên (IC $p=0.3$ và LT), trật tự dễ tổn thương mạng dày > mạng thưa (`mesh > star > tree/chain` theo CPR) vẫn được bảo toàn. Chúng tôi sẽ diễn đạt rõ đây là các mô hình phân tích cách điệu.

**3. Tính tự đủ, script thiếu, ký hiệu & TCB vs Orchestrator (Nhận xét 3–10):**
- **Tự đủ & lý thuyết:** Giảm dẫn chiếu Supplement từ 21 xuống ≤5, giữ 3–4 định lý chính phát biểu dễ hiểu kèm ý tưởng chứng minh và giả định tường minh, chuyển các hệ quả phụ sang Appendix.
- **Script:** Đóng gói đầy đủ `make_defense_table.py` (đã có trong repo) và `run_rebuttal_studies.py` vào gói supplementary.
- **Ký hiệu & TCB:** Bỏ viết tắt có subscript/chưa định nghĩa khỏi Abstract; định nghĩa NRP, PNA, ASR, $\Phi$, $\Psi$, TCB ngay lần đầu; tách bạch **khung thực thi tin cậy / trusted runtime harness (TCB)** (bộ ghi trace + checker tất định) với **tác tử LLM Orchestrator** (không tin cậy, có thể bị compromise).

---

## 4. Trả lời Reviewer pE9X

Cảm ơn phản biện đã đưa ra những nhận xét phương pháp luận cực kỳ sắc sảo. Mọi điểm nêu ra đều là điểm yếu thực sự; chúng tôi đã chạy các thí nghiệm nhắm đích để kiểm chứng và xử lý trung thực từng mục.

**1. Bão hòa do luật availability (Con 1):**
Chúng tôi đã chạy ablation tắt luật hub cứng ở `star`/`tree`. Tại N=5, M=30 (0% compliance), $\text{ASR}_{\text{sys}}$ khi collusion giảm từ 1.000 xuống **0.300** `[0.167, 0.479]` trên `star`/`tree` (0.233 / 0.167 cho comp. orch.), trong khi `chain`=0.000 và `mesh`=0.433; phần hỏng còn lại đến từ cạn k-quorum. Trên synthetic degradation (M=738, star), bỏ luật hub phân tách rõ defense (`colluding`: no-defense 0.657, fixed-threshold 0.539, guardrail 0.424). Chúng tôi sẽ báo cáo đồng thời `ASR_act`, `ASR_sys(no-hub)` và `ASR_sys(full)`.

**2. Đối chứng không phòng thủ cùng protocol (Con 2):**
Trên đúng seed N=5, M=30 (1.075 quyết định, 0 parse failures):
- **`Llama-3.2-1B` (`none`):** compliance 1.075/1.075 (trùng bản có defense: ceiling effect).
- **`Ministral-3-8B-Instruct` (Bedrock):** Vì AWS đã chuyển `mistral-7b-instruct-v0:2` sang Legacy trong lúc review, chúng tôi chạy đủ cặp `none` vs `delimiting` trên model kế nhiệm đang active: **0/1.075** compliance ở cả hai nhánh (floor effect, khớp pilot Qwen), trong khi `delimiting` tăng chi phí **+26.3%** (213 → 269 tokens/lượt).
Chúng tôi sẽ rút lại cách viết nhân quả "drives compliance to 0/1,075" và mô tả Bảng 1 đúng bản chất là chế độ zero-compliance vs full-compliance.

**3. Controlled collusion vs vị trí seed (Con 3):**
Đổi tên Định lý 9.7 thành *Seed Placement Advantage* (ở $s=1$, đặt trung tâm vs ngẫu nhiên tăng CPR thêm +0.134 `tree`, +0.122 `star`, +0.033 `chain`, -0.032 không có ý nghĩa trên `mesh`). Khi cố định số attacker ($s=2$), cố định vị trí (`random` hoặc `central`) và dùng chung một lượt lan truyền trên cả 4 topology (M=738), phối hợp thuần túy làm tăng $\text{ASR}_{\text{act}}$ thêm **+0.270 đến +0.428** (phối hợp hành động) và **+0.104 đến +0.232** (split-payload), mọi $p_{\text{Holm}}=0.0016$.

**4. Giả định lý thuyết, CoRB & phạm vi (Con 4 & 5):**
Ghi tường minh các giả định homogeneity/determinism/phép chiếu $\pi(\tau)$ và nói rõ tính toàn vẹn của checker không đồng nghĩa tính đúng của predicate. Chúng tôi cũng sửa bug tái sử dụng trạng thái blue-policy trong `run_corb_sweep.py` (blue khởi tạo mới, M=200: `chain_adaptive` $\text{ASR}_{\text{sys}}=0.310/\text{NRP}=0.635$; `star_adaptive` 0.415/0.521), thừa nhận mô hình chi phí synthetic chưa cộng overhead của defense (trái với mức +26.3% đo được trên LLM thật), và hạ claim CoRB xuống giao thức đề xuất có kiểm chứng synthetic.

**5. Cluster-aware CI & đồng bộ số liệu (Con 6 & 7):**
1.075 quyết định gom cụm trong 360 episode (2.986/ep). Dưới giả định thận trọng nhất cho greedy decoding ($\text{ICC}=1 \Rightarrow N_{\text{eff}}=360$), cận trên 95% cho 0-compliance là **0.0106** (Bonferroni-12: **0.0223**), không phải 0.0036. Đồng bộ CI hai phía cấp cell (`[0,0.114]`, `[0.274,0.608]`, `[0.886,1]`; Bonf-12: `[0,0.215]`, `[0.218,0.678]`, `[0.785,1]`), đổi nhãn 41.6% → 31.8% → 27.6% sang **`ASR_act`** và ghi rõ mức co hẹp giữa các bối cảnh chưa đủ phân giải ở M=738 ($p=0.083, 0.292$).

---

## 5. Bản gộp 1 ô duy nhất (Chỉ dùng nếu OpenReview giới hạn TỔNG cộng 2.500 ký tự cho cả 3 reviewer)

Chúng tôi cảm ơn các phản biện vì những nhận xét kỹ lưỡng. Trong thời gian rebuttal, chúng tôi đã chạy các thí nghiệm nhắm đích và lập kế hoạch sửa toàn diện cho mọi điểm chính.

**1. Ablation luật availability (pE9X, Xdct):** Tắt luật hub cứng ở `star`/`tree` gỡ bỏ bão hòa 1.000 tầm thường nhưng vẫn giữ phần hỏng do cạn k-quorum: ở N=5, M=30 (0% compliance), $\text{ASR}_{\text{sys}}$ khi collusion giảm từ 1.000 xuống **0.300** `[0.167,0.479]` trên `star`/`tree` (comp. orch.: 0.233/0.167; `chain` 0.000; `mesh` 0.433). Trên synthetic degradation (M=738, star), bỏ luật hub tách rõ các defense (`colluding`: no-defense 0.657, fixed-threshold 0.539, guardrail 0.424). Bài sẽ báo cáo đồng thời `ASR_act`, `ASR_sys(no-hub)` và `ASR_sys(full)`.

**2. Đối chứng không phòng thủ (pE9X):** Trên đúng seed N=5, M=30 (1.075 quyết định, 0 parse failures): `Llama-3.2-1B` comply 1.075/1.075 khi không defense (ceiling effect). Do AWS Bedrock khóa Legacy `mistral-7b-instruct-v0:2` trong lúc review, chúng tôi chạy đủ cặp `none` vs `delimiting` trên bản kế nhiệm active `Ministral-3-8B-Instruct`: 0/1.075 compliance ở cả hai nhánh (floor effect, khớp pilot Qwen) với chi phí tăng +26.3% token (213→269/lượt). Bài sẽ rút lại cách viết nhân quả ("drives compliance to 0/1,075") và trình bày Bảng 1 theo chế độ zero- vs full-compliance.

**3. Controlled collusion & độ nhạy lan truyền (pE9X, Xdct):** Đổi tên Định lý 9.7 thành *Seed Placement Advantage* và cô lập phối hợp thuần với số attacker cố định ($s=2$) và vị trí cố định trên 4 topology (M=738): phối hợp hành động tăng $\text{ASR}_{\text{act}}$ thêm +0.270..+0.428 và split-payload tăng +0.104..+0.232 (mọi $p_{\text{Holm}}=0.0016$). So sánh `ThresholdCascade` ($\theta=1..3$) với `IndependentCascade` ($p=0.1..0.5$) và `LinearThreshold` ($N=5,10$) xác nhận $\theta \ge 2$ dừng trên `chain`/`tree` thưa (CPR=0) còn `mesh` lan toàn mạng (1.0), và trật tự dày > thưa bảo toàn qua mô hình ngẫu nhiên; bài sẽ nêu rõ quy tắc ngưỡng là mô hình cách điệu.

**4. Cluster-aware CI, CoRB & đồng bộ số liệu (pE9X):** Xem 360 episode (2.986 qđ/ep) là cụm (ICC=1) cho cận trên 95% 0-compliance là 0.0106 (Bonf-12: 0.0223) thay vì 0.0036; đồng bộ cell CI về `[0,0.114]`/`[0.274,0.608]`/`[0.886,1]`. Đổi nhãn 41.6%→31.8%→27.6% sang **`ASR_act`** (co hẹp chưa đủ phân giải ở M=738: $p=0.083/0.292$), sửa bug tái dùng blue-policy trong `run_corb_sweep.py` và hạ CoRB xuống giao thức đề xuất có minh họa synthetic.

**5. Bố cục & rõ nghĩa (Go5y, Xdct):** Chuyển Overview + quy trình researcher + bài toán mẫu `travel-booking` lên Mục 2, thêm bảng so sánh Related Work, giảm dẫn Supplement (21→≤5), định nghĩa mọi viết tắt lần đầu, tách trusted harness (TCB) khỏi Orchestrator bị compromise, và đóng gói kèm `make_defense_table.py`.
