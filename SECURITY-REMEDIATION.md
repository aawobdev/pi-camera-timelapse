# Security Remediation Plan - pi-camera-timelapse

_Generated 2026-10-08 from the trivy full scan (weekly CVE job), re-run 2026-10-08._

This document lists the dependency vulnerabilities found in this repo and what needs to change. It is a plan, not a fix - apply it deliberately and run the test suite afterwards.

**Summary:** 2 findings across 1 packages - 🔴 1 critical, 🟠 1 high, 🟡 0 medium.

## Vulnerable packages

| Package | Installed | 🔴 | 🟠 | 🟡 | Fixed version |
|---|---|---|---|---|---|
| `pycrypto` | 2.6.1 | 1 | 1 | 0 | **none available** |

## ⚠️ No fix available

- **`pycrypto`** (2.6.1) - Abandoned since 2013. Replace with `pycryptodome` (drop-in: `from Crypto.Cipher import ...` works the same) or remove the dependency if unused.

## How to fix

This repo pins Python deps in `requirements.txt` - bump the entries and reinstall into the venv.

```bash
pip install -r requirements.txt   # inside the project venv
# run the test suite before committing
```


## Notes

- Severity counts are per (CVE, package) pair; the same upstream bug often appears under several transitive dependency paths.
- Some advisories are fixed in multiple release lines (e.g. `7.5.5` or `8.0.1`) - pick the line that matches your major version.
- Fixes can introduce breaking changes at major-version boundaries. Run the test suite and, for deployed apps, verify the running service afterwards.
- Re-run `trivy fs --severity CRITICAL,HIGH,MEDIUM .` to confirm the findings clear.

