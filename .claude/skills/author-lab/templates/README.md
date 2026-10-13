# <FILL: DayNN – Tên lab>

**Hình thức:** <FILL: Cá nhân | Nhóm 3 (2–4)> · **Track:** <FILL> · **Ngôn ngữ:** tiếng Việt (lệnh, tên file, mã tiêu chí bằng tiếng Anh)

<FILL: 1–2 câu: sau lab này bạn làm được gì, gắn với slide nào của buổi sáng.>

## Thời lượng và điểm

- Trên lớp: **<FILL> phút** (gồm 10 phút nộp bài). Cài đặt làm **trước** buổi học, không tính giờ.
- Điểm: core **100** + bonus tối đa **<FILL>**. `final = min(100, core + bonus)`.
- Chi tiết chấm: [RUBRIC.md](RUBRIC.md) — đây là tài liệu duy nhất quyết định điểm.

## Mục tiêu học tập

| # | Làm được | Đo bằng | Mức đạt |
|---|---|---|---|
| O1 | <FILL: động từ quan sát được + đối tượng + điều kiện> | <FILL: file / lệnh> | <FILL: số hoặc điều kiện cụ thể> |
| O2 | | | |
| O3 | | | |

## Đọc theo thứ tự

| Thứ tự | File | Khi nào |
|---|---|---|
| 1 | README.md | bây giờ |
| 2 | CHECKPOINTS.md | trong khi làm, từng bước |
| 3 | RUBRIC.md | trước khi bắt đầu và trước khi nộp |
| 4 | SUBMISSION.md | 15 phút cuối |
| 5 | TEAM.md | bài nhóm: 5 phút đầu, chia vai |

## Chuẩn bị trước buổi học

```bash
<FILL: lệnh cài đặt, ghim phiên bản>
<FILL: lệnh preflight>
```

Kết quả đúng: `<FILL: dòng in ra khi môi trường sẵn sàng>`. Không ra dòng này → xem [Xử lý sự cố](#xử-lý-sự-cố) trước buổi học.

## Bắt đầu nhanh

```bash
<FILL: 1–3 lệnh chạy được ngay trên template, in ra kết quả mẫu>
```

## Các bước

| Bước | Phút | Sản phẩm | Tự kiểm tra | Đạt khi |
|---|---|---|---|---|
| CP1 | <FILL> | <FILL: file> | `<FILL: lệnh>` | <FILL: kết quả quan sát được> |
| CP2 | | | | |
| CP3 | | | | |
| Nộp bài | 10 | commit + SHA trên LMS | `<FILL: lệnh self-check>` | in `SẴN SÀNG NỘP` |

**Nếu bị chậm:** <FILL: đến phút X chưa xong CPy → bỏ phần nào, mất bao nhiêu điểm>.

## Sản phẩm cần nộp

| Đường dẫn | Định dạng / giới hạn | Tiêu chí |
|---|---|---|
| `<FILL: path>` | <FILL> | R1 |

Không commit: <FILL: dữ liệu thô, model weights, `.env`>.

## Cấu trúc repo

```
<FILL: cây thư mục; đánh dấu file bạn sửa và file cố định (không được sửa)>
```

## Quy định

- **AI:** <FILL: mức cho phép, vd "được dùng AI để hỏi và sinh code mẫu; bạn phải giải thích được mọi dòng đã nộp">. Khai báo trong `submission/REFLECTION.md`.
- Không bịa kết quả, log, phiên test, người test hay feedback. Vi phạm là **điều kiện trượt** (xem RUBRIC).
- Không sửa: <FILL: tests, bộ case cố định, scorer>. Sửa = tiêu chí liên quan 0 điểm.
- Không commit khoá API / `.env`. Dùng `.env.example`.
- Tên file chỉ dùng chữ, số, `-`, `_`, `.` (không dùng `: * ? " < > |` — repo sẽ hỏng khi clone trên Windows).

## Nộp bài

Xem [SUBMISSION.md](SUBMISSION.md). Tóm tắt: repo `<FILL: mẫu tên>`, <FILL: public>, hạn **<FILL: HH:MM dd/mm/yyyy (GMT+7)>**, chấm **commit cuối cùng trước hạn**, dán SHA 40 ký tự lên LMS. Nộp muộn: <FILL: −N điểm/ngày, tối đa M ngày>.

## Xử lý sự cố

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| <FILL: chỉ ghi lỗi đã gặp khi dry run> | | |

## Tài liệu

- <FILL: slide buổi sáng, tài liệu gốc>
