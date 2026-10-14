import argparse
import csv
import json
import os
import platform
import statistics
import sys
import time
import tracemalloc
from pathlib import Path
from src.scanner import scan_path
from src.metrics import evaluate_findings
from src.visualization import bar_chart_svg

ROOT = Path(__file__).resolve().parent


def write_json(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def write_csv(path, rows):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else []
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def flatten_scan(scan):
    return scan["findings"]


def save_scan(scan, out):
    out = Path(out)
    out.mkdir(parents=True, exist_ok=True)
    write_json(out / "findings.json", scan["findings"])
    summary = {key: scan[key] for key in ("root", "files_scanned", "bytes_scanned")}
    try:
        summary["root"] = Path(summary["root"]).resolve().relative_to(ROOT).as_posix()
    except (ValueError, OSError):
        summary["root"] = str(summary["root"])
    write_json(out / "scan_summary.json", summary)
    write_csv(out / "findings.csv", scan["findings"])
    high_risk = [row for row in scan["findings"] if row.get("severity") == "HIGH"]
    family_counts = {}
    for row in scan["findings"]:
        family_counts[row["family"]] = family_counts.get(row["family"], 0) + 1
    risk_report = {
        "title": "Cryptographic Inventory Risk Report",
        "scope": summary["root"],
        "files_scanned": scan["files_scanned"],
        "bytes_scanned": scan["bytes_scanned"],
        "total_findings": len(scan["findings"]),
        "high_risk_findings": len(high_risk),
        "pqc_indicators": len(scan["findings"]) - len(high_risk),
        "findings_by_family": family_counts,
        "prioritization": "HIGH findings are classical public-key/key-establishment indicators requiring human review; INFO findings indicate possible PQC adoption and are not proof of secure deployment.",
        "limitations": ["Static source indicators may be false positives or miss indirect, aliased, dynamically loaded, binary or dependency-mediated cryptography.", "Do not include secret key material in inventory output.", "Migration decisions require protocol and implementation review."]
    }
    write_json(out / "risk_report.json", risk_report)
    (out / "risk_report.md").write_text(
        "# Cryptographic Inventory Risk Report\\n\\n"
        f"- Scope: `{risk_report['scope']}`\\n"
        f"- Files scanned: {risk_report['files_scanned']}\\n"
        f"- Bytes scanned: {risk_report['bytes_scanned']}\\n"
        f"- Total findings: {risk_report['total_findings']}\\n"
        f"- High-risk classical indicators: {risk_report['high_risk_findings']}\\n"
        f"- PQC indicators: {risk_report['pqc_indicators']}\\n\\n"
        "## Findings by family\\n\\n" +
        "".join(f"- {family}: {count}\\n" for family, count in sorted(family_counts.items())) +
        "\\n## Interpretation\\n\\n" + risk_report["prioritization"] +
        "\\n\\n## Limitations\\n\\n" + "".join(f"- {item}\\n" for item in risk_report["limitations"]),
        encoding="utf-8"
    )


def self_test(out):
    corpus = ROOT / "data" / "raw" / "labeled_corpus"
    labels = ROOT / "tests" / "expected_findings.json"
    scan = scan_path(corpus)
    metrics = evaluate_findings(scan["findings"], labels)
    metrics["files_scanned"] = scan["files_scanned"]
    metrics["bytes_scanned"] = scan["bytes_scanned"]
    save_scan(scan, Path(out) / "self_test")
    write_json(Path(out) / "tables" / "validation_metrics.json", metrics)
    write_csv(Path(out) / "tables" / "validation_metrics.csv", [metrics])
    print(json.dumps(metrics, indent=2))
    return metrics


def run_scan(path, out, max_file_bytes=None, max_files=None):
    scan = scan_path(path, max_file_bytes=max_file_bytes, max_files=max_files)
    save_scan(scan, out)
    counts = {}
    for row in scan["findings"]:
        counts[row["family"]] = counts.get(row["family"], 0) + 1
    summary = {key: scan[key] for key in ("root", "files_scanned", "bytes_scanned")}
    summary["finding_count"] = len(scan["findings"])
    summary["findings_by_family"] = counts
    write_json(Path(out) / "scan_summary.json", summary)
    print(json.dumps(summary, indent=2))
    return scan


def benchmark(path, out, repeats=30, profiles_path=None):
    out = Path(out)
    profiles_path = Path(profiles_path) if profiles_path else ROOT / "platforms" / "platform_profiles.json"
    profiles = json.loads(profiles_path.read_text(encoding="utf-8"))["profiles"]
    rows = []
    for profile in profiles:
        timings = []
        memory_peaks = []
        last_scan = None
        for _ in range(max(1, int(repeats))):
            tracemalloc.start()
            start = time.perf_counter()
            last_scan = scan_path(path, max_file_bytes=profile.get("max_file_bytes"), max_files=profile.get("max_files"))
            timings.append(time.perf_counter() - start)
            _, peak = tracemalloc.get_traced_memory()
            tracemalloc.stop()
            memory_peaks.append(peak)
        mean_seconds = statistics.mean(timings)
        rows.append({
            "profile": profile["name"],
            "profile_status": profile["status"],
            "host_os": platform.platform(),
            "python_version": platform.python_version(),
            "repeats": max(1, int(repeats)),
            "files_scanned": last_scan["files_scanned"],
            "bytes_scanned": last_scan["bytes_scanned"],
            "finding_count": len(last_scan["findings"]),
            "mean_seconds": round(mean_seconds, 8),
            "median_seconds": round(statistics.median(timings), 8),
            "min_seconds": round(min(timings), 8),
            "max_seconds": round(max(timings), 8),
            "bytes_per_second": round(last_scan["bytes_scanned"] / mean_seconds, 2) if mean_seconds else 0,
            "peak_traced_python_bytes_median": int(statistics.median(memory_peaks)),
            "note": profile["note"]
        })
    write_csv(out / "tables" / "platform_comparison.csv", rows)
    write_json(out / "tables" / "platform_comparison.json", {
        "measurement_type": "local same-host resource-budget profile comparison",
        "memory_metric": "Python tracemalloc peak allocation; not total process RSS",
        "warning": "These results do not represent independent physical machines or organizer-measured target platforms. Platform B is an explicit scan-budget emulation.",
        "source_path": str(Path(path)),
        "profiles": rows
    })
    bar_chart_svg([(r["profile"], r["mean_seconds"]) for r in rows], "Mean scan runtime by local profile (seconds)", out / "figures" / "runtime_comparison.svg")
    bar_chart_svg([(r["profile"], r["finding_count"]) for r in rows], "Detected indicators by local profile", out / "figures" / "finding_count_comparison.svg")
    bar_chart_svg([(r["profile"], r["peak_traced_python_bytes_median"]) for r in rows], "Median peak traced Python allocation (bytes)", out / "figures" / "memory_comparison.svg")
    bar_chart_svg([(r["profile"], r["files_scanned"]) for r in rows], "Files scanned by local profile", out / "figures" / "coverage_comparison.svg")
    print(json.dumps(rows, indent=2))
    return rows


def main():
    parser = argparse.ArgumentParser(prog="project-q-p2")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--scan")
    parser.add_argument("--benchmark")
    parser.add_argument("--evaluate")
    parser.add_argument("--labels")
    parser.add_argument("--out", default=str(ROOT / "results"))
    parser.add_argument("--repeats", type=int, default=30)
    parser.add_argument("--max-file-bytes", type=int)
    parser.add_argument("--max-files", type=int)
    args = parser.parse_args()
    if args.self_test:
        self_test(args.out)
    elif args.scan:
        run_scan(args.scan, args.out, args.max_file_bytes, args.max_files)
    elif args.benchmark:
        benchmark(args.benchmark, Path(args.out), args.repeats)
    elif args.evaluate:
        if not args.labels:
            parser.error("--evaluate requires --labels with independently reviewed JSON labels")
        result = run_scan(args.evaluate, args.out)
        metrics = evaluate_findings(result["findings"], args.labels)
        write_json(Path(args.out) / "tables" / "evaluation_metrics.json", metrics)
        write_csv(Path(args.out) / "tables" / "evaluation_metrics.csv", [metrics])
        print(json.dumps(metrics, indent=2))
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
