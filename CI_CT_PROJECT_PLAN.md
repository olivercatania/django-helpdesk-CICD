# CIS*4150 — CI/CT Applied Research Project: Source of Truth

**Repository:** `olivercatania/django-helpdesk-CICD`  
**Working branch:** `ci-ct-rebuild`  
**Team:** Oliver Catania and Jian Lim  
**Project:** Compare full-suite testing on every commit (Strategy A) with a runtime-selected fast subset on commits and a full pre-merge test (Strategy B).  
**Submission deadline:** Wednesday, December 2, 2026, 11:59 p.m. (CourseLink).  
**Authoritative requirements:** Course `Term_Project_ver_3-1.pdf`, Option 1 rubric, submitted team goal document; this checklist operationalizes them. If the instructor/TA approves a scope change, document it below before changing the experiment.

## Current position (November 2, 2026)

- [x] Existing full-suite WSL baseline collected on October 26, 2026 (`baseline-wsl/`). Its commit differs from the CI run: `8c7b9ff92f018a394c6faa972e4328ad178b80b9`.
- [x] Existing full-suite GitHub Actions baseline collected and verified: commit `26f57b5d40b57dd999bb5aec433883f979a9ae93`, Python 3.12.3, 503 tests (501 passed, 2 skipped), measured test command 30.49 s, combined coverage 78.44%.
- [x] Clean Git state on `ci-ct-rebuild` confirmed by user screenshot; this is the same commit as the CI artifact.
- [x] Plan and initial focused regression test module prepared in the Step 1/2 bundle.
- [ ] Copy the project plan, baseline CI notes, and test module into the local working tree, then commit this checklist; archive the original GitHub Actions ZIP outside Git (or in a clearly labeled results archive).
- [ ] Run the new regression test module and the full suite **on clean application code**. Do not count the tests as validated until these commands pass.

**Baseline source:** GitHub Actions artifact `full-test-41532518241-1(1).zip` (original CI run; exact commit in `baseline-ci/run-01/commit.txt`). Local WSL timings are *not* directly comparable to GitHub Actions timings because the machines and commits differ.

## Rules for the experiment

1. **Never delete unrelated existing regression tests to make the full suite faster.** The full suite is all existing tests plus any accepted new tests.
2. **Freeze the tests and fast subset before any fault injections.** Choose the fast subset based on timed clean runs, not on which injected faults it will catch.
3. **Compare identical application states and planned commit sequences** for Strategy A and B. Use isolated branches/scenarios; never merge intentionally faulty application code into stable `main`.
4. **Keep the two workflow triggers separate.** Strategy A: full suite on each experiment commit. Strategy B: fast suite on each experiment commit; full suite at the planned pre-merge gate. Avoid triggering the full suite on every Strategy B push via another workflow or an already-open PR.
5. **Track command runtime AND complete CI workflow runtime separately.** Setup overhead can mask test-command savings.
6. **A detected fault requires a test failure attributable to that fault.** Infrastructure failures, setup problems, and expected messages logged by passing tests are not detections.
7. **Coverage does not equal detection effectiveness.** Report statement/branch coverage alongside observed fault detections.
8. **Save exact SHAs, environment/dependency versions, test counts, logs, run URLs/IDs, and repeatable commands** so results are independently verifiable.

## Step 1 — Preserve a clean baseline

**Status: evidence captured; archive/commit organization pending.**

- [x] Record clean starting commit, environment and baseline test counts.
- [x] Preserve existing local WSL baseline.
- [x] Download working full GitHub Actions baseline and inspect test/coverage/timing artifacts.
- [ ] Commit this checklist and `baseline-ci/run-01/README.md` / compact evidence files.
- [ ] Keep the downloaded original CI artifact as the raw baseline; optionally record the original run URL.

**Acceptance:** A reader can identify the original clean source version and retrieve/reproduce its full-suite run. This is **historical baseline evidence**, not the final A-vs-B measurement after tests are added.

