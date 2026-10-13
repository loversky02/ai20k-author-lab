# RUBRIC — <FILL: DayNN – Tên lab>

Đây là tài liệu duy nhất quyết định điểm. README và CHECKPOINTS phải khớp với file này.

## 1. Công thức

`final = min(100, core + bonus)` · core tối đa **100** · bonus tối đa **<FILL>**.
Điểm sàn: **<FILL: Không có điểm sàn | bài nộp hợp lệ tối thiểu X>**.

## 2. Bảng tiêu chí

Loại: **D** = script quyết định · **J** = người / LLM chấm theo mốc bên dưới.

| ID | Tiêu chí | Điểm | Bằng chứng | Loại | Mục tiêu |
|---|---|---|---|---|---|
| R1 | <FILL> | <FILL> | `<FILL: path hoặc lệnh>` | D | O1 |
| R2 | | | | J | O2 |
| B1 | <FILL: bonus> | <FILL> | | | O? |

## 3. Tiêu chí D

| ID | Lệnh | Mức điểm |
|---|---|---|
| R1 | `<FILL>` | <FILL: vd 6/6 test = 20; 4–5 = 12; < 4 = 0> |

## 4. Tiêu chí J

### R2 — <FILL> (<FILL> điểm)

**Phải có:** <FILL: mô tả nội dung, vd "≥2 trường hợp cụ thể kèm id và số liệu từ lần chạy của bạn">.

| Mức | Điểm | Ví dụ |
|---|---|---|
| Strong | <FILL> | <FILL: một câu mẫu đạt mức này> |
| Adequate | <FILL> | <FILL> |
| Chưa đạt | 0 | <FILL> |

**Trừ điểm:** <FILL: −N mỗi …; trần X nếu …>.

## 5. Điều kiện trượt và trần điểm

Độc lập với điểm, áp dụng cho mọi bài:

| Vi phạm | Hậu quả |
|---|---|
| Bịa kết quả, log, phiên test, người test hoặc feedback | tổng = 0 |
| Commit khoá API | <FILL> |
| Sửa file cố định (tests, case set, scorer) | tiêu chí liên quan = 0 |
| Repo private / 404 lúc chấm, sai repo | <FILL> |

## 6. Bằng chứng hợp lệ

- <FILL: vd "Notebook phải được commit kèm output đã chạy. Ảnh chụp màn hình chỉ bổ trợ, không thay output.">
- <FILL: vd "Lần chạy hợp lệ khi provider_error_cases = 0 và measured_cases = total_cases.">
- Người chấm đọc số từ output / file chạy lại được, không chấm theo từ khoá xuất hiện trong bài.

## 7. Xếp loại

| Điểm | Mức |
|---|---|
| 90–100 | Xuất sắc |
| 75–89 | Tốt |
| 60–74 | Đạt |
| 0–59 | Cần làm lại |

## 8. Bài nhóm

<FILL: Cá nhân — bỏ mục này. Nhóm — điểm nhóm (tiêu chí nào) / điểm cá nhân (tiêu chí nào); thành viên không có bằng chứng thì nhận gì; quy tắc hỏi vấn đáp.>

## 9. Nộp muộn, phúc khảo

- Chấm commit cuối cùng trước hạn. Muộn: <FILL: −N điểm/ngày, tối đa M ngày>.
- Phúc khảo: <FILL: trong N ngày sau khi có điểm, qua kênh nào>.

## 10. Checklist người chấm (2 phút)

- [ ] Repo đúng tên, public, SHA trên LMS khớp commit trước hạn
- [ ] Chạy `<FILL: lệnh self-check / grader>`
- [ ] <FILL: các điểm cần mở và nhìn>
- [ ] Ghi tiêu chí J kèm trích dẫn bằng chứng (path:line)
