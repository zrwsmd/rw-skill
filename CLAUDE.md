# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture
This repository contains a collection of **Skills** for Claude.
- **Root Directory**: `skill/` contains all skills.
- **Skill Structure**: Each skill is in a subdirectory (e.g., `skill/code-review-fixer/`) containing:
  - `SKILL.md`: Metadata, description, and workflow definition for the skill.
  - `scripts/`: Python scripts that implement the skill's logic.

## Development & Testing
There is no central build system. Skills are developed and tested individually.

### Python Environment
- Scripts are written in Python 3.
- Dependencies: `pandas`, `openpyxl` are commonly used.

### Running Skill Scripts
Scripts are typically run from the root of the repository or the skill directory.

**Example: Parsing a code review report**
```bash
python skill/code-review-fixer/scripts/parse_code_review_report.py --input "path/to/report.html" --severity "严重"
```

**Example: Converting HTML report to Excel**
```bash
python skill/review-html-to-xlsx/scripts/code_review_report_to_xlsx.py --input "path/to/report.html"
```

## Code Style
- Follow Python PEP 8 standards for scripts.
- `SKILL.md` files must follow the specific YAML frontmatter and section headers format.
