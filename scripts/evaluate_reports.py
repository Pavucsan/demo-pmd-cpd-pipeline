"""Parse PMD/CPD XML and expose an unambiguous quality result to Actions."""

import os
from pathlib import Path
import xml.etree.ElementTree as ET


def count_elements(path: Path, local_name: str) -> int:
    root = ET.parse(path).getroot()
    return sum(1 for element in root.iter() if element.tag.rsplit("}", 1)[-1] == local_name)


def main() -> None:
    pmd_count = count_elements(Path("target/pmd.xml"), "violation")
    cpd_count = count_elements(Path("target/cpd.xml"), "duplication")
    kind = "quality_violation" if pmd_count or cpd_count else "success"
    summary = f"PMD violations: {pmd_count}; CPD duplications: {cpd_count}"

    output_path = os.environ.get("GITHUB_OUTPUT")
    if output_path:
        with open(output_path, "a", encoding="utf-8") as output:
            output.write(f"kind={kind}\n")
            output.write(f"summary={summary}\n")
    print(summary)


if __name__ == "__main__":
    main()

