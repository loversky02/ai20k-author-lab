# LAB_SPEC — Ví dụ – Hiệu chỉnh LLM-as-judge với nhãn người

Tài liệu thiết kế cho coach. Trạng thái: **đã review, chưa dry run** (lab mẫu của skill `author-lab`).

## 0. Thẻ lab

| Mục | Giá trị |
|---|---|
| Ngày / track / slide nguồn | Ví dụ / Đánh giá hệ thống AI / "LLM-as-judge: bias và calibration" |
| Đối tượng, trình độ | học viên AI20K, đọc được Python, chưa cài kappa bao giờ |
| Thời lượng trên lớp / ngoài giờ | 180 phút / cài đặt trước buổi (chỉ cần Python ≥ 3.10) |
| Hình thức | nhóm 3 (2–4), mỗi người một slice A/B/C |
| Môi trường | local, stdlib, zero-key |
| Cách chấm | script (R1–R4, 65 điểm) + người theo mốc (R5, R6, B1) |
| Mức dùng AI | được dùng, phải khai báo, vấn đáp được |
| Hạn nộp | 23:59 20/10/2026 (GMT+7) |
| Câu hỏi mở (ai quyết, khi nào) | không có |
| Phiên bản lab | v1 (13/10/2026), bản đầu |

### 0b. Phiên bản & nguồn

| Công cụ | Phiên bản pin | Ngày kiểm tra | Nguồn chính thức (URL) | Smoke test | Phương án dự phòng |
|---|---|---|---|---|---|
| Python (chỉ stdlib) | ≥ 3.10 | 13/10/2026 | https://docs.python.org/3/ | đã chạy 13/10 (macOS); Windows, Colab: chưa | không cần: không có gói ngoài, không cần key |

## 1. Mục tiêu

Xem README §Mục tiêu học tập (O1–O4). Không chép lại để tránh lệch.

## 2. Bảng căn chỉnh

| Mục tiêu | Bước luyện | Tiêu chí chấm | Bằng chứng |
|---|---|---|---|
| O1 | CP1, CP2 | R1, R2 | tests cố định; `results/judge_run_v1.json` |
| O2 | CP3 | R3, R6 | `results/swap_test.json`; REPORT mục Swap test |
| O3 | CP4 | R5 | `submission/INDIVIDUAL/<MSSV>.md` |
| O4 | CP4, CP5 | R4, R6, B1 | `results/judge_run_v2.json`; REPORT |

Mục tiêu không có tiêu chí: không có. Tiêu chí không có mục tiêu: không có.

## 3. Rubric

Đã chuyển sang RUBRIC.md. Ngưỡng D lấy từ số đo (xem §6 và `coach/ANSWER_KEY.md`).

## 4. Các bước

Đã chuyển sang README §Các bước và CHECKPOINTS.md. Tổng 150 / 180 phút (buffer 17 %). Giờ là ước lượng, **chưa dry run**.

## 5. Quyết định thiết kế

| Quyết định | Phương án bị loại | Lý do |
|---|---|---|
| Judge là hàm luật tất định, không gọi LLM | gọi API LLM thật | zero-key, chạy lại được từng verdict; cơ chế lỗi (vị trí, thiếu số) vẫn giống judge LLM |
| Người chấm chạy lại judge và so từng verdict | tin số trong `results/` | chặn sửa tay `results/` mà không cần đọc code |
| R4 tính kappa bằng metrics của coach | dùng `src/metrics.py` của nhóm | sai kappa chỉ mất điểm một lần (R1) |
| Ngưỡng R4 Δ ≥ 0.10 | Δ > 0 | một sửa đổi đơn lẻ chỉ tăng 0.02–0.04 (đo); 0.10 buộc phân tích ≥ 2 loại lỗi |
| Mỗi người một slice, viết INDIVIDUAL riêng | một báo cáo nhóm duy nhất | điểm cá nhân có bằng chứng riêng; slice B cố ý chỉ có 3 lỗi v1 |
| Ô học viên điền dùng `_(điền)_` | `<FILL>` | `<FILL>` là lỗi soạn đề với `lint_lab.py`, không được còn khi phát hành |
| Không có điểm sàn | sàn 30 điểm cho bài có nộp | template trống phải ra 0 để kiểm soát âm tính có nghĩa |

## 6. Kiểm tra sẵn sàng chấm

| Kiểm tra | Kết quả | Ngày |
|---|---|---|
| Template trống qua grader ≈ 0 | `coach/grade_d.py --template` → 0/65; `check.py` → CHƯA SẴN SÀNG: 8 mục | 13/10/2026 |
| Lời giải mẫu từ template = điểm tối đa | `coach/grade_d.py --solution coach/reference` → 65/65; `check.py --solution coach/reference` → SẴN SÀNG NỘP | 13/10/2026 |
| Sửa tay 1 verdict trong `judge_run_v2.json` | R2 = 7, R4 = 0, grader in cảnh báo §5 | 13/10/2026 |
| Exploit: `swap_test.json` viết tay, `is_consistent` chưa cài | R3 = 0 | 13/10/2026 |
| Exploit: đổi `JUDGES["v1"]` rồi chạy lại run_eval | R2 = 7, R4 = 0 | 13/10/2026 |
| Bài dở dang: JSON hỏng / thiếu trường / xoá `src/judge.py` | báo ✗, không traceback | 13/10/2026 |
| `lint_lab.py` 0 ERROR | 0 ERROR, 0 WARN | 13/10/2026 |
| 2 người chấm 3–5 bài mẫu, lệch ≤ ngưỡng | CHƯA LÀM | |
| Dry run đo giờ thật | CHƯA ĐO | |
