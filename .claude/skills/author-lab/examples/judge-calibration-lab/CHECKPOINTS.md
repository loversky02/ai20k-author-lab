# CHECKPOINTS — Ví dụ – Hiệu chỉnh LLM-as-judge với nhãn người

Mỗi checkpoint: làm → tự kiểm tra → commit `CPx: <một dòng>`. Tự kiểm tra **không phải chấm điểm**; nó chỉ báo bạn đã có đủ sản phẩm để đi tiếp.

Phân công trong nhóm (xem TEAM.md): CP2 do **Metrics** làm, CP3 do **Bias** làm, cả nhóm làm CP1, CP4, CP5. Người không làm bước đó vẫn phải chạy được lệnh tự kiểm tra của bước đó.

## CP0 — Chuẩn bị (trước buổi học, không tính giờ)

**Cần làm:** clone repo nhóm, chạy preflight trên máy mỗi người.
**Tự kiểm tra:** `python3 scripts/run_eval.py --judge v1` → `judge=v1  n=60  accuracy=0.750  kappa=CHƯA CÀI (CP2)`

## CP1 — Đọc judge và chạy baseline (15 phút) · Dùng

**Cần làm:** đọc `judge_v1` và `pairwise_v1` trong `src/judge.py`, đọc `accuracy()` trong `src/metrics.py`. Chạy baseline, mở `results/judge_run_v1.json`, xem mục `disagreements`.
**Sản phẩm:** `results/judge_run_v1.json`
**Cần hiểu:** judge v1 sai 15/60 câu. Trong 15 câu đó, judge nói `fail` khi người nói `pass` bao nhiêu lần, và ngược lại? Vì sao một judge "đúng 75 %" vẫn có thể tệ?
**Tự kiểm tra:** `python3 scripts/run_eval.py --judge v1` → `accuracy=0.750  ... disagreements=15`
**Bị kẹt?** Mở một câu trong `disagreements`, tìm câu đó trong `data/answers.jsonl` theo `id`, so `answer` với `reference`: judge v1 đòi đủ mọi số trong reference.
Commit: `CP1: baseline judge v1`

## CP2 — Confusion matrix và Cohen's kappa (30 phút) · Sửa

**Cần làm:** cài `confusion()` và `cohen_kappa()` trong `src/metrics.py`. Docstring có công thức và trường hợp biên; 8 test trong `tests/test_metrics.py` nói chính xác kết quả cần trả về.
**Sản phẩm:** `src/metrics.py`
**Cần hiểu:** test `test_constant_judge_is_zero` — judge luôn nói `pass` đúng 75 % mà kappa = 0. Vì sao?
**Tự kiểm tra:** `python3 -m unittest tests.test_metrics -v` → `Ran 8 tests ... OK`; rồi chạy lại `python3 scripts/run_eval.py --judge v1` → `kappa=` là một số.
**Bị kẹt?** Tính tay test `test_textbook_value`: p_o = (20 + 15) / 50; p_e = P(người pass) × P(judge pass) + P(người fail) × P(judge fail).
Commit: `CP2: confusion matrix and kappa`

## CP3 — Swap test cho judge so cặp (25 phút) · Sửa

**Cần làm:** cài `is_consistent()` trong `scripts/swap_test.py` rồi chạy. Mở `results/swap_test.json`, xem `inconsistent_ids` và các dòng tương ứng trong `rows`.
**Sản phẩm:** `scripts/swap_test.py`, `results/swap_test.json`
**Cần hiểu:** `human_agreement` và `consistency` khác nhau thế nào? Một judge có thể đồng ý với người ở phần lớn cặp mà vẫn lệch vị trí không?
**Tự kiểm tra:** `python3 scripts/swap_test.py` → `n_pairs=30  consistency=` một số nhỏ hơn `1.000`
**Bị kẹt?** Lần đầu judge thấy (a, b) và trả `A` nghĩa là chọn a. Lần hai judge thấy (b, a); nếu vẫn chọn a thì nó trả chữ nào?
Commit: `CP3: swap test`

## CP4 — Phân tích lỗi theo slice và judge v2 (40 phút) · Tự làm

**Cần làm:**
1. Mỗi người lấy slice của mình (TEAM.md), lọc `disagreements` của `results/judge_run_v1.json` theo slice, viết `submission/INDIVIDUAL/<MSSV>.md` theo `_TEMPLATE.md` (≥ 3 id, loại lỗi, câu trích).
2. Cả nhóm gộp các loại lỗi, chọn cách sửa, viết `judge_v2` trong `src/judge.py`. Chỉ sửa `judge_v2` và hàm phụ mới.
3. `python3 scripts/run_eval.py --judge v2`.
**Sản phẩm:** `submission/INDIVIDUAL/<MSSV>.md` (mỗi người), `src/judge.py`, `results/judge_run_v2.json`
**Cần hiểu:** sửa judge trên chính 60 câu rồi đo lại trên 60 câu đó thì kappa mới nói được gì, không nói được gì?
**Tự kiểm tra:** `python3 check.py` → các dòng `judge_run_v2.json` và `<MSSV>.md` có ✓
**Bị kẹt?** Bắt đầu bằng loại lỗi xuất hiện nhiều nhất trên cả 3 slice. Sửa một loại, chạy lại, xem kappa đổi bao nhiêu trước khi sửa loại tiếp theo.
Commit: `CP4: error analysis and judge v2`

## CP5 — Báo cáo nhóm (20 phút) · Tự làm

**Cần làm:** điền `submission/REPORT.md`: bảng v1/v2 (tổng và theo slice), ma trận nhầm lẫn, swap test, mục "Con số này không chứng minh". Số chép từ `results/`, 2 chữ số thập phân.
**Sản phẩm:** `submission/REPORT.md`
**Cần hiểu:** nếu ngày mai bộ câu hỏi đổi sang chính sách khác, phần nào của judge v2 còn dùng được?
**Tự kiểm tra:** `python3 check.py` → dòng `REPORT.md có đủ số đo khớp results/` có ✓
**Bị kẹt?** Mở RUBRIC §4 R6, mức Adequate: đó là danh sách tối thiểu.
Commit: `CP5: team report`
