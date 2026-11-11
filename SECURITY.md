# Security Policy

## Supported scope

`Automate-Workflow/automation-tools` is a documentation and data repository containing `data/tools.csv`, generated Markdown files, SVG assets, and a Python standard-library generator script (`scripts/generate.py`). It does not publish binaries or operate hosted services.

## Reporting a vulnerability

Please do not open public issues for security-sensitive reports. Report concerns using one of the following private channels:

- GitHub private vulnerability reporting: `https://github.com/Automate-Workflow/automation-tools/security/advisories/new`
- Email: `ayush_24a12res897@iitp.ac.in`

Include the affected file path or URL, reproduction steps or evidence, and the nature of the risk.

## Expected response times

- **Acknowledgement**: Within 7 days of receiving the report.
- **Assessment and remediation**: Confirmed issues involving malicious links, hijacked URLs, or exposed secrets are prioritized for immediate removal or correction.

## What counts as a security report

- Malicious, compromised, or phishing URLs in `data/tools.csv` or Markdown files.
- Wrong, spoofed, or hijacked repository URLs pointing to unintended owners or domains.
- Leaked secrets, API tokens, or credentials committed anywhere in the repository.
- Code execution, workflow injection, or unsafe behavior in `scripts/generate.py` or `.github/workflows/`.

## What does not count

- **Vulnerabilities in listed third-party tools**: Report security bugs in any listed tool directly to that project's upstream maintainers.
- **Routine metadata updates**: Broken links from normal project renames, license updates, or new tool suggestions should be submitted through the repository issue templates or a pull request.
