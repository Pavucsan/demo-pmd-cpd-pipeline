# Create one email-friendly ZIP containing every available quality report.
from pathlib import Path
import zipfile

ARCHIVE = Path("target/quality-reports.zip")
REPORT_PATTERNS = (
    "target/pmd.xml",
    "target/cpd.xml",
    "target/reports/**/*",
    "target/surefire-reports/**/*",
)


def main() -> None:
    files = sorted(
        {
            path
            for pattern in REPORT_PATTERNS
            for path in Path().glob(pattern)
            if path.is_file() and path != ARCHIVE
        }
    )
    if not files:
        print("No reports are available; the email will be sent without an attachment.")
        return

    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(ARCHIVE, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to("target"))
    print(f"Created {ARCHIVE} with {len(files)} report files.")


if __name__ == "__main__":
    main()

