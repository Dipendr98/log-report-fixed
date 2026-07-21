import json
import re
from collections import Counter
from pathlib import Path


def _expected():
    """Independently recompute the correct answer from the untouched access.log."""
    paths, ips, total = Counter(), set(), 0
    with open("/app/access.log") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            total += 1
            ips.add(line.split()[0])
            m = re.search(r'"(?:GET|POST|PUT|DELETE|HEAD|PATCH) (\S+) ', line)
            if m:
                paths[m.group(1)] += 1
    return total, len(ips), paths


def test_report_exists():
    """The agent produced /app/report.json (not a symlink to another path)."""
    p = Path("/app/report.json")
    assert not p.is_symlink(), "report.json must not be a symlink"
    assert p.exists(), "no report.json found"


def test_report_is_valid_json_object():
    """report.json is a JSON object with the three required keys."""
    data = json.loads(Path("/app/report.json").read_text())
    assert isinstance(data, dict)
    assert {"total_requests", "unique_ips", "top_path"} <= data.keys()


def test_total_requests_correct():
    """total_requests matches the true line count of access.log."""
    total, _, _ = _expected()
    data = json.loads(Path("/app/report.json").read_text())
    assert data["total_requests"] == total


def test_unique_ips_correct():
    """unique_ips matches the true count of distinct client IPs."""
    _, unique_ips, _ = _expected()
    data = json.loads(Path("/app/report.json").read_text())
    assert data["unique_ips"] == unique_ips


def test_top_path_correct():
    """top_path matches the most frequently requested path (ties allowed)."""
    _, _, paths = _expected()
    max_count = max(paths.values())
    valid_top_paths = {p for p, c in paths.items() if c == max_count}
    data = json.loads(Path("/app/report.json").read_text())
    assert data["top_path"] in valid_top_paths


def test_access_log_not_modified():
    """The agent must not modify the input access.log."""
    with open("/app/access.log") as f:
        line_count = sum(1 for line in f if line.strip())
    assert line_count == 6, "access.log appears to have been modified"
