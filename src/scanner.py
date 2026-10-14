import ast
from pathlib import Path
from src.rules import COMPILED_RULES

SUPPORTED_EXTENSIONS = {".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go", ".rs", ".c", ".h", ".cpp", ".hpp", ".cs", ".php", ".rb", ".swift", ".kt", ".scala", ".yaml", ".yml", ".toml", ".ini", ".cfg", ".conf", ".json", ".xml"}
SKIPPED_DIRS = {".git", ".hg", ".svn", ".venv", "venv", "__pycache__", "node_modules", "dist", "build", ".tox", ".mypy_cache", ".pytest_cache"}


def _python_ast_families(text):
    found = {}
    try:
        tree = ast.parse(text)
    except (SyntaxError, ValueError, TypeError):
        return found
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            module = (node.module or "").lower()
            for alias in node.names:
                name = alias.name.lower()
                family = None
                if name == "rsa" or name == "rsaencryption":
                    family = "RSA"
                elif name == "dsa":
                    family = "DSA"
                elif name in {"ec", "ecdsa", "ecdh", "ellipticcurve"}:
                    family = "ELLIPTIC_CURVE"
                elif name in {"dh", "diffiehellman"}:
                    family = "DIFFIE_HELLMAN"
                if family and ("cryptography" in module or "crypto.publickey" in module or "asymmetric" in module):
                    found.setdefault(node.lineno, set()).add(family)
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            attribute = node.func.attr.lower()
            family = None
            if attribute in {"generate_private_key", "generate_key"} and isinstance(node.func.value, ast.Name) and node.func.value.id.lower() == "rsa":
                family = "RSA"
            if family:
                found.setdefault(node.lineno, set()).add(family)
    return found


def _source_files(root, max_file_bytes=None, max_files=None):
    root = Path(root)
    if root.is_file():
        candidates = [root]
    else:
        candidates = []
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix.lower() not in SUPPORTED_EXTENSIONS:
                continue
            if any(part in SKIPPED_DIRS for part in path.parts):
                continue
            candidates.append(path)
    candidates.sort(key=lambda p: str(p).lower())
    selected = []
    for path in candidates:
        try:
            size = path.stat().st_size
        except OSError:
            continue
        if max_file_bytes is not None and size > int(max_file_bytes):
            continue
        if max_files is not None and len(selected) >= int(max_files):
            break
        selected.append(path)
    return selected


def scan_path(root, max_file_bytes=None, max_files=None):
    requested_root = Path(root).expanduser()
    root = requested_root.resolve()
    root_label = str(requested_root) if not requested_root.is_absolute() else str(root)
    if not root.exists():
        raise FileNotFoundError(f"Scan path does not exist: {root}")
    files = _source_files(root, max_file_bytes=max_file_bytes, max_files=max_files)
    findings = []
    bytes_scanned = 0
    for path in files:
        try:
            raw = path.read_bytes()
        except OSError:
            continue
        if max_file_bytes is not None and len(raw) > int(max_file_bytes):
            continue
        bytes_scanned += len(raw)
        text = raw.decode("utf-8", errors="replace")
        ast_findings = _python_ast_families(text) if path.suffix.lower() == ".py" else {}
        for line_number, line in enumerate(text.splitlines(), start=1):
            families = set(ast_findings.get(line_number, set()))
            for rule, pattern in COMPILED_RULES:
                if pattern.search(line):
                    if rule["family"] == "DSA" and pattern.search(line) and "ML-DSA" in line.upper():
                        continue
                    families.add(rule["family"])
            for family in sorted(families):
                rule = next(item for item, _ in COMPILED_RULES if item["family"] == family)
                findings.append({
                    "file": str(path.relative_to(root)) if root.is_dir() else path.name,
                    "line": line_number,
                    "family": family,
                    "category": rule["category"],
                    "severity": rule["severity"],
                    "risk_score": 90 if rule["severity"] == "HIGH" else 10,
                    "risk_reason": "Quantum-vulnerable public-key/key-establishment indicator" if rule["severity"] == "HIGH" else "Post-quantum algorithm indicator; verify implementation and parameter set",
                    "evidence": line.strip()[:240],
                    "recommendation": rule["recommendation"]
                })
    return {"root": root_label, "files_scanned": len(files), "bytes_scanned": bytes_scanned, "findings": findings}
