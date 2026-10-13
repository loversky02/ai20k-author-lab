# Sources

Why the rules in this skill exist. Paraphrased; follow the link for the original. Items marked *(heuristic)* are working defaults, not findings — say so if you quote them to a coach.

## Course design

- **Backward design** — plan desired results, then acceptable evidence, then activities. Wiggins & McTighe, *Understanding by Design* (ASCD, 2nd ed. 2005). Summaries: https://fctl.ucf.edu/teaching-resources/course-design/backward-design/ · https://teach.wsu.edu/resources/teaching-toolkit/backward-design/
- **Constructive alignment** — the verb in the outcome is the verb practised and the verb assessed; learners study what they expect to be graded on. Biggs, "Aligning teaching for constructing learning". Primer: https://www.qmul.ac.uk/queenmaryacademy/educators/resources/curriculum-design/constructive-alignment/
- **Revised Bloom verbs** — https://www.coloradocollege.edu/other/assessment/how-to-assess-learning/learning-outcomes/blooms-revised-taxonomy.html · https://teaching.uic.edu/cate-teaching-guides/syllabus-course-design/blooms-taxonomy-of-educational-objectives/
- **Condition + degree in objectives** — Mager, *Preparing Instructional Objectives* (1962); widely reproduced in teaching-centre guides.
- 3–5 objectives per 2–4 h lab; 15–25 % time buffer *(heuristic)*.

## Practice design

- **Worked-example effect** and **expertise reversal** (fade support as the lab goes) — Sweller's cognitive load theory; Kalyuga et al. on expertise reversal: https://www.researchgate.net/publication/226748784_The_expertise_reversal_effect_and_worked_examples_in_tutored_problem_solving
- **Faded worked examples** — Renkl, Atkinson & Große (2004), *Instructional Science* 32.
- **Faded Parsons problems** — Weinman, Fox & Hearst, CHI 2021.
- **Use → Modify → Create** — Lee et al. (2011), "Computational thinking for youth in practice", *ACM Inroads* 2(1).

## Rubrics

- Analytic rubrics, independent criteria, parallel descriptors, 3–5 levels: https://www.assessment.aa.ufl.edu/media/assessmentaaufledu/practical-guide-materials/Module-2d---Rubric-Design.pdf · https://www.umaryland.edu/fctl/resources/assessment/rubrics-and-grading/ · https://www.niu.edu/citl/resources/guides/instructional-guide/rubrics-for-assessment.shtml
- Specification grading (pass/fail against stated specs) — Nilson, *Specifications Grading* (Stylus, 2014).

## Group work

- Positive interdependence and individual accountability — Johnson & Johnson: https://www.co-operation.org/what-is-cooperative-learning
- Behaviour-anchored peer rating (CATME-B) — Ohland et al. (2012), *AMLE* 11(4): https://info.catme.org/wp-content/uploads/Comprehensive-Assessment-of-Team-Member-Effectiveness.pdf
- Git commits vs peer ratings (correlated, gameable, use as cross-check): https://dl.acm.org/doi/10.1145/3593592

## LLM as judge

- Position, verbosity and self-enhancement bias; strong judges agree with humans about as often as humans agree with each other — Zheng et al., NeurIPS 2023: https://arxiv.org/abs/2306.05685
- Decomposed, calibrated rubric questions — Hashemi et al., LLM-Rubric, ACL 2024: https://aclanthology.org/2024.acl-long.745/
- Rubric + reference answer in the judge prompt — Kim et al., Prometheus, ICLR 2024: https://arxiv.org/abs/2310.08491
- Form-filled stepwise scoring; bias toward LLM-written text — Liu et al., G-Eval, EMNLP 2023: https://arxiv.org/abs/2303.16634

## AI use and integrity

- Design for evidence of learning rather than detection — TEQSA (2025): https://www.teqsa.gov.au/sites/default/files/2025-09/enacting-assessment-reform-in-a-time-of-artificial-intelligence.pdf
- AI Assessment Scale (state the permitted level per task): https://arxiv.org/abs/2412.09029

## Skill authoring

- https://agentskills.io/specification · https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices

## Local evidence

- VinUni-AI20k lab repos — see `org-lab-patterns.md`.
- K4 grading QC reports (Oct 2026) — see `grader-pitfalls.md`.
- `auto-grader/docs/lab-package-standard.md` — lab package, calibration gate, submissions as untrusted input.
