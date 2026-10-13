# RUNBOOK — Ví dụ – Hiệu chỉnh LLM-as-judge  (PRIVATE — không đưa vào repo học viên)

**Trạng thái:** nháp, **chưa dry run** · **Thời lượng:** 180 phút · **Coach:** (điền khi dùng thật)

## Trước buổi học

| Việc | Lệnh / nơi làm | Xong khi |
|---|---|---|
| Hai kiểm tra sẵn sàng chấm | `python3 coach/grade_d.py --template` và `--solution coach/reference` | 0/65 và 65/65 |
| Repo học viên không có `coach/` | `ls coach` trong bản phát hành | "No such file" |
| Danh sách lớp, chia nhóm 3 | LMS | mỗi nhóm có đủ slice A/B/C (nhóm 2 người: bỏ slice B) |
| Máy học viên chạy được | học viên tự chạy `python3 scripts/run_eval.py --judge v1` trước buổi | in `accuracy=0.750` |

## Diễn tiến

| Phút | Coach nói / làm | Học viên làm | Để ý | Nếu chậm |
|---|---|---|---|---|
| 0–10 | "Judge cho accuracy 0.75 — tốt hay tệ?" Chiếu ma trận nhầm lẫn trống | điền TEAM.md, chọn slice | nhóm chưa chia slice | coach chỉ định slice theo MSSV |
| 10–25 | đi một vòng, không giảng | CP1 | ai chưa ra 0.750 | xem README §Xử lý sự cố dòng 1 |
| 25–55 | gợi ý: "kappa bằng bao nhiêu khi judge luôn nói pass?" | CP2 | nhóm chia cho n − 1 (6/8 test) | chỉ vào `test_textbook_value` |
| 55–80 | | CP3 | `is_consistent` đảo ngược → `consistency=0.300` | hỏi "đổi chỗ mà verdict đổi theo thì judge nhất quán hay không?" |
| 80–120 | nhắc: mỗi người viết INDIVIDUAL trên slice của mình | CP4 | nhóm sửa v2 bằng một ý duy nhất (Δ ≈ 0.03) | nhắc ngưỡng R4 Δ ≥ 0.10 trong RUBRIC |
| 120–140 | | CP5 | REPORT thiếu mục "không chứng minh" | |
| 140–170 | DEBRIEF | | | rút DEBRIEF còn 2 khái niệm |
| 170–180 | | `check.py`, commit, SHA lên LMS | | |

## Tình huống biên

Đề không nói rõ → trả lời **một** cách cho cả lớp và ghi vào đây.

| Tình huống | Quy tắc |
|---|---|
| Nhóm 2 người | bỏ slice B (ít lỗi nhất); hai người lấy A và C |
| Nhóm 4 người | người thứ 4 lấy lại slice A, phải chọn ≥ 3 id khác người kia nếu có (A có 6 id) |
| v2 đạt kappa 1.0 bằng cách tra bảng id | hợp lệ cho R4 (tất định), nhưng R6 Strong đòi nêu đây là số trong mẫu; coach nêu trong debrief |
| Hỏi "được dùng LLM thật cho v2 không" | không: v2 phải tất định, không gọi mạng (README §Quy định) |

## Nên / không nên

- Không nói ngưỡng 50 % số liệu hay danh sách từ khoá của lời giải mẫu trước phút 120.
- Không chiếu kappa slice B của lời giải mẫu: slice B chỉ có 3 lỗi, dễ dẫn tới kết luận sai.

## Kiểm tra nhanh sau buổi

Mở 3 bài: một nhóm xong sớm, một nhóm chưa xong CP3, một nhóm 2 người. Nhìn: INDIVIDUAL có câu trích nguyên văn không; REPORT có số khớp `results/` không.

## Giờ đo thật (chỉ điền từ buổi thật, không ước lượng)

| Bước | Dự kiến | Thực tế (trung vị) | Ghi chú |
|---|---|---|---|
| CP1 | 15 | CHƯA ĐO | |
| CP2 | 30 | CHƯA ĐO | |
| CP3 | 25 | CHƯA ĐO | |
| CP4 | 40 | CHƯA ĐO | |
| CP5 | 20 | CHƯA ĐO | |

## Lỗi đã gặp → chuyển vào README §Xử lý sự cố

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| `ImportError: Failed to import test module` | chạy từ thư mục con | `cd` về gốc repo (đã tái hiện khi soạn) |
