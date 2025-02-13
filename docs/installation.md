# Installation Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git (for version control)

## Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/supply-chain-scanner.git
cd supply-chain-scanner
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install the package in development mode:
```bash
pip install -e ".[dev]"
```

## Configuration

1. Copy the default configuration:
```bash
cp src/supply_chain_scanner/config/default_config.json config.json
```

2. Edit the configuration file according to your needs:
```bash
nano config.json  # or use your preferred editor
```

## Verification

1. Run the tests to ensure everything is working:
```bash
pytest tests/
```

2. Run a sample scan:
```bash
python -m supply_chain_scanner --config config.json
```

## Troubleshooting

If you encounter any issues during installation:

1. Ensure Python version is correct:
```bash
python --version
```

2. Verify virtual environment is activated:
```bash
which python  # should point to your venv
```

3. Check installed packages:
```bash
pip list
```

## Additional Setup

### For Development

Install development dependencies:
```bash
pip install -e ".[dev]"
```

### For Production

Install only production dependencies:
```bash
pip install .
```