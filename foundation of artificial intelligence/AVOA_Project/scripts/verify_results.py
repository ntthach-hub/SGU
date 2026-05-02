from pathlib import Path
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
RESULTS_DIR = PROJECT_ROOT / "results"

EXPECTED_FILES = [
    RESULTS_DIR / "avoa" / "sphere_convergence.png",
    RESULTS_DIR / "avoa" / "rastrigin_convergence.png",
    RESULTS_DIR / "avoa" / "ackley_convergence.png",
    RESULTS_DIR / "pso" / "sphere_convergence.png",
    RESULTS_DIR / "pso" / "rastrigin_convergence.png",
    RESULTS_DIR / "pso" / "ackley_convergence.png",
    RESULTS_DIR / "comparison" / "sphere_comparison.png",
    RESULTS_DIR / "comparison" / "rastrigin_comparison.png",
    RESULTS_DIR / "comparison" / "ackley_comparison.png",
]


def main() -> int:
    missing_files = [path for path in EXPECTED_FILES if not path.exists()]

    if missing_files:
        print("Missing result files:")
        for path in missing_files:
            print(f"- {path.relative_to(PROJECT_ROOT)}")
        return 1

    print("All expected result files are present.")
    for path in EXPECTED_FILES:
        print(f"- {path.relative_to(PROJECT_ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())