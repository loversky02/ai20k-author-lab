# DEBRIEF — Ví dụ – Hiệu chỉnh LLM-as-judge  (PRIVATE)

30 phút cuối buổi (phút 140–170). 3 khái niệm. Số bên dưới là **số của lời giải mẫu**; thay bằng số của lớp khi có.

## Accuracy che giấu hướng lỗi

- **Chỉ:** ma trận v1 — 12/15 lỗi là câu đúng bị fail; accuracy 0.75, kappa 0.51.
- **Hỏi:** "Judge này nghiêm quá hay dễ quá? Accuracy có cho bạn biết không?"
- **Chốt:** báo kappa và ma trận nhầm lẫn, không báo accuracy một mình.
- **Không chứng minh:** kappa 0.51 so với **một** người chấm; không biết hai người chấm đồng ý với nhau tới đâu.

## Đồng thuận cao vẫn có thể là thiên lệch vị trí

- **Chỉ:** swap test — human_agreement 0.90 nhưng consistency 0.70; 9 cặp hoà đều bị xử về A.
- **Hỏi:** "Nếu chỉ đo đồng thuận với người, nhóm nào phát hiện được lỗi này?"
- **Chốt:** luôn chạy judge so cặp hai chiều; cặp đổi kết quả khi đổi chỗ là cặp judge không phân biệt được.
- **Không chứng minh:** swap test đo `pairwise_v1`, không đo judge v2 của các nhóm.

## Cải tiến trên chính dữ liệu đánh giá

- **Chỉ:** v2 mẫu kappa 0.93 nhờ từ khoá khớp đúng câu trong dữ liệu ("tự động gia hạn"); bảng B1 của nhóm nào có held-out.
- **Hỏi:** "Đưa judge v2 này đi chấm bài lab tuần sau được không?"
- **Chốt:** số trong mẫu không phải bằng chứng tổng quát; giữ lại một phần dữ liệu trước khi sửa.
- **Không chứng minh:** held-out một slice 20 câu vẫn là mẫu nhỏ.

## Số liệu lớp

Ví dụ (lời giải mẫu), chưa có số lớp thật.

## Form ẩn danh (3 câu)

1. Bạn kẹt ở bước nào lâu nhất?
2. Mỗi bước mất khoảng bao nhiêu phút?
3. Nên bỏ hoặc rút gọn phần nào?
