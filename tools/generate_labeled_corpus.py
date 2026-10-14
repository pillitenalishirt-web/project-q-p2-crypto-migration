from pathlib import Path
import json
import shutil

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "data" / "raw" / "labeled_corpus"
DESTINATION = ROOT / "data" / "processed" / "benchmark_corpus"


def main():
    if DESTINATION.exists():
        shutil.rmtree(DESTINATION)
    DESTINATION.mkdir(parents=True)
    for index in range(1, 151):
        source = SOURCE / ("legacy_crypto.py" if index % 3 else "pqc_names.py")
        target = DESTINATION / f"module_{index:03d}.py"
        text = source.read_text(encoding="utf-8")
        target.write_text(text + f"\nmodule_number = {index}\n", encoding="utf-8")
    manifest = {"generated_file_count": len(list(DESTINATION.glob("*.py"))), "source": "bundled labelled demonstration fixtures", "use": "runtime stress demonstration only; not a public open-source repository"}
    (DESTINATION / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
