# Quick Start Guide

## 1. Install
```bash
pip install infradocs
# or from source:
pip install -e .
```

## 2. Create sample data
```bash
infradocs init my-network
cd my-network
```
This creates a `sample-data/` folder and `config.yaml`.

## 3. Edit your data
Open `sample-data/devices.yaml` and replace the sample entries with your own devices.

## 4. Build
```bash
infradocs build --input sample-data --output output/site
```

## 5. View
Open `output/site/index.html` in your browser.

For full documentation see the `docs/` folder.
