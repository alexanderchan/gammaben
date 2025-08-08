# SPX Gamma Profile Analysis

A comprehensive tool for analyzing SPX options gamma exposure using live CBOE data.

## 🚀 Quick Start

### Interactive Charts (Default)

```bash
./run_gamma_enhanced.sh
# Choose option 1 or just press Enter
```

### Save Charts to Files

```bash
./run_gamma_enhanced.sh
# Choose option 2
```

### Direct Command Usage

```bash
# Activate environment
export PATH="$HOME/.local/bin:$PATH"
source gamma-env/bin/activate

# Interactive display
python gammaProfileCommandLine_enhanced.py SPX

# Save to files
python gammaProfileCommandLine_enhanced.py SPX --save

# Custom output directory
python gammaProfileCommandLine_enhanced.py SPX --save --output-dir my_analysis
```

## 📊 What You Get

### 4 Professional Charts

1. **Total Gamma Exposure** - Net gamma by strike price
2. **Open Interest** - Call vs Put distribution
3. **Gamma by Type** - Separate call/put gamma analysis
4. **Gamma Profile** - How gamma changes with price movement

### Key Metrics

- **Current SPX Price**: Live market data
- **Total Gamma**: Dollar exposure per 1% move
- **Gamma Flip Point**: Critical price level for market behavior

## 🖼️ Chart Interaction

### When Charts Display Interactively:

- **Zoom**: Click and drag to zoom into areas
- **Pan**: Use pan tool to move around
- **Reset**: Press 'r' or use home button
- **Save**: Use toolbar to save current view
- **Navigate**: Close each chart to see the next one

### When Charts Are Saved:

- High-resolution PNG files (300 DPI)
- Saved to `gamma_charts/` directory
- Open with: `open gamma_charts/`

## 📈 Analysis Insights

### Gamma Flip Point

- **Above flip point**: Positive gamma environment (dampens moves)
- **Below flip point**: Negative gamma environment (accelerates moves)
- **Current analysis**: Flip point at 6,319 (SPX at 6,385)

### Market Structure

- **$75.01 Billion** total gamma per 1% SPX move
- **12,367** option pairs analyzed
- **Live CBOE data** updated in real-time

## 🛠️ Environment Details

### Python Environment

- **Python**: 3.7.3 (compatible with older systems)
- **Package Manager**: uv (fast, modern)
- **Virtual Environment**: `gamma-env/`

### Key Libraries

- **pandas**: 1.3.5 (compatibility optimized)
- **numpy**: 1.21.6
- **scipy**: 1.7.3
- **matplotlib**: 3.5.3
- **requests**: 2.31.0

## 📚 Documentation

- **[CHART_GUIDE.md](CHART_GUIDE.md)**: Detailed chart interpretation guide
- **[test_gamma_simple.py](test_gamma_simple.py)**: Environment verification script

## 🔧 Troubleshooting

### Environment Issues

```bash
# Test environment
python test_gamma_simple.py

# Reinstall if needed
uv pip install pandas numpy scipy matplotlib requests "urllib3<2.0"
```

### Chart Display Issues

- Ensure virtual environment is activated
- Check matplotlib backend: `python -c "import matplotlib.pyplot as plt; print(plt.get_backend())"`
- Use `--save` flag if interactive display fails

### API Connection

- Script fetches live data from CBOE
- No API key required
- Handles rate limiting automatically

## 📊 Sample Output

```
🔄 Fetching SPX options data from CBOE...
💰 SPX Spot Price: 6385.38
📊 Processing 12367 option pairs...
📈 Generating Chart 1: Total Gamma Exposure...
📈 Generating Chart 2: Open Interest...
📈 Generating Chart 3: Gamma by Call/Put...
📈 Generating Chart 4: Gamma Profile...

✅ Analysis Complete!
📊 Total Gamma: $75.01 Bn per 1% SPX move
🎯 Gamma Flip Point: 6319
```

## 🎯 Use Cases

- **Day Trading**: Identify key support/resistance levels
- **Options Strategy**: Understand market maker positioning
- **Risk Management**: Monitor gamma exposure changes
- **Market Analysis**: Track regime changes (positive/negative gamma)

---

_Built with ❤️ using modern Python tooling and live market data_
