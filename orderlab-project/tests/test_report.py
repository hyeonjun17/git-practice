from generate_report import build_report


def test_build_report(sample_csv, tmp_path):
    site = tmp_path / "site"
    report = build_report(sample_csv, site)

    assert report == site / "index.html"
    html = report.read_text(encoding="utf-8")
    assert "<h1>OrderLab Report</h1>" in html
    assert "<p>Revenue: 35,000 KRW</p>" in html
