"""Lint an ai20k lab's learner-facing docs before release. Stdlib only.

    python3 lint_lab.py <lab-dir> [--quiet]

Reads README.md, RUBRIC.md, SUBMISSION.md, CHECKPOINTS.md, TEAM.md, CONTRIBUTIONS.md and .gitignore
in <lab-dir>, plus every file name under it. Prints one line per finding:

    ERROR <check>: <message>     must be fixed before the lab ships
    WARN  <check>: <message>     read it; fix unless you have a reason

and exits 1 if any ERROR was found. It checks the things that made K4 graders disagree or
learners ask "what do I submit?": README sections, rubric total vs bands, objective <-> rubric
coverage, step minutes vs duration, an absolute deadline, a numeric late rule, the floor policy,
Windows-safe file names, deliverables hidden by .gitignore, unfilled placeholders, vague words in
grading text, unpinned lines in requirements.txt and the team files of a group lab.

Conventions it relies on (the author-lab templates follow them):
  objectives are table rows `| O1 | ...` under the README "Mục tiêu" heading;
  rubric rows are `| R1 | ...` (core) and `| B1 | ...` (bonus) with a points column headed
  "Điểm"/"Points" and an objective column headed "Mục tiêu"/"Objective";
  the README steps table has a "Phút"/"Minutes" column; duration is "<N> phút" or "<N> min".
It cannot judge whether a criterion is fair or a step is teachable — that stays with the coach.
"""
import fnmatch
import re
import sys
import unicodedata
from pathlib import Path

findings = []


def report(level, check, msg):
    findings.append((level, check, msg))


def fold(s):
    """Lower-case and strip Vietnamese accents so 'Mục tiêu' matches 'muc tieu'."""
    s = s.replace("đ", "d").replace("Đ", "D")
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn").lower()


def read(lab, name):
    p = lab / name
    return p.read_text(encoding="utf-8") if p.is_file() else None


def sections(md):
    """Map folded heading text -> body text, for ## and ### headings."""
    out, cur, buf = {}, "_top", []
    for line in md.splitlines():
        m = re.match(r"^#{2,3}\s+(.*)", line)
        if m:
            out[cur] = "\n".join(buf)
            cur, buf = fold(m.group(1)), []
        else:
            buf.append(line)
    out[cur] = "\n".join(buf)
    return out


def find_section(secs, *keys):
    for head, body in secs.items():
        if any(k in head for k in keys):
            return body
    return None


