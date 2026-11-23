from pathlib import Path

from orderlab.csv_report import revenue_from_csv


def build_report(
    csv_path: str | Path = "data/sample_orders.csv",
    output_dir: str | Path = "site",
) -> Path:
    revenue = revenue_from_csv(csv_path)
    site = Path(output_dir)
    site.mkdir(parents=True, exist_ok=True)
    report = site / "index.html"
    report.write_text(
        f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>OrderLab Report</title>
</head>
<body>
  <main>
    <h1>OrderLab Report</h1>
    <p>Revenue: {revenue:,} KRW</p>
  </main>
</body>
</html>
""",
        encoding="utf-8",
    )
    return report


if __name__ == "__main__":
    build_report()
