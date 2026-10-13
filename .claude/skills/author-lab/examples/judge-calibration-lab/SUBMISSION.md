# Nộp bài — Ví dụ – Hiệu chỉnh LLM-as-judge với nhãn người

## Hợp đồng nộp bài

| Mục | Quy định |
|---|---|
| Repo | `judge-calib-<MaNhom>` (vd `judge-calib-N07`) · public · tạo repo mới từ template (Use this template), không fork |
| Hạn | **23:59 20/10/2026 (GMT+7)** |
| Commit được chấm | commit cuối cùng trước hạn; dán SHA 40 ký tự lên LMS |
| Nộp muộn | −10 điểm/ngày, tối đa 2 ngày; sau đó 0 |
| Sau hạn | không force-push; sửa bằng commit mới và ghi vào cuối file này; không được chấm nếu coach không đồng ý |
| Kênh | LMS, bài "Judge calibration" · bài nhóm: **mỗi thành viên** nộp cùng URL và SHA |
| Vấn đáp | có, 5 phút/nhóm ở buổi kế tiếp, coach chọn người trả lời; không giải thích được phần mình làm thì tiêu chí đó 0 |

## File phải có

| Đường dẫn | Định dạng / giới hạn |
|---|---|
| `src/metrics.py` | `confusion()`, `cohen_kappa()` đã cài |
| `scripts/swap_test.py` | `is_consistent()` đã cài |
| `src/judge.py` | `judge_v2` của nhóm, tất định |
| `results/judge_run_v1.json` | do `scripts/run_eval.py --judge v1` sinh |
| `results/judge_run_v2.json` | do `scripts/run_eval.py --judge v2` sinh |
| `results/swap_test.json` | do `scripts/swap_test.py` sinh |
| `submission/INDIVIDUAL/<MSSV>.md` | mỗi thành viên một file, ≤ 400 từ |
| `submission/REPORT.md` | ≤ 500 từ |
| `TEAM.md`, `CONTRIBUTIONS.md` | không còn `_(điền)_` |

## Tự kiểm tra trước khi nộp

- [ ] `python3 check.py` in `SẴN SÀNG NỘP`
- [ ] Mở repo trong cửa sổ ẩn danh: thấy đủ file, không cần đăng nhập
- [ ] SHA trên GitHub = SHA đã dán lên LMS (mỗi thành viên)
- [ ] Không có `.env`, khoá API trong repo
- [ ] Mỗi `INDIVIDUAL/<MSSV>.md` có mục `## Dùng AI`
- [ ] Tên file không chứa `: * ? " < > |`

## Ghi chép sau hạn (nếu có)

| Ngày | Commit | Lý do |
|---|---|---|
