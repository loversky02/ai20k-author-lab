# RUBRIC — Ví dụ – Hiệu chỉnh LLM-as-judge với nhãn người

Đây là tài liệu duy nhất quyết định điểm. README và CHECKPOINTS phải khớp với file này.

## 1. Công thức

`final = min(100, core + bonus)` · core tối đa **100** · bonus tối đa **5**.
Điểm sàn: **Không có điểm sàn.** Một bài chỉ nộp template không sửa được 0 điểm (đã kiểm tra bằng `coach/grade_d.py --template`).

## 2. Bảng tiêu chí

Loại: **D** = script quyết định · **J** = người / LLM chấm theo mốc bên dưới.

| ID | Tiêu chí | Điểm | Bằng chứng | Loại | Mục tiêu |
|---|---|---|---|---|---|
| R1 | Cài confusion matrix và Cohen's kappa | 25 | `python3 -m unittest tests.test_metrics -v` (bản tests cố định của người chấm) | D | O1 |
| R2 | Hai lần chạy judge tái lập được | 15 | `results/judge_run_v1.json`, `results/judge_run_v2.json` | D | O1, O4 |
| R3 | Swap test đúng và tái lập được | 15 | `results/swap_test.json`, `scripts/swap_test.py` | D | O2 |
| R4 | Judge v2 cải thiện kappa | 10 | kappa tính lại từ `verdicts` trong hai file run | D | O4 |
| R5 | Phân tích lỗi trên slice cá nhân | 20 | `submission/INDIVIDUAL/<MSSV>.md` | J | O3 |
| R6 | Báo cáo nhóm: trước/sau và giới hạn | 15 | `submission/REPORT.md` | J | O2, O4 |
| B1 | Đánh giá giữ lại (held-out) cho judge v2 | 5 | `submission/REPORT.md` mục Held-out | J | O4 |

R2–R4 dùng hàm metrics của người chấm, không dùng `src/metrics.py` của bạn: sai ở R1 không bị trừ lần nữa ở R4.

## 3. Tiêu chí D

Người chấm chạy `python3 coach/grade_d.py <repo>` trên bản sao của repo.

| ID | Lệnh / kiểm tra | Mức điểm |
|---|---|---|
| R1 | chạy 8 test cố định trên `src/metrics.py` của bạn | 8/8 = 25 · 6–7 = 15 · < 6 = 0 |
| R2 | mỗi file: `data_sha256` khớp, chạy lại `JUDGES[v]` trên `data/answers.jsonl` cho **đúng từng verdict**, accuracy khớp | 2 file hợp lệ = 15 · 1 file = 7 · 0 = 0 |
| R3 | `data_sha256` khớp; `original`/`swapped` khớp khi chạy lại; `consistent` và `consistency` khớp khi người chấm tính lại | đúng hết = 15 · tái lập được nhưng `consistency` sai = 5 · thiếu / không tái lập = 0 |
| R4 | chỉ khi R2 = 15: Δ = kappa(v2) − kappa(v1) | Δ ≥ 0.10 = 10 · 0 < Δ < 0.10 = 5 · Δ ≤ 0 = 0 |

Ngưỡng R4 lấy từ số đo: judge v1 có kappa 0.508; một sửa đổi đơn lẻ (bắt câu thô lỗ, hoặc chấp nhận ≥ 50 % số liệu) tăng 0.02–0.04; lời giải mẫu tăng 0.423. Δ ≥ 0.10 cần kết hợp ít nhất hai loại lỗi.

## 4. Tiêu chí J

### R5 — Phân tích lỗi trên slice cá nhân (20 điểm, cá nhân)

**Phải có:** dòng `Slice: A|B|C` đúng với TEAM.md; bảng ≥ 3 id mà **judge v1 sai** thuộc slice đó (lấy từ `disagreements` trong `results/judge_run_v1.json`); mỗi id có nhãn người, nhãn judge, một **loại lỗi** trong danh sách bên dưới, câu trích nguyên văn từ `answer` cho thấy lỗi, và v2 của nhóm đã sửa id đó chưa.

Loại lỗi: `thiếu-số` (đúng nhưng thiếu một số trong reference) · `số-bằng-chữ` · `không-có-số` (reference không có số) · `bịa-thêm` (đúng số, thêm chính sách không có) · `giọng-điệu` (đúng nội dung, thô lỗ) · `khác` (phải giải thích).

| Mức | Điểm | Ví dụ |
|---|---|---|
| Strong | 20 | ≥ 3 id đúng slice, loại lỗi và câu trích khớp dữ liệu; **thêm** một câu khái quát có số, vd "5/6 lỗi của v1 trên slice A là `thiếu-số` hoặc `không-có-số`: v1 đòi đủ mọi số nên phạt câu trả lời ngắn" |
| Adequate | 12 | ≥ 3 id đúng slice, loại lỗi và câu trích khớp dữ liệu, không có câu khái quát hoặc câu khái quát không có số |
| Chưa đạt | 0 | < 3 id hợp lệ, hoặc id không thuộc slice, hoặc không có file |

**Trừ điểm:** −4 mỗi id có câu trích không có trong `answer` hoặc loại lỗi mâu thuẫn với câu trích (tối đa −12). Câu trích bịa = điều kiện trượt §5. Hai thành viên nộp cùng bảng id → cả hai tối đa 6.

