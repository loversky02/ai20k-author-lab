# Ví dụ – Hiệu chỉnh LLM-as-judge với nhãn người

> **Đây là lab mẫu của skill `author-lab`**, không phải lab đã phát hành. Mọi số trong lab là số đo thật trên bộ dữ liệu tự tạo trong `data/`; giờ trên lớp **chưa dry run** (xem `coach/RUNBOOK.md`).

**Hình thức:** Nhóm 3 (2–4) · **Track:** Đánh giá hệ thống AI · **Ngôn ngữ:** tiếng Việt (lệnh, tên file, mã tiêu chí bằng tiếng Anh)

Sau lab này, nhóm bạn đo được một judge tự động đồng thuận với người chấm tới đâu (accuracy, Cohen's kappa, ma trận nhầm lẫn), phát hiện được độ lệch vị trí của judge so cặp, và cải tiến judge mà vẫn nói rõ con số mới **không** chứng minh điều gì. Gắn với phần "LLM-as-judge: bias và calibration" của slide buổi sáng.

## Thời lượng và điểm

- Trên lớp: **180 phút** (gồm 10 phút nộp bài). Cài đặt làm **trước** buổi học, không tính giờ.
- Điểm: core **100** + bonus tối đa **5**. `final = min(100, core + bonus)`.
- 65 điểm do script quyết định (R1–R4), 35 điểm người chấm theo mốc (R5 cá nhân, R6 nhóm).
- Chi tiết chấm: [RUBRIC.md](RUBRIC.md) — đây là tài liệu duy nhất quyết định điểm.

## Mục tiêu học tập

| # | Làm được | Đo bằng | Mức đạt |
|---|---|---|---|
| O1 | Cài đặt confusion matrix và Cohen's kappa cho nhãn pass/fail, kể cả trường hợp biên | `python3 -m unittest tests.test_metrics -v` | 8/8 test pass |
| O2 | Đo độ lệch vị trí của judge so cặp bằng swap test | `results/swap_test.json` | file tái lập được; `consistency` đúng khi người chấm tính lại |
| O3 | Phân loại lỗi của judge trên phần dữ liệu của riêng mình, dẫn id và trích câu trả lời | `submission/INDIVIDUAL/<MSSV>.md` | ≥ 3 id judge v1 sai thuộc slice của bạn, mỗi id có loại lỗi và câu trích |
| O4 | Cải tiến judge và báo cáo trước/sau trên cùng dữ liệu, kèm giới hạn của phép đo | `results/judge_run_v2.json`, `submission/REPORT.md` | kappa v2 − kappa v1 ≥ 0.10; REPORT nêu ≥ 1 giới hạn có số |

## Đọc theo thứ tự

| Thứ tự | File | Khi nào |
|---|---|---|
| 1 | README.md | bây giờ |
| 2 | TEAM.md | 5 phút đầu: chia vai, chọn slice |
| 3 | RUBRIC.md | trước khi bắt đầu và trước khi nộp |
| 4 | CHECKPOINTS.md | trong khi làm, từng bước |
| 5 | SUBMISSION.md | 15 phút cuối |

## Chuẩn bị trước buổi học

Chỉ cần Python 3.10 trở lên, không cài thêm gói, không cần khoá API.

```bash
python3 --version
python3 scripts/run_eval.py --judge v1
```

Kết quả đúng: dòng bắt đầu bằng `judge=v1  n=60  accuracy=0.750  kappa=CHƯA CÀI (CP2)`. Không ra dòng này → xem [Xử lý sự cố](#xử-lý-sự-cố) trước buổi học.

## Bắt đầu nhanh

```bash
python3 scripts/run_eval.py --judge v1     # chạy judge mẫu trên 60 câu trả lời
python3 check.py                           # xem còn thiếu gì; template trống sẽ báo CHƯA SẴN SÀNG
```

## Các bước

| Bước | Phút | Sản phẩm | Tự kiểm tra | Đạt khi |
|---|---|---|---|---|
| Mở đầu | 10 | `TEAM.md` đã điền vai, slice | mở `TEAM.md` | không còn `_(điền)_` ở bảng vai |
| CP1 Dùng | 15 | `results/judge_run_v1.json` | `python3 scripts/run_eval.py --judge v1` | in `accuracy=0.750` |
| CP2 Sửa | 30 | `src/metrics.py` | `python3 -m unittest tests.test_metrics -v` | `OK`, 8 test |
| CP3 Sửa | 25 | `scripts/swap_test.py`, `results/swap_test.json` | `python3 scripts/swap_test.py` | in `consistency=` nhỏ hơn 1.000 |
| CP4 Tự làm | 40 | `src/judge.py` (`judge_v2`), `results/judge_run_v2.json`, `submission/INDIVIDUAL/<MSSV>.md` | `python3 check.py` | các dòng INDIVIDUAL và judge_run_v2 có ✓ |
| CP5 Tự làm | 20 | `submission/REPORT.md` | `python3 check.py` | dòng REPORT có ✓ |
| Nộp bài | 10 | commit + SHA trên LMS | `python3 check.py` | in `SẴN SÀNG NỘP` |

Tổng 150 / 180 phút, chừa 30 phút (17 %) cho chậm trễ.

**Nếu bị chậm:** đến phút 110 chưa xong CP3 → bỏ cải tiến judge ở CP4 (mất R4, tối đa 10 điểm), nhưng vẫn viết `INDIVIDUAL/<MSSV>.md` từ `results/judge_run_v1.json` và chạy lại `--judge v2` (v2 = v1 vẫn hợp lệ cho R2). Đến phút 150 chưa có REPORT → viết REPORT 5 dòng chỉ gồm số đo, bỏ phần giới hạn (mất mức Strong của R6).

## Sản phẩm cần nộp

| Đường dẫn | Định dạng / giới hạn | Tiêu chí |
|---|---|---|
| `src/metrics.py` | `confusion()`, `cohen_kappa()` đã cài | R1 |
| `results/judge_run_v1.json` | do `scripts/run_eval.py` sinh, không sửa tay | R2 |
| `results/judge_run_v2.json` | do `scripts/run_eval.py` sinh, không sửa tay | R2, R4 |
| `scripts/swap_test.py` | `is_consistent()` đã cài | R3 |
| `results/swap_test.json` | do `scripts/swap_test.py` sinh | R3 |
| `src/judge.py` | chỉ sửa `judge_v2` và hàm phụ mới | R4 |
| `submission/INDIVIDUAL/<MSSV>.md` | mỗi thành viên một file, ≤ 400 từ, theo `_TEMPLATE.md` | R5 |
| `submission/REPORT.md` | ≤ 500 từ, số khớp `results/` | R6, B1 |
| `TEAM.md`, `CONTRIBUTIONS.md` | đã điền | §8 RUBRIC |

Không commit: `.env`, khoá API, thư mục `__pycache__/`.

## Cấu trúc repo

```
data/answers.jsonl        # CỐ ĐỊNH — 60 câu trả lời + nhãn người, slice A/B/C
data/pairs.jsonl          # CỐ ĐỊNH — 30 cặp + lựa chọn của người
src/judge.py              # judge_v1, pairwise_v1 CỐ ĐỊNH; judge_v2 bạn sửa (CP4)
src/metrics.py            # accuracy() mẫu; confusion(), cohen_kappa() bạn cài (CP2)
scripts/run_eval.py       # CỐ ĐỊNH — chạy judge, ghi results/judge_run_<v>.json
scripts/swap_test.py      # is_consistent() bạn cài (CP3)
tests/test_metrics.py     # CỐ ĐỊNH — 8 test
check.py                  # tự kiểm tra trước khi nộp (không phải chấm điểm)
results/                  # sinh ra bằng script, phải commit
submission/REPORT.md      # nhóm viết (CP5)
submission/INDIVIDUAL/    # mỗi người một file (CP4)
TEAM.md, CONTRIBUTIONS.md # nhóm điền
```

## Quy định

- **AI:** được dùng AI để hỏi khái niệm, gợi ý code và rà lỗi. Bạn phải giải thích được mọi dòng đã nộp; vấn đáp không giải thích được thì tiêu chí đó 0 điểm. Khai báo công cụ và việc đã dùng trong mục `## Dùng AI` của `submission/INDIVIDUAL/<MSSV>.md`.
- Không bịa kết quả, log, số đo hay câu trích. File trong `results/` phải do script sinh ra và tái lập được. Vi phạm là **điều kiện trượt** (xem RUBRIC §5).
- Không sửa: `tests/test_metrics.py`, `data/*.jsonl`, `scripts/run_eval.py`, `judge_v1`, `pairwise_v1`. Sửa = tiêu chí liên quan 0 điểm. `check.py` báo ✗ nếu các file này đổi.
- `judge_v2` phải tất định: không random, không gọi mạng. Người chấm chạy lại và so từng verdict.
- Không commit khoá API / `.env`. Lab này không cần khoá; B1 cũng không cần.
- Tên file chỉ dùng chữ, số, `-`, `_`, `.` (không dùng `: * ? " < > |` — repo sẽ hỏng khi clone trên Windows).

## Nộp bài

Xem [SUBMISSION.md](SUBMISSION.md). Tóm tắt: repo `judge-calib-<MaNhom>`, public, hạn **23:59 20/10/2026 (GMT+7)**, chấm **commit cuối cùng trước hạn**, mỗi thành viên dán cùng SHA 40 ký tự lên LMS. Nộp muộn: −10 điểm/ngày, tối đa 2 ngày; sau đó 0.

## Xử lý sự cố

| Triệu chứng | Nguyên nhân | Cách sửa |
|---|---|---|
| `ImportError: Failed to import test module: test_metrics` | chạy lệnh từ thư mục con (vd `tests/`) | `cd` về gốc repo rồi chạy lại |
| `kappa=CHƯA CÀI (CP2)` sau khi đã cài | chưa chạy lại `run_eval.py` | chạy lại `python3 scripts/run_eval.py --judge v1` và `--judge v2` |
| `check.py`: verdict không khớp lần chạy lại | sửa `judge_v2` nhưng chưa sinh lại `results/` | chạy lại `--judge v2`, commit file mới |

Dòng 1 đã tái hiện khi soạn lab. Dòng 2–3 là thông báo `run_eval.py` / `check.py` tự in ra, chưa phải lỗi đã gặp với học viên. Bổ sung sau dry run.

## Tài liệu

- Zheng et al., *Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena*, NeurIPS 2023 — position bias, swap test: https://arxiv.org/abs/2306.05685
- Cohen's kappa: J. Cohen (1960), *Educational and Psychological Measurement* 20(1).
