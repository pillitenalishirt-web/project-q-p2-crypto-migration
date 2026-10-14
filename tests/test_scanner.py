import json
import tempfile
import unittest
from pathlib import Path
from src.scanner import scan_path, _python_ast_families
from src.metrics import evaluate_findings

ROOT = Path(__file__).resolve().parents[1]
CORPUS = ROOT / "data" / "raw" / "labeled_corpus"
LABELS = ROOT / "tests" / "expected_findings.json"


class ScannerTests(unittest.TestCase):
    def test_labelled_corpus_metrics(self):
        scan = scan_path(CORPUS)
        metrics = evaluate_findings(scan["findings"], LABELS)
        self.assertEqual(metrics["false_negatives"], 0)
        self.assertEqual(metrics["false_positives"], 0)
        self.assertEqual(metrics["precision"], 1.0)
        self.assertEqual(metrics["recall"], 1.0)

    def test_missing_path_raises(self):
        with self.assertRaises(FileNotFoundError):
            scan_path(ROOT / "does-not-exist")

    def test_neutral_file_has_no_crypto_findings(self):
        scan = scan_path(CORPUS / "neutral_app.py")
        self.assertEqual(scan["findings"], [])

    def test_ast_recognizes_asymmetric_imports(self):
        source = "from cryptography.hazmat.primitives.asymmetric import rsa as keygen"
        self.assertEqual(_python_ast_families(source), {1: {"RSA"}})

    def test_profile_limits_are_respected(self):
        scan = scan_path(CORPUS, max_file_bytes=1)
        self.assertEqual(scan["files_scanned"], 0)
        self.assertEqual(scan["findings"], [])

    def test_multilanguage_fixtures_detect_classical_and_pqc_indicators(self):
        fixture = ROOT / "data" / "raw" / "multilang_demo"
        scan = scan_path(fixture)
        metrics = evaluate_findings(scan["findings"], ROOT / "tests" / "multilang_expected_findings.json")
        self.assertGreaterEqual(scan["files_scanned"], 3)
        self.assertEqual(metrics["false_negatives"], 0)
        self.assertEqual(metrics["false_positives"], 0)
        self.assertEqual(metrics["precision"], 1.0)
        self.assertEqual(metrics["recall"], 1.0)

    def test_findings_include_risk_fields(self):
        scan = scan_path(CORPUS)
        self.assertTrue(scan["findings"])
        self.assertIn("risk_score", scan["findings"][0])
        self.assertIn("risk_reason", scan["findings"][0])


if __name__ == "__main__":
    unittest.main()
