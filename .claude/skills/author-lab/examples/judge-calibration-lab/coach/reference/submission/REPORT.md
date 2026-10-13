# REPORT — N00 (bài mẫu của coach)

Số lấy từ lần chạy lời giải mẫu: `python3 check.py --solution coach/reference`.

## Judge v1 và v2

| | accuracy | kappa | kappa slice A | kappa slice B | kappa slice C |
|---|---|---|---|---|---|
| v1 | 0.75 | 0.51 | 0.42 | 0.69 | 0.42 |
| v2 | 0.97 | 0.93 | 0.80 | 1.00 | 1.00 |

Ma trận nhầm lẫn (hàng = người, cột = judge):

| | v1 pass | v1 fail | v2 pass | v2 fail |
|---|---|---|---|---|
| người pass (37) | 25 | 12 | 35 | 2 |
| người fail (23) | 3 | 20 | 0 | 23 |

v1 sai chủ yếu theo một hướng: 12/15 lỗi là câu đúng bị fail.

## judge_v2 thay đổi gì

| Thay đổi | Loại lỗi | id sửa được |
|---|---|---|
| Pass khi có ≥ 50 % số trong reference (thay vì 100 %) | `thiếu-số` | a04, a10 |
| Đọc "một tuần" = 7, "nửa năm" = 6 | `số-bằng-chữ` | a21, a48 |
| Reference không có số → pass khi ≥ 30 % từ của reference có trong answer | `không-có-số` | a34, a35, a40, a41, a43, a53 |
| Fail khi answer hứa thêm điều reference không có ("tặng", "tự động gia hạn", "giảm thêm") | `bịa-thêm` | a38, a59 |
| Fail khi có cụm thô lỗ | `giọng-điệu` | a01 |

Chưa sửa: a19, a44 (câu đúng, rất ngắn, không còn số và ít từ chung với reference).

## Swap test

| consistency | first_position_rate | human_agreement | inconsistent_ids |
|---|---|---|---|
| 0.70 | 0.60 | 0.90 | p03, p07, p13, p23, p24, p27, p28, p29, p30 |

9/30 cặp đổi kết quả khi đổi chỗ: ở cả 9 cặp, judge v1 cho hai câu cùng một verdict và `pairwise_v1` xử hoà về vị trí A. Vì nửa số cặp đặt câu tốt ở vị trí A, xử hoà về A trúng ý người ở 6/9 cặp đó, nên `human_agreement` 0.90 trông tốt dù judge không phân biệt được hai câu. Đo đồng thuận với người mà không đổi chỗ sẽ không thấy lỗi này.

## Con số này không chứng minh

- v2 được chỉnh trên chính 60 câu này, nên kappa 0.93 là số **trong mẫu**. Các từ khoá như "tự động gia hạn" khớp đúng câu trong dữ liệu; trên câu hỏi mới, v2 có thể không hơn v1.
- Slice B chỉ có 3 lỗi v1 và 20 câu; kappa 1.00 trên slice B không đủ để nói v2 hoàn hảo trên loại câu đó.
- Nhãn người là của một người chấm; lab không đo hai người chấm đồng ý với nhau tới đâu, nên không biết kappa trần thực tế là bao nhiêu.
- Swap test chạy trên `pairwise_v1`, không phải trên v2.

## Held-out (B1, không bắt buộc)

Không làm trong bài mẫu.
