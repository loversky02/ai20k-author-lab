# TEAM — _(điền)_

**Nhóm:** _(điền)_ · **Repo:** `judge-calib-<MaNhom>` · **Người đại diện nộp:** mỗi thành viên đều nộp cùng URL + SHA.

## Vai trò

Mỗi vai sở hữu một sản phẩm mà vai khác cần dùng. Nhóm 2 người: người giữ vai **Metrics** kiêm **Report**. Nhóm 4: tách **Report** khỏi **Judge**, người thứ tư giữ Report và làm B1.

| Vai trò | Họ tên – MSSV – GitHub | Sở hữu (file/thư mục) | Giao cho ai, phút thứ mấy | Phần cá nhân |
|---|---|---|---|---|
| Metrics | _(điền)_ | `src/metrics.py` | Judge + Report, phút 55 (kappa để so v1/v2) | `INDIVIDUAL/<MSSV>.md` |
| Bias | _(điền)_ | `scripts/swap_test.py`, `results/swap_test.json` | Report, phút 80 (số swap test) | `INDIVIDUAL/<MSSV>.md` |
| Judge + Report | _(điền)_ | `src/judge.py` (`judge_v2`), `submission/REPORT.md` | cả nhóm, phút 120 (v2 để mỗi người ghi "v2 đã sửa?") | `INDIVIDUAL/<MSSV>.md` |

## Đầu vào riêng của mỗi người

Mỗi người phân tích slice theo chữ số cuối MSSV: 0–3 → slice A, 4–6 → slice B, 7–9 → slice C. Hai người cùng slice: người có MSSV lớn hơn lấy slice kế tiếp (A → B → C → A). Ghi slice vào bảng dưới và vào dòng `Slice:` trong file INDIVIDUAL.

| Họ tên – MSSV | Slice |
|---|---|
| _(điền)_ | _(điền)_ |

## Mốc bàn giao

| Phút | Ai giao | Giao gì | Nếu trễ |
|---|---|---|---|
| 55 | Metrics | `src/metrics.py` pass 8 test | Judge + Report so v1/v2 bằng accuracy trước; kappa điền sau |
| 80 | Bias | `results/swap_test.json` | Report để trống mục swap test, Bias tự điền trước phút 160 |
| 120 | Judge + Report | `results/judge_run_v2.json` | mỗi người ghi "v2 đã sửa?" = "chưa đo" và nộp INDIVIDUAL đúng hạn |

## Điểm nhóm và điểm cá nhân

Xem RUBRIC §8. Tóm tắt: 80 điểm nhóm (R1–R4, R6, B1), 20 điểm cá nhân (R5 trên file INDIVIDUAL của từng người).

## Đánh giá đồng đội (cuối buổi, 5 phút)

Mỗi người chấm từng bạn 1–5 cho: đóng góp vào công việc · tương tác với nhóm · giữ nhóm đúng tiến độ · đòi hỏi chất lượng · kỹ năng liên quan. Mốc: 1 = hầu như không làm phần của mình; 3 = làm đủ phần được giao, đúng hạn; 5 = làm đủ, giúp người khác gỡ vướng, kiểm tra lại sản phẩm chung. Form: đường link coach gửi trên LMS lúc phút 170.