## Step 2 — Design/implement project-specific regression tests

**Status: in progress (unvalidated test module prepared).**

- [x] Inspect existing ticket creation, ticket model/status and queue-permission tests.
- [x] Prepare `tests/test_ci_regression_dependencies.py` with four dependency-resolution scenarios on clean code: no blockers, mixed resolved/unresolved blockers, unblock after resolution, block again after reopening.
- [ ] Run `python quicktest.py tests.test_ci_regression_dependencies -v 2` in the project WSL environment; investigate any failures.
- [ ] Run `python quicktest.py` and confirm all baseline tests plus new tests pass.
- [ ] Examine `tests/test_ticket_submission.py` and add a *nonduplicate* validation assertion if it adds coverage (e.g., invalid private-queue submission creates no ticket).
- [ ] Examine `tests/test_per_queue_staff_permission.py` and strengthen an uncovered or weak permission assertion, without changing expected correct behaviour.
- [ ] Record test case ID, tested requirement, input/initial state, oracle (expected result), and target code area for each added case.
- [ ] Commit validated tests **before** timing/selection/fault injection; freeze these tests for subsequent experiments.

**Acceptance:** Original application code passes all tests; targeted new cases have documented expected results. No injected faults exist in the frozen baseline.

## Step 3 — Profile test modules and freeze the fast subset

**Status: not started.**

- [ ] Decide a selection rule and runtime budget **before** introducing faults (e.g., choose quickest clean modules up to a prespecified time limit). Explain limitations of purely runtime-based selection.
- [ ] On the CI-equivalent environment, measure individual candidate test modules repeatedly. Record command, commit, runtime and test count. Note repeated database/startup cost for separate module runs.
- [ ] Form a candidate fast subset, then measure the entire subset together (do not just add individual module times).
- [ ] Measure full vs fast statement and branch coverage on the *same frozen clean commit*.
- [ ] Freeze the list of module labels in the plan and the Strategy B workflow; do not adjust it based on observed fault outcomes.

**Acceptance:** The exact fast module list, selection rationale, and baseline runtimes/coverage are recorded and reproducible.

**Fast subset (fill after profiling):** `TBD`  
**Selection rule/runtime budget:** `TBD`  
**Frozen clean commit:** `TBD`

## Step 4 — Implement two nonoverlapping CI strategies

**Status: not started; current `ci.yml` only implements full-suite testing.**

- [ ] Preserve/parameterize installation, Python 3.12.3, dependency pins, coverage instrumentation and artifact capture.
- [ ] Strategy A: execute all tests for each predefined experiment commit.
- [ ] Strategy B: run the fixed fast subset after each commit; full regression suite once at the planned pre-merge stage.
- [ ] Carefully isolate event filters and branches: do not run both full and fast jobs on Strategy B push, and avoid repeated full PR runs before the planned gate.
- [ ] Save timing, tests.log, coverage reports, commit, environment, and run metadata even on test failures.

**Acceptance:** Both configured CI strategies clearly implement their intended schedules and leave inspectable evidence.

## Step 5 — Validate both strategies on clean frozen code

**Status: not started.**

- [ ] Verify full and fast jobs pass on identical clean source/test versions.
- [ ] Verify no accidental full-suite runs occur on Strategy B commit pushes.
- [ ] Trigger a clean Strategy B pull request to verify full pre-merge checks; close validation PR without merging if appropriate.
- [ ] Collect repeated clean timings for **both** configurations on the same runner/dependency environment (suggestion: at least five runs per configuration; document the actual number).
- [ ] Record median and spread separately for instrumented test execution and whole workflow duration.

**Acceptance:** Correct tests run at correct events, evidence is captured, and final clean A-vs-B comparison baseline is established.

## Step 6 — Inject 10–15 controlled faults and replay identical scenarios

**Status: not started.**

