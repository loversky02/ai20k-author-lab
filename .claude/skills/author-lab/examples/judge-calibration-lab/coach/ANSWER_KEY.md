# ANSWER_KEY — Ví dụ – Hiệu chỉnh LLM-as-judge  (PRIVATE)

Lời giải mẫu: `coach/reference/` · Dữ liệu tạo bằng: `python3 coach/make_data.py` (tất định, không seed ngẫu nhiên) · Đo ngày: 13/10/2026.

## Theo từng tiêu chí

| ID | Bằng chứng mong đợi | Biến thể chấp nhận | Sai nhưng trông hợp lý (điểm, đã đo) | Dung sai |
|---|---|---|---|---|
| R1 | 8/8 test; kappa v1 = 0.508 | cách viết bất kỳ qua 8 test | chia p_e cho n − 1 → 6/8 (15) · quên trường hợp p_e = 1 → 7/8 (15) | test so tới 1e-6 |
| R2 | hai file tái lập; v1 accuracy 0.750 | v2 = v1 vẫn hợp lệ | sửa tay 1 verdict → R2 7, R4 0, grader cảnh báo §5 | so đúng từng verdict |
| R3 | consistency 0.700, first_position_rate 0.600, human_agreement 0.900; 9 cặp lệch p03 p07 p13 p23 p24 p27 p28 p29 p30 | — | `is_consistent` đảo (`==`) → consistency 0.300 (5) | 1e-4 |
| R4 | v2 kappa 0.931, Δ +0.423 | mọi v2 tất định có Δ ≥ 0.10 | chỉ hạ ngưỡng số liệu → kappa 0.53 (5) · chỉ bắt câu thô lỗ → 0.544 (5) · không sửa v2 → Δ 0 (0) | kappa của coach |
| R5 | ≥ 3 id lỗi v1 đúng slice, câu trích nguyên văn: A = a01 a10 a19 a35 a44 a53 · B = a04 a38 a40 · C = a21 a34 a41 a43 a48 a59 | loại lỗi khác nếu câu trích ủng hộ | slice B chỉ có đúng 3 id: thiếu một là Chưa đạt | — |
| R6 | bảng như `coach/reference/submission/REPORT.md` | — | "human_agreement 0.90 nên judge tốt" mà không nhắc cặp hoà → tối đa Adequate | số khớp `results/` |
| B1 | giữ lại một slice, có SHA lúc đo | — | đo held-out sau khi đã sửa theo slice đó → không phải held-out (0) | — |

Mẫu bài làm cho R5/R6: `coach/reference/submission/`, `coach/reference/TEAM.md`, `coach/reference/CONTRIBUTIONS.md`.

## Kiểm tra sẵn sàng chấm

| Kiểm tra | Điểm ra | Kỳ vọng |
|---|---|---|
| Template trống | 0/65 | ≈ 0 |
| Lời giải mẫu | 65/65 (+ R5 20, R6 15 theo bài mẫu) | 100 |
| Bài yếu mẫu: CP2 + CP3 xong, không sửa v2 | 55/65 | R4 = 0 |
| CP2 có lỗi, chưa làm CP3 | 30/65 | R1 15, R3 0 |

## Nhật ký bất đồng giữa người chấm

| Ngày | Bài (mã ẩn danh) | Tiêu chí | Chấm A | Chấm B | Phán quyết | Quy tắc mới |
|---|---|---|---|---|---|---|
| | | | | | | |
