# LAB_SPEC — <FILL: DayNN – Tên lab>

Tài liệu thiết kế cho coach (có thể giữ private). Viết theo thứ tự: thẻ lab → mục tiêu → căn chỉnh → rubric → các bước. Trạng thái: **<FILL: nháp | đã review | đã dry run | đã pilot>**.

## 0. Thẻ lab

| Mục | Giá trị |
|---|---|
| Ngày / track / slide nguồn | <FILL> |
| Đối tượng, trình độ | <FILL> |
| Thời lượng trên lớp / ngoài giờ | <FILL> phút / <FILL> |
| Hình thức | <FILL: cá nhân / nhóm N> |
| Môi trường | <FILL: local / Colab / cloud; zero-key hay cần key> |
| Cách chấm | <FILL: script / LLM judge / người / kết hợp> |
| Mức dùng AI | <FILL> |
| Hạn nộp | <FILL: HH:MM dd/mm/yyyy (GMT+7)> |
| Câu hỏi mở (ai quyết, khi nào) | <FILL> |
| Phiên bản lab | <FILL: v1 (dd/mm/yyyy)>; lab cũ: link bản trước + danh sách thay đổi |

### 0b. Phiên bản & nguồn

Mỗi công cụ / thư viện / model lab dùng. Chỉ ghi "đã chạy" khi đã cài và chạy từ môi trường sạch (`references/research-and-refresh.md`).

| Công cụ | Phiên bản pin | Ngày kiểm tra | Nguồn chính thức (URL) | Smoke test | Phương án dự phòng |
|---|---|---|---|---|---|
| <FILL> | <FILL: ==x.y.z> | <FILL> | <FILL> | <FILL: đã chạy dd/mm / theo docs> | <FILL> |

## 1. Mục tiêu

| # | Làm được | Đo bằng | Mức đạt |
|---|---|---|---|
| O1 | | | |

## 2. Bảng căn chỉnh

| Mục tiêu | Bước luyện | Tiêu chí chấm | Bằng chứng |
|---|---|---|---|
| O1 | CP? | R? | |

Mục tiêu không có tiêu chí: <FILL: không có>. Tiêu chí không có mục tiêu: <FILL: không có>.

## 3. Rubric (nháp → RUBRIC.md)

## 4. Các bước (nháp → README + CHECKPOINTS)

| Bước | Phút | Pha (dùng/sửa/tự làm) | Sản phẩm | Tự kiểm tra | Bị kẹt? |
|---|---|---|---|---|---|

Tổng phút: <FILL> / <FILL> (buffer <FILL> %).

## 5. Quyết định thiết kế

| Quyết định | Phương án bị loại | Lý do |
|---|---|---|

## 6. Kiểm tra sẵn sàng chấm

| Kiểm tra | Kết quả | Ngày |
|---|---|---|
| Template trống qua grader ≈ 0 | <FILL: CHƯA CHẠY> | |
| Lời giải mẫu từ template = điểm tối đa | <FILL: CHƯA CHẠY> | |
| `lint_lab.py` 0 ERROR | | |
| 2 người chấm 3–5 bài mẫu, lệch ≤ ngưỡng | | |
| Dry run đo giờ thật | <FILL: CHƯA ĐO> | |
