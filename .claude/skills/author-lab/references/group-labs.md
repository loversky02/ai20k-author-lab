# Group labs

A group lab must answer, for every member: **what do I own, who depends on it, what do I hand in myself, and how is my score separated from the team's.** "Done when: group labs state each member's tasks" is the acceptance rule this file serves.

## Design rules

1. **Positive interdependence.** Roles own complementary artifacts, and each role's output is another role's input (Johnson & Johnson). A team where three people could each do the whole lab alone is three individual labs.
2. **Individual accountability.** Every member has at least one artifact only they produce, graded on its own.
3. **Roles name artifacts, not adjectives.** "Metrics owner — `src/metrics.py`, `tests/test_metrics.py`" not "phụ trách kỹ thuật".
4. **Handoffs are on the clock.** The schedule says when role A's output must exist for role B (e.g. metrics frozen at minute 70 so the bias tester can use them). Give a fixture so B is not blocked if A is late.
5. **Rotate or share the hardest thinking.** Every member writes their own error analysis on their own case slice, so nobody only formats slides.
6. **Size.** 3 is the default for a 3-hour lab; 4–6 needs sub-tasks per person or roles collapse into watching.

## Role table (TEAM.md)

| Vai trò | Thành viên (Họ tên – MSSV – GitHub) | Sở hữu (file/thư mục) | Giao cho ai, khi nào | Phần cá nhân |
|---|---|---|---|---|
| Metrics owner | | `src/metrics.py`, `tests/test_metrics.py` | Judge owner, phút 70 | `INDIVIDUAL/<MSSV>.md` |
| Judge & rubric owner | | `src/judge.py`, `judge_rubric.md` | Bias tester, phút 110 | `INDIVIDUAL/<MSSV>.md` |
| Bias tester | | `src/swap_test.py`, `results/swap.json` | Cả nhóm, phút 140 | `INDIVIDUAL/<MSSV>.md` |

Teams of 2: merge roles 2+3. Teams of 4: split judge and rubric. Say this in TEAM.md.

## The INDIVIDUAL block

One file per member, written by that member, committed from their own GitHub account:

- What I built (paths, commit SHAs).
- One decision I made and the alternative I rejected.
- My own analysis on **my** input slice (cases chosen by the last digit of my MSSV), with ids and numbers from my run.
- AI use: tool, for what, what I changed or rejected after checking.
- What I would fix next.

Raw evidence over summaries: the member's own log, notes or test output. In Day18–19 T1, "individual" notes were copied between members and test sessions with testers were AI-fabricated; per-member different inputs and raw evidence make this visible.

## Scoring split

State it in RUBRIC §Team, with numbers:

- Team rows (shared product): e.g. 60 points, same for every member.
- Individual rows (own role artifact + INDIVIDUAL block): e.g. 40 points, per member.
- A member with no verifiable work in their owned paths and no INDIVIDUAL block gets 0 on individual rows and the team score × the peer factor (or a fixed cap) — say which.
- **Oral check rule** if used: any member may be asked about any part; cannot explain own part → that row 0 (Hackathon 3A). State it before the lab starts.

## Peer rating

A short behaviour-anchored form at the end (CATME-style categories: contributing to the work, interacting with teammates, keeping the team on track, expecting quality, having relevant skills), 1–5 with an anchor sentence per level. Use it to flag problem teams and to adjust individual scores only within a stated range (e.g. factor 0.8–1.0). Peer ratings have halo effects; never let them alone zero a member.

## Git as cross-check, not proof

Commit share correlates with peer ratings, but commit counts are easy to game and pair-programming hides real work. Use commits together with owned-file history and PR reviews; ask "each member has ≥2 non-trivial commits in their owned paths" rather than counting lines. A member who worked on a teammate's laptop records it in CONTRIBUTIONS.md with the SHAs.

## Submission for teams

- One repo; the name carries the team id. Every member submits the same URL and SHA on the LMS (L3B Day04) — a mismatch in student id across forms has split teams before (Hackathon 3A).
- `CONTRIBUTIONS.md` lists per member: owned paths, SHAs, % effort agreed by the team, signature line (GitHub handle).
