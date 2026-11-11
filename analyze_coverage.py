"""Compare full-suite and smoke-suite coverage, then compute efficiency ratios.

Usage (from the repo root, after creating full.json and smoke.json):
    python analyze_coverage.py full.json smoke.json
"""

import json
import sys

# Median CI timings from the paper (GitHub Actions, 5 clean attempts each).
# Local timings are NOT used, because they depend on your machine.
TEST_TIME = {"full": 31.81, "smoke": 10.37}  # seconds, from timing.txt
JOB_TIME = {"full": 67, "smoke": 46}  # seconds, CI job duration
FAULTS_DETECTED_ON_PUSH = {"full": 10, "smoke": 6}


def load(path):
    with open(path) as f:
        return json.load(f)


def short_name(path):
    return path.replace("\\", "/").split("src/helpdesk/")[-1]


def main(full_path, smoke_path):
    full, smoke = load(full_path), load(smoke_path)
    ft, st = full["totals"], smoke["totals"]

    # 1. Overall coverage
    print("=== 1. Coverage ===")
    print(f"{'':28}{'Full':>10}{'Smoke':>10}")
    stmt_pct = {k: 100 * t["covered_lines"] / t["num_statements"] for k, t in (("full", ft), ("smoke", st))}
    br_pct = {k: 100 * t["covered_branches"] / t["num_branches"] for k, t in (("full", ft), ("smoke", st))}
    comb = {"full": ft["percent_covered"], "smoke": st["percent_covered"]}
    print(f"{'Statements covered':28}{ft['covered_lines']:>10}{st['covered_lines']:>10}  (of {ft['num_statements']})")
    print(f"{'Branches covered':28}{ft['covered_branches']:>10}{st['covered_branches']:>10}  (of {ft['num_branches']})")
    print(f"{'Statement coverage %':28}{stmt_pct['full']:>10.2f}{stmt_pct['smoke']:>10.2f}")
    print(f"{'Branch coverage %':28}{br_pct['full']:>10.2f}{br_pct['smoke']:>10.2f}")
    print(f"{'Combined coverage %':28}{comb['full']:>10.2f}{comb['smoke']:>10.2f}")

    # 2. What full covers that smoke does not, per file
    print("\n=== 2. Statements covered by full but NOT by smoke ===")
    gaps = []
    for path, data in full["files"].items():
        full_lines = set(data["executed_lines"])
        smoke_lines = set(smoke["files"].get(path, {}).get("executed_lines", []))
        gap = len(full_lines - smoke_lines)
        if gap:
            gaps.append((gap, short_name(path), len(full_lines), len(smoke_lines)))
    gaps.sort(reverse=True)
    total_gap = sum(g[0] for g in gaps)
    print(f"Total: {total_gap} statements "
          f"({100 * total_gap / ft['covered_lines']:.0f}% of what full covers)")
    print(f"Branches: {ft['covered_branches'] - st['covered_branches']} "
          f"({100 * (1 - st['covered_branches'] / ft['covered_branches']):.0f}% of what full covers)")
    print(f"\n{'File':28}{'Gap':>6}{'Full':>8}{'Smoke':>8}")
    for gap, name, f_n, s_n in gaps[:12]:
        print(f"{name:28}{gap:>6}{f_n:>8}{s_n:>8}")

    # 3. Efficiency ratios
    print("\n=== 3. Efficiency ratios ===")
    print(f"{'':42}{'Full':>8}{'Smoke':>8}")
    for label, times in (("test time", TEST_TIME), ("CI job time", JOB_TIME)):
        print(f"{'Combined coverage % per s of ' + label:42}"
              f"{comb['full'] / times['full']:>8.2f}{comb['smoke'] / times['smoke']:>8.2f}")
        print(f"{'Faults detected per s of ' + label:42}"
              f"{FAULTS_DETECTED_ON_PUSH['full'] / times['full']:>8.2f}"
              f"{FAULTS_DETECTED_ON_PUSH['smoke'] / times['smoke']:>8.2f}")
    for k in ("full", "smoke"):
        print(f"Fixed CI overhead ({k}): {JOB_TIME[k] - TEST_TIME[k]:.1f} s")

    # 4. Break-even: k pushes per pull request, plus one full run at merge for B
    saving = JOB_TIME["full"] - JOB_TIME["smoke"]
    k = JOB_TIME["full"] / saving
    print("\n=== 4. Break-even ===")
    print(f"A = {JOB_TIME['full']}k s,  B = {JOB_TIME['smoke']}k + {JOB_TIME['full']} s")
    print(f"B saves time only when k > {k:.2f}, i.e. at least {int(k) + 1} pushes per pull request")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        sys.exit("Usage: python analyze_coverage.py full.json smoke.json")
    main(sys.argv[1], sys.argv[2])