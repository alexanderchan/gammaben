# Gamma Profile Chart Guide

## 📊 Chart Overview

The gamma profile analysis generates 4 key charts that help analyze SPX options market structure:

### 1. Total Gamma Exposure (`1_total_gamma_exposure.png`)

- **What it shows**: Net gamma exposure by strike price
- **Key insights**:
  - Positive bars = net long gamma (market makers short gamma)
  - Negative bars = net short gamma (market makers long gamma)
  - Large bars indicate significant gamma concentration

### 2. Open Interest (`2_open_interest.png`)

- **What it shows**: Call vs Put open interest distribution
- **Key insights**:
  - Green bars (above zero) = Call open interest
  - Red bars (below zero) = Put open interest
  - Shows where most options activity is concentrated

### 3. Gamma by Call/Put (`3_gamma_by_type.png`)

- **What it shows**: Separate gamma exposure for calls vs puts
- **Key insights**:
  - Green bars = Call gamma exposure
  - Red bars = Put gamma exposure (negative)
  - Helps identify which option type is driving gamma

### 4. Gamma Profile (`4_gamma_profile.png`)

- **What it shows**: How gamma exposure changes as SPX price moves
- **Key insights**:
  - Blue line = Total gamma across all expiries
  - Orange line = Gamma excluding next expiry
  - Green line = Gamma excluding next monthly expiry
  - **Gamma Flip Point**: Where gamma changes from negative to positive
  - Red shaded area = Negative gamma region (accelerating moves)
  - Green shaded area = Positive gamma region (dampening moves)

## 🖼️ Interactive Chart Navigation

When charts display interactively (without `--save` flag), you can:

### Toolbar Controls

- **🏠 Home**: Reset to original view
- **⬅️➡️ Back/Forward**: Navigate through zoom history
- **🔍 Pan**: Click and drag to move around the chart
- **🔍 Zoom**: Click and drag to zoom into specific areas
- **⚙️ Configure**: Adjust subplot parameters
- **💾 Save**: Save current view to file

### Keyboard Shortcuts

- **`r`**: Reset zoom to original view
- **`f`**: Toggle fullscreen mode
- **`g`**: Toggle grid on/off
- **`l`**: Toggle log/linear scale (y-axis)
- **`k`**: Toggle log/linear scale (x-axis)

### Mouse Controls

- **Left click + drag**: Zoom into selected area
- **Right click**: Context menu with additional options
- **Mouse wheel**: Zoom in/out at cursor position
- **Middle click + drag**: Pan the chart

## 🚀 Usage Examples

### Save Charts to Files

```bash
# Save all charts as PNG files
python gammaProfileCommandLine_enhanced.py SPX --save

# Save to custom directory
python gammaProfileCommandLine_enhanced.py SPX --save --output-dir my_charts

# Using the enhanced runner script
./run_gamma_enhanced.sh
# Then choose option 2
```

### Display Interactive Charts

```bash
# Display charts interactively
python gammaProfileCommandLine_enhanced.py SPX

# Using the enhanced runner script
./run_gamma_enhanced.sh
# Then choose option 1 (default)
```

### View Saved Charts

```bash
# Open all charts in default image viewer
open gamma_charts/

# View individual charts
open gamma_charts/1_total_gamma_exposure.png
open gamma_charts/2_open_interest.png
open gamma_charts/3_gamma_by_type.png
open gamma_charts/4_gamma_profile.png
```

## 📈 Interpreting the Analysis

### Key Metrics Displayed

- **SPX Spot Price**: Current index level
- **Total Gamma**: Dollar amount of gamma exposure per 1% SPX move
- **Gamma Flip Point**: Price level where gamma changes sign

### Trading Implications

- **Above Gamma Flip**: Positive gamma environment
  - Market makers buy dips, sell rallies
  - Tends to dampen price movements
- **Below Gamma Flip**: Negative gamma environment
  - Market makers sell dips, buy rallies
  - Tends to accelerate price movements

### Chart Analysis Tips

1. **Look for gamma concentration**: Large bars indicate key support/resistance levels
2. **Monitor the flip point**: Distance from current price indicates regime
3. **Compare expiry effects**: See how upcoming expirations impact gamma
4. **Track changes over time**: Run analysis regularly to see shifts

## 🔧 Troubleshooting

### Charts Not Displaying

- Ensure you're in the virtual environment: `source gamma-env/bin/activate`
- Check if matplotlib backend supports display: `python -c "import matplotlib.pyplot as plt; plt.plot([1,2,3]); plt.show()"`

### Charts Too Small/Large

- Modify figure size in the script: `plt.figure(figsize=(width, height))`
- Use interactive zoom controls to adjust view

### Save Directory Issues

- Script automatically creates the output directory
- Check permissions if directory creation fails
- Use absolute paths if needed: `--output-dir /full/path/to/charts`
