# Tree Samples - Code Migration Utilities

A collection of utilities and documentation for analyzing and migrating REST API codebases using ripgrep.

## 📁 Files Overview

### Documentation

- **`ideas.md`** - Comprehensive migration strategies guide
  - REST to GraphQL migration patterns
  - Python to Java mapping techniques
  - Dependency tracing methodologies
  - Automated discovery approaches

### Ripgrep Utilities (`ripgrep_ideas/`)

- **`ripgrep_cmd.md`** - Quick reference ripgrep commands
  - Find REST endpoints in Java/Python
  - Locate HTTP client usage
  - Search configuration files
  - Trace property references

- **`ripgrep.py`** - Advanced endpoint migration tracker
  - `EndpointMigrationTracker` class for comprehensive analysis
  - Multi-phase search (URLs → properties → HTTP calls → variable tracing)
  - JSON output parsing from ripgrep
  - Automated migration report generation

- **`rg_script.py`** - Simple URL search utility
  - Quick script to find URL references
  - Domain-based searching
  - HTTP client pattern detection

## 🚀 Usage with UV

### Prerequisites
- Install [uv](https://github.com/astral-sh/uv): `curl -LsSf https://astral.sh/uv/install.sh | sh`
- Install [ripgrep](https://github.com/BurntSushi/ripgrep): `brew install ripgrep` (macOS) or equivalent

### Running Scripts

#### Simple Service Endpoint Search
```bash
# Edit service_endpoints dict in rg_script.py first (format: {"service_name": "/endpoint/path"}), then run:
uv run python ripgrep_ideas/rg_script.py
```

#### Advanced Migration Tracking
```bash
# Use the EndpointMigrationTracker class programmatically:
uv run python -c "
from ripgrep_ideas.ripgrep import EndpointMigrationTracker

tracker = EndpointMigrationTracker(
    project_root='/path/to/your/project',
    urls=['https://api.example.com/v1/users']
)

report = tracker.generate_migration_report('https://api.example.com/v1/users')
print(report)
"
```

#### Interactive Python Session
```bash
# Launch Python REPL with uv to explore the migration tracker:
uv run python

# Then in Python:
>>> from ripgrep_ideas.ripgrep import EndpointMigrationTracker
>>> tracker = EndpointMigrationTracker('.', ['https://your-url.com'])
>>> results = tracker.search_literal_urls('https://your-url.com')
>>> print(results)
```

#### Run Manual Ripgrep Commands
```bash
# Use commands from ripgrep_cmd.md directly, for example:

# Find Java REST endpoints
rg -t java -A 3 -B 1 '@(RequestMapping|GetMapping|PostMapping|PutMapping|DeleteMapping)\('

# Find Python HTTP calls
rg -t py -A 3 'requests\.(get|post|put|delete)|urlopen|httpx\.|aiohttp'

# Search configuration files
rg -g '*.{properties,yml,yaml,json,env}' 'api|endpoint|url|service'
```

## 🔍 Use Cases

1. **REST to GraphQL Migration** - Identify all REST endpoints before migrating
2. **Python to Java Port** - Map dependencies and trace file relationships
3. **Endpoint Discovery** - Find all API consumers in a codebase
4. **Configuration Audit** - Locate hardcoded URLs and external dependencies
5. **Refactoring Analysis** - Understand code impact before changes

## 📝 Quick Start Example

```bash
# 1. Clone/navigate to your target project
cd /path/to/project

# 2. Search for specific endpoint usage
uv run python -c "
from ripgrep_ideas.ripgrep import EndpointMigrationTracker

tracker = EndpointMigrationTracker(
    project_root='.',
    urls=['https://api.legacy.com/users']
)

# Find literal references
results = tracker.search_literal_urls('https://api.legacy.com/users')
for file, matches in results.items():
    print(f'{file}:')
    for match in matches:
        print(f'  Line {match[\"line\"]}: {match[\"content\"].strip()}')
"
```

## 🛠️ Customization

Edit the scripts to customize for your needs:
- **Service endpoints**: Modify `service_endpoints` dict in `rg_script.py` (format: `{"service_name": "/endpoint/path"}`)
- **Search patterns**: Add custom regex patterns in `ripgrep.py`
- **File types**: Adjust `-g` glob patterns for different languages
- **Context lines**: Change `-A`/`-B` parameters for more/less context
