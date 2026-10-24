"""Fail CI on dependency vulnerabilities the Space can actually fix.

Reads `pip-audit --format json` output. Every advisory fails the build except
Pillow advisories whose only fix is Pillow 13 or newer: no Gradio release
allows Pillow 13 yet (Gradio 6 requires pillow<13), and this app takes no image
input, so Pillow's image-decoding flaws are not reachable through it. Once
Gradio allows Pillow 13, the resolver picks it and those advisories disappear;
a Pillow advisory with a fix below 13 fails the build, since it is installable.
"""

from __future__ import annotations

import json
import sys

PILLOW_CAP_MAJOR = 13  # Gradio 6 requires pillow<13


def _major(version: str) -> int:
    return int(version.split(".")[0])


def main(path: str) -> int:
    report = json.load(open(path))
    blocking, deferred = [], []
    for dep in report.get("dependencies", []):
        for vuln in dep.get("vulns", []):
            entry = f"{dep['name']} {dep['version']} {vuln['id']} (fixed in {', '.join(vuln['fix_versions']) or 'no release'})"
            fixable_under_cap = any(_major(v) < PILLOW_CAP_MAJOR for v in vuln["fix_versions"])
            if dep["name"].lower() == "pillow" and vuln["fix_versions"] and not fixable_under_cap:
                deferred.append(entry)
            else:
                blocking.append(entry)
    for entry in deferred:
        print(f"deferred (needs Pillow {PILLOW_CAP_MAJOR}+, blocked by Gradio): {entry}")
    for entry in blocking:
        print(f"VULNERABLE: {entry}")
    print(f"{len(blocking)} blocking, {len(deferred)} deferred")
    return 1 if blocking else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