def table_rows(text):
    """Yield (header_cells, row_cells) for every markdown table row in text."""
    header = None
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("|"):
            header = None
            continue
        cells = [c.strip() for c in s.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        if header is None:
            header = cells
            continue
        yield header, cells


def col(header, *keys):
    for i, h in enumerate(header):
        if any(k in fold(h) for k in keys):
            return i
    return None


def num(cell):
    m = re.search(r"-?\d+(?:[.,]\d+)?", cell or "")
    return float(m.group(0).replace(",", ".")) if m else None


README_SECTIONS = [  # (label, folded keys, level)
    ("Thời lượng và điểm", ("thoi luong", "duration"), "ERROR"),
    ("Mục tiêu học tập", ("muc tieu", "objective"), "ERROR"),
    ("Đọc theo thứ tự", ("doc theo thu tu", "read in order", "read-in-order"), "WARN"),
    ("Chuẩn bị trước buổi học", ("chuan bi", "preflight", "setup", "prerequisite"), "ERROR"),
    ("Bắt đầu nhanh", ("bat dau nhanh", "quick start", "quickstart"), "WARN"),
    ("Các bước", ("cac buoc", "steps", "lich trinh", "schedule"), "ERROR"),
    ("Sản phẩm cần nộp", ("san pham", "deliverable"), "ERROR"),
    ("Cấu trúc repo", ("cau truc", "repo tree", "structure"), "WARN"),
    ("Quy định", ("quy dinh", "rules"), "ERROR"),
    ("Nộp bài", ("nop bai", "submission"), "ERROR"),
    ("Xử lý sự cố", ("xu ly su co", "troubleshoot", "loi thuong gap"), "WARN"),
]
VAGUE = ["tốt", "đầy đủ", "hợp lý", "rõ ràng", "phù hợp", "chất lượng", "good", "clear",
         "reasonable", "appropriate", "sufficient", "nice", "properly"]
VAGUE_RE = re.compile(r"(?<![\wÀ-ỹ])(" + "|".join(re.escape(w) for w in VAGUE) + r")(?![\wÀ-ỹ])", re.I)
BAD_NAME = re.compile(r'[:*?"<>|]')
DATE_RE = re.compile(r"\b\d{1,2}/\d{1,2}/\d{4}\b|\b\d{4}-\d{2}-\d{2}\b")
TIME_RE = re.compile(r"\b\d{1,2}[:h]\d{2}\b")
TZ_RE = re.compile(r"GMT\s*\+\s*7|UTC\s*\+\s*7|\bICT\b|Asia/Ho_Chi_Minh", re.I)
DEFERRED_RE = re.compile(r"theo (thông báo|coach|key coach|giảng viên)|per coach|announced later", re.I)
PLACEHOLDER_RE = re.compile(r"<FILL\b[^>]*>")
SOFT_PLACEHOLDER_RE = re.compile(r"\b(TODO|TBD|FIXME|XXX)\b")


def check_readme(readme):
    secs = sections(readme)
    for label, keys, level in README_SECTIONS:
        if find_section(secs, *keys) is None:
            report(level, "readme-section", f'README has no "{label}" section')
    top = secs.get("_top", "") + "\n" + readme[:600]
    mode = re.search(r"(hình thức|mode)\W+([^\n·]+)", top, re.I)
    if not mode:
        report("ERROR", "readme-mode", 'README does not state the mode ("**Hình thức:** Cá nhân | Nhóm N")')
    is_team = bool(mode and re.search(r"nhóm|team|group", mode.group(2), re.I))
    return secs, is_team


def readme_objectives(secs):
    body = find_section(secs, "muc tieu", "objective") or ""
    return sorted({m.group(1) for m in re.finditer(r"^\|\s*(O\d+)\s*\|", body, re.M)}, key=lambda s: int(s[1:]))


def readme_duration(secs):
    body = find_section(secs, "thoi luong", "duration") or ""
    m = re.search(r"(\d+)\s*(phút|phut|min)", body, re.I)
    if m:
        return int(m.group(1))
    m = re.search(r"(\d+(?:[.,]\d+)?)\s*(giờ|gio|h\b|hours?)", body, re.I)
    return int(float(m.group(1).replace(",", ".")) * 60) if m else None


def check_steps(secs):
    body = find_section(secs, "cac buoc", "steps", "lich trinh", "schedule")
    if body is None:
        return
    total, seen = 0, False
    for header, cells in table_rows(body):
        i = col(header, "phut", "minute", "min")
        if i is None or i >= len(cells):
            continue
        v = num(cells[i])
        if v is not None:
            total, seen = total + v, True
    duration = readme_duration(secs)
    if not seen:
        report("ERROR", "steps-minutes", 'README steps table has no "Phút"/"Minutes" column with numbers')
        return
    if duration is None:
        report("ERROR", "duration", 'README "Thời lượng" section states no duration in minutes')
        return
    if total > duration:
        report("ERROR", "steps-minutes", f"step minutes sum to {total:g} but the session is {duration} min")
    elif total > 0.9 * duration:
        report("WARN", "steps-minutes", f"step minutes {total:g}/{duration} leave under 10% buffer (aim for 15-25%)")
    if not re.search(r"(nếu bị chậm|neu bi cham|if behind|when behind)", body, re.I):
        report("WARN", "steps-behind", 'README steps section has no "Nếu bị chậm" rule (which step to drop)')


def check_rubric(rubric, objectives):
    if rubric is None:
        report("ERROR", "rubric", "RUBRIC.md is missing")
        return
    core, bonus, cited, rows, seen = 0.0, 0.0, set(), 0, set()
    for header, cells in table_rows(rubric):
        rid = cells[0] if cells else ""
        if not re.fullmatch(r"[RB]\d+", rid):
            continue
        pi = next((i for i, h in enumerate(header) if fold(h) in ("diem", "points", "point", "pts")), None)
        oi = col(header, "muc tieu", "objective")
        if pi is None or oi is None or rid in seen:
            continue
        seen.add(rid)
        rows += 1
        pts = num(cells[pi]) if pi < len(cells) else None
        if pts is None:
            report("ERROR", "rubric-points", f"rubric row {rid} has no points")
            continue
        if rid.startswith("R"):
            core += pts
        else:
            bonus += pts
        objs = set(re.findall(r"O\d+", cells[oi])) if oi is not None and oi < len(cells) else set()
        if rid.startswith("R") and not objs:
            report("ERROR", "alignment", f"rubric row {rid} cites no objective (orphan criterion)")
        cited |= objs
    if rows == 0:
        report("ERROR", "rubric-table", 'RUBRIC has no criteria table with "| R1 |" rows, a "Điểm" column and a "Mục tiêu" column')
        return
    stated = re.search(r"core\s+(?:toi da|tong|max(?:imum)?|total)\s*[:=]?\s*\**\s*(\d+)", fold(rubric))
    expected = float(stated.group(1)) if stated else 100.0
    if abs(core - expected) > 0.01:
        report("ERROR", "rubric-total", f"core rows sum to {core:g}, rubric states {expected:g}")
    if "min(100" not in rubric.replace(" ", ""):
        report("WARN", "rubric-formula", "RUBRIC has no `final = min(100, core + bonus)` line")
    for o in objectives:
        if o not in cited:
            report("ERROR", "alignment", f"objective {o} is not assessed by any rubric row")
    for o in sorted(cited - set(objectives)):
        report("ERROR", "alignment", f"rubric cites {o}, which README does not define")
    folded = fold(rubric)
    if not re.search(r"diem san|floor", folded):
        report("ERROR", "floor-policy", 'RUBRIC does not state a floor policy (write "Không có điểm sàn" if none)')
    if not re.search(r"bang chung hop le|evidence validity|valid evidence", folded):
        report("WARN", "evidence-validity", "RUBRIC has no evidence-validity section (outputs vs screenshots, run validity)")
    if not re.search(r"dieu kien truot|fail condition", folded):
        report("WARN", "fail-conditions", "RUBRIC lists no fail conditions apart from the score")
    if not re.search(r"checklist", folded):
        report("WARN", "grader-checklist", "RUBRIC has no grader checklist")
    uppers = [int(b) for a, b in re.findall(r"\b(\d{1,3})\s*[–-]\s*(\d{1,3})\b", find_section(sections(rubric), "xep loai", "band", "muc diem") or "")]
    if uppers and max(uppers) != 100:
        report("ERROR", "rubric-bands", f"grade bands top out at {max(uppers)}, final score tops out at 100")
    in_code = False
    for n, line in enumerate(rubric.splitlines(), 1):
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if in_code or line.lstrip().startswith("#"):
            continue
        text = re.sub(r"`[^`]*`", "", line)
        m = VAGUE_RE.search(text)
        if m and not re.search(r"\d", text):
            report("WARN", "vague-word", f'RUBRIC line {n}: "{m.group(1)}" with no number or concrete descriptor')


def check_deadline(texts):
    joined = "\n".join(t for t in texts if t)
    if not (DATE_RE.search(joined) and TIME_RE.search(joined) and TZ_RE.search(joined)):
        report("ERROR", "deadline", "no absolute deadline (date + time + GMT+7) in README/SUBMISSION")
    if not re.search(r"(muộn|late)[^\n]*\d", joined, re.I):
        report("ERROR", "late-rule", "no numeric late rule (e.g. '−10 điểm/ngày')")
    for m in DEFERRED_RE.finditer(joined):
        report("WARN", "deferred-policy", f'policy deferred to an announcement: "{m.group(0)}"')
    if not re.search(r"\bSHA\b|commit cuối|last commit", joined, re.I):
        report("WARN", "graded-commit", "the graded commit is not defined (last commit before the deadline + SHA)")


def check_names(lab):
    for p in lab.rglob("*"):
        if ".git" in p.parts:
            continue
        if BAD_NAME.search(p.name) or p.name.endswith((".", " ")):
            report("ERROR", "windows-name", f"{p.relative_to(lab)} is not a valid Windows file name")
    for name in ("README.md", "SUBMISSION.md", "CHECKPOINTS.md"):
        t = read(lab, name) or ""
        for m in re.finditer(r"`([^`\s]+\.[A-Za-z0-9]{1,5})`", t):
            if "*" in m.group(1):  # a glob such as data/*.jsonl names many files, not one
                continue
            if BAD_NAME.sub("", m.group(1).replace("<", "").replace(">", "")) != m.group(1).replace("<", "").replace(">", ""):
                report("ERROR", "windows-name", f'{name} asks for "{m.group(1)}", not a valid Windows file name')


NOT_SUBMITTED_RE = re.compile(r"không (được )?(commit|nộp|sửa)|không có|do not (commit|submit|edit)|don't (commit|submit)|never commit", re.I)


def deliverable_paths(secs, submission):
    text = (find_section(secs, "san pham", "deliverable") or "") + "\n" + (submission or "")
    paths = set()
    # lines that forbid a path ("Không commit: `.env`") name what must NOT be submitted
    text = "\n".join(l for l in text.splitlines() if not NOT_SUBMITTED_RE.search(l))
    for m in re.finditer(r"`([^`\s]+)`", text):
        s = m.group(1)
        if "/" in s or re.search(r"\.[A-Za-z0-9]{1,5}$", s):
            if not s.startswith(("python", "make", "git", "http", "-")) and "<" not in s:
                paths.add(s.rstrip("/"))
    return paths


def check_gitignore(lab, paths):
    gi = read(lab, ".gitignore")
    if not gi:
        return
    pats = [p.strip() for p in gi.splitlines() if p.strip() and not p.startswith("#") and not p.startswith("!")]
    for path in sorted(paths):
        parts = path.split("/")
        for pat in pats:
            pp = pat.strip("/")
            hit = fnmatch.fnmatch(path, pp) or any(fnmatch.fnmatch(seg, pp) for seg in parts) \
                or any(fnmatch.fnmatch("/".join(parts[: i + 1]), pp) for i in range(len(parts)))
            if hit:
                report("ERROR", "gitignored-deliverable", f'required path "{path}" is matched by .gitignore pattern "{pat}"')
                break


def check_placeholders(lab):
    for name in ("README.md", "RUBRIC.md", "SUBMISSION.md", "CHECKPOINTS.md", "TEAM.md"):
        t = read(lab, name)
        if not t:
            continue
        hard = PLACEHOLDER_RE.findall(t)
        if hard:
            report("ERROR", "placeholder", f"{name} still has {len(hard)} <FILL> placeholder(s)")
        for n, line in enumerate(t.splitlines(), 1):
            if SOFT_PLACEHOLDER_RE.search(re.sub(r"`[^`]*`", "", line)):
                report("WARN", "placeholder", f"{name} line {n}: {line.strip()[:80]}")


PIN_RE = re.compile(r"^[A-Za-z0-9_.\-\[\],]+\s*(==|===|@)")


def check_pins(lab):
    for name in ("requirements.txt", "requirements-dev.txt"):
        t = read(lab, name)
        if not t:
            continue
        for n, line in enumerate(t.splitlines(), 1):
            line = line.split("#")[0].strip()
            if not line or line.startswith("-") or "://" in line:
                continue
            if not PIN_RE.match(line):
                report("WARN", "pins", f"{name} line {n}: '{line}' is not pinned with == (a new release can break the lab mid-cohort)")


def check_team(lab, rubric):
    team = read(lab, "TEAM.md")
    if team is None:
        report("ERROR", "team", "group lab but TEAM.md is missing")
    else:
        roles = sum(1 for h, c in table_rows(team) if col(h, "vai tro", "role") == 0 and c and c[0] and not c[0].startswith("<"))
        if roles < 2:
            report("ERROR", "team", "TEAM.md role table names fewer than 2 roles")
        if not re.search(r"so huu|owns|owned", fold(team)):
            report("ERROR", "team", 'TEAM.md role table has no "Sở hữu" (owned artifact) column')
        if not re.search(r"individual|ca nhan", fold(team)):
            report("ERROR", "team", "TEAM.md does not define each member's individual part")
    if read(lab, "CONTRIBUTIONS.md") is None:
        report("ERROR", "team", "group lab but CONTRIBUTIONS.md is missing")
    if rubric and not re.search(r"^#{2,3}.*(nhom|team)", fold(rubric), re.M):
        report("ERROR", "team", "RUBRIC has no team section splitting shared vs individual points")


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 1:
        print(__doc__.split("\n\n")[0])
        print("usage: python3 lint_lab.py <lab-dir> [--quiet]")
        return 2
    lab = Path(args[0]).resolve()
    readme = read(lab, "README.md")
    rubric = read(lab, "RUBRIC.md")
    submission = read(lab, "SUBMISSION.md")
    if readme is None:
        report("ERROR", "readme", "README.md is missing")
        objectives, is_team, secs = [], False, {}
    else:
        secs, is_team = check_readme(readme)
        objectives = readme_objectives(secs)
        if not objectives:
            report("ERROR", "objectives", 'README objectives table has no "| O1 |" rows')
        elif len(objectives) > 5:
            report("WARN", "objectives", f"{len(objectives)} objectives; 3-5 is the default for a 2-4 h lab")
        check_steps(secs)
    check_rubric(rubric, objectives)
    if submission is None:
        report("WARN", "submission", "SUBMISSION.md is missing; the README must then carry the whole contract")
    check_deadline([readme, submission])
    check_names(lab)
    check_gitignore(lab, deliverable_paths(secs, submission))
    check_placeholders(lab)
    check_pins(lab)
    if is_team:
        check_team(lab, rubric)
    quiet = "--quiet" in argv
    for level, check, msg in findings:
        if not (quiet and level == "WARN"):
            print(f"{level:<5} {check}: {msg}")
    e = sum(1 for f in findings if f[0] == "ERROR")
    w = len(findings) - e
    print(f"{e} ERROR, {w} WARN — {lab.name} ({'team' if is_team else 'individual'} lab)")
    return 1 if e else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