- [ ] Design 10–15 distinct, realistic application faults across ticket creation, status updates/dependencies and permissions as promised in the goal document.
- [ ] For every candidate fault, document source location, intended incorrect behaviour, expected test oracle and clean starting commit.
- [ ] Verify each fault is caught by the frozen **full suite**; replace unsuitable fault candidates without retuning the fast subset.
- [ ] Predefine feature branch commit sequence, fault-introduction commit, and merge-gate event for each scenario.
- [ ] Replay equivalent code/commit states under Strategy A and Strategy B. Reset or isolate each fault so earlier failures cannot obscure later outcomes.
- [ ] Save run links, timestamps, SHAs, test names, failure excerpts, coverage and runtime for every scheduled test event.
- [ ] Never merge intentionally faulty branches into `main`.

**Acceptance:** The same planned fault scenarios have verifiable test evidence under both strategies.

## Step 7 — Analyze results and validity

**Status: not started.**

- [ ] Compute total Strategy A vs B **instrumented test-command** time for matched commit sequences and percentage saved.
- [ ] Separately compare total **GitHub Actions workflow** time including setup and artifacts.
- [ ] Count faults caught at push, caught only pre-merge, and never caught. Do not label a pre-merge detection as permanently missed.
- [ ] Compute fault-detection delay in commits/events and wall-clock minutes; explicitly define start/end timestamps and handling of undetected faults.
- [ ] Compare full/fast statement and branch coverage; explain why coverage and fault detection differ.
- [ ] Make labeled charts of runtimes, detection stages/delays and coverage; cite exact run IDs/data.
- [ ] Discuss repetitions/variance, seeded-fault realism, one-project generalizability, timing noise, clean-suite selection bias, and other validity threats.

**Acceptance:** Results answer the research question with reproducible numbers, not anecdotal conclusions.

## Step 8 — Report, evidence and submission

**Status: not started.**

- [ ] Draft ~10-page Option 1 report using the supplied MS Word template: title, academic integrity statement, introduction, methodology/test requirements/harness/oracles, findings, discussion, conclusion, references.
- [ ] Include AI-use declaration/checklist as required by the course guidelines where applicable.
- [ ] Explain both strategies, test design, fast-selection method, fault methodology, reproducibility and exact experiment timeline.
- [ ] Include clearly captioned charts/tables, detection and timing data, limitations and practical recommendations.
- [ ] Provide contribution appendix with evidence from Git history and agreed member responsibilities.
- [ ] Archive workflows, test scripts, fault patch/commit identifiers, run evidence, logs and analysis data in supplementary ZIP if appropriate.
- [ ] Verify naming/submission instructions and upload the final report and supporting file(s) before **December 2, 2026 at 11:59 p.m.**

**Acceptance:** Professional, replicable report and documented evidence addressing rubric dimensions: problem/scope (20%), methodology (25%), evidence (25%), analysis (20%), presentation (10%).

## Responsibilities (from approved team goal document)

- **Jian:** lead test design and controlled fault injection.
- **Oliver:** lead CI workflow implementation, profiling/selection and Coverage.py measurements.
- **Both:** agree on experiment protocol, interpret results, write and review the report.
- Both members should provide demonstrable test-related contributions and Git evidence. Update actual allocation if responsibilities change.

## Experiment data register (fill during Steps 3–7)

| Scenario / run ID | Commit SHA | Strategy | Stage | Test modules | Tests passed/failed/skipped | Test time (s) | Workflow time (s) | Statement % | Branch % | Fault detected? / failing test | Run URL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| original-CI-run-01 | `26f57b5d40b57dd999bb5aec433883f979a9ae93` | historical full baseline | clean push | full | 501 / 0 / 2 | 30.49 | not recorded | 81.57 | 67.13 | N/A (clean code) | GitHub run 41532518241 |

**Change log:** Record changes to scope, test-set selection, timing protocol and fault list here *before* the relevant measurement, with date and reason.
