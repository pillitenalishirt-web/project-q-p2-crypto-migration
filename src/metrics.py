import json
from pathlib import Path


def finding_keys(findings, root=None):
    keys = set()
    for row in findings:
        file_name = row["file"].replace("\\", "/")
        keys.add((file_name, int(row["line"]), row["family"]))
    return keys


def evaluate_findings(findings, labels_path):
    expected_rows = json.loads(Path(labels_path).read_text(encoding="utf-8"))
    expected = {(row["file"].replace("\\", "/"), int(row["line"]), row["family"]) for row in expected_rows}
    detected = finding_keys(findings)
    true_positive = len(expected & detected)
    false_positive = len(detected - expected)
    false_negative = len(expected - detected)
    precision = true_positive / (true_positive + false_positive) if true_positive + false_positive else 0.0
    recall = true_positive / (true_positive + false_negative) if true_positive + false_negative else 0.0
    f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
    return {
        "label_source": str(Path("tests") / Path(labels_path).name),
        "unit": "relative file path + line number + algorithm family",
        "true_positives": true_positive,
        "false_positives": false_positive,
        "false_negatives": false_negative,
        "precision": round(precision, 4),
        "recall": round(recall, 4),
        "f1": round(f1, 4),
        "label_count": len(expected),
        "prediction_count": len(detected),
        "interpretation": "Metrics apply only to this labelled corpus and are not a general performance estimate."
    }