### R6 — Báo cáo nhóm: trước/sau và giới hạn (15 điểm)

**Phải có:** bảng kappa và accuracy của v1 và v2 (tổng và theo slice), ma trận nhầm lẫn của cả hai, kết quả swap test (`consistency`, `first_position_rate`, `human_agreement`), và mục "Con số này không chứng minh".

| Mức | Điểm | Ví dụ |
|---|---|---|
| Strong | 15 | mọi số khớp `results/`; giải thích vì sao `human_agreement` cao mà `consistency` thấp (cặp hoà bị xử về vị trí A); nêu ≥ 2 giới hạn có số, vd "v2 được chỉnh trên chính 60 câu này nên kappa 0.93 là số trong mẫu" và "slice B chỉ có 3 lỗi v1, quá ít để kết luận theo slice" |
| Adequate | 9 | mọi số khớp `results/`; nêu ≥ 1 giới hạn có số; chưa giải thích quan hệ giữa `human_agreement` và `consistency` |
| Chưa đạt | 0 | thiếu bảng số, hoặc có số không khớp `results/`, hoặc không có giới hạn nào |

**Trừ điểm:** −3 mỗi số trong REPORT không khớp `results/` (tối đa −9). Kết luận "judge v2 đáng tin để chấm thật" mà không có đánh giá ngoài 60 câu → trần 9.

### B1 — Đánh giá giữ lại (+5)

Chỉnh `judge_v2` chỉ dựa trên 2 slice, đo kappa trên slice còn lại **trước khi** sửa thêm, ghi rõ slice nào giữ lại và commit SHA lúc đo. +5 khi số đo tái lập được từ commit đó; +2 khi có số nhưng không chỉ ra được commit; 0 nếu không có.

## 5. Điều kiện trượt và trần điểm

Độc lập với điểm, áp dụng cho mọi bài:

| Vi phạm | Hậu quả |
|---|---|
| Bịa kết quả, log, số đo hoặc câu trích (file `results/` sửa tay, số trong REPORT không có trong bất kỳ lần chạy nào) | tổng = 0 |
| Commit khoá API | trần 50 điểm và phải xoá khoá khỏi lịch sử trong 24 giờ |
| Sửa `tests/test_metrics.py`, `data/*.jsonl`, `scripts/run_eval.py`, `judge_v1`, `pairwise_v1` | R1–R4 liên quan = 0 |
| Repo private / 404 lúc chấm, sai repo | 0 cho đến khi sửa trong hạn nộp muộn; tính như nộp muộn |
| `judge_v2` không tất định (kết quả đổi giữa hai lần chạy) | R2 tính 1 file, R4 = 0 |

## 6. Bằng chứng hợp lệ

- File `results/*.json` chỉ hợp lệ khi người chấm chạy lại script trên repo của bạn và được **đúng từng verdict**. Sửa code sau khi chạy mà không chạy lại = file không hợp lệ.
- Ảnh chụp màn hình không thay được file `results/`.
- Số trong REPORT và INDIVIDUAL phải đọc được từ `results/` ở commit được chấm.
- Người chấm đọc số từ output / file chạy lại được, không chấm theo từ khoá xuất hiện trong bài.

## 7. Xếp loại

| Điểm | Mức |
|---|---|
| 90–100 | Xuất sắc |
| 75–89 | Tốt |
| 60–74 | Đạt |
| 0–59 | Cần làm lại |

## 8. Bài nhóm

- **Điểm nhóm (80):** R1, R2, R3, R4, R6 và B1 — mọi thành viên nhận như nhau.
- **Điểm cá nhân (20):** R5, chấm riêng trên `INDIVIDUAL/<MSSV>.md` của từng người.
- Thành viên **không có** file INDIVIDUAL và không có dòng trong CONTRIBUTIONS: nhận 0 cho R5 và được hỏi vấn đáp; không giải thích được phần mình nhận làm trong TEAM.md thì điểm nhóm của người đó × 0.5.
- Đánh giá đồng đội (TEAM.md) trung bình ≤ 2/5 từ cả hai bạn còn lại → coach hỏi vấn đáp trước khi chốt điểm; điểm đồng đội không tự động trừ điểm.
- Commit chỉ là bằng chứng phụ: không bị trừ vì ít commit nếu CONTRIBUTIONS ghi rõ làm chung máy.

## 9. Nộp muộn, phúc khảo

- Chấm commit cuối cùng trước hạn. Muộn: −10 điểm/ngày, tối đa 2 ngày; sau đó 0.
- Phúc khảo: trong 3 ngày sau khi có điểm, qua form phúc khảo trên LMS, nêu ID tiêu chí và bằng chứng (path:line).

## 10. Checklist người chấm (2 phút)

- [ ] Repo đúng tên, public, SHA trên LMS khớp commit trước hạn
- [ ] Chạy `python3 coach/grade_d.py <repo>` → ghi R1–R4
- [ ] Mở `results/judge_run_v1.json` → lấy `disagreements` theo slice; mở từng `INDIVIDUAL/<MSSV>.md` → đối chiếu id, slice, câu trích
- [ ] Mở `submission/REPORT.md` → so từng số với `results/`
- [ ] Ghi tiêu chí J kèm trích dẫn bằng chứng (path:line)
