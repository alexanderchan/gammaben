# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Environment Setup

This project uses `uv` as the Python package manager with a virtual environment:

```bash
# Activate environment
export PATH="$HOME/.local/bin:$PATH"
source gamma-env/bin/activate

# Test environment
python test_gamma_simple.py
```

## Common Commands

### Run Gamma Analysis

```bash
# Interactive charts (default)
./run_gamma_enhanced.sh
# Choose option 1 or press Enter

# Save charts to files  
./run_gamma_enhanced.sh
# Choose option 2

# Direct command usage
python gammaProfileCommandLine_enhanced.py SPX          # Interactive
python gammaProfileCommandLine_enhanced.py SPX --save   # Save to files
python gammaProfileCommandLine_enhanced.py SPX --save --output-dir custom_dir
```

### Environment Testing

```bash
python test_gamma_simple.py  # Verify environment and API connectivity
```

## Project Architecture

This is a SPX options gamma exposure analysis tool that:

1. **Fetches live data** from CBOE API (`https://cdn.cboe.com/api/global/delayed_quotes/options/_SPX.json`)
2. **Calculates gamma exposure** using Black-Scholes model via `calcGammaEx()` function
3. **Generates 4 charts**:
   - Total Gamma Exposure by strike
   - Open Interest (Calls vs Puts) 
   - Gamma by Type (Call/Put breakdown)
   - Gamma Profile across price levels
4. **Outputs** either interactively or saves to `gamma_charts/` directory

### Key Components

- `gammaProfileCommandLine_enhanced.py` - Main analysis engine with CLI args
- `gammaProfileCommandLine.py` - Original version (basic)  
- `run_gamma_enhanced.sh` - Interactive runner script with user options
- `run_gamma.sh` - Basic runner script
- `test_gamma_simple.py` - Environment verification script

### Dependencies (Python 3.7.3)

- pandas 1.3.5 (compatibility optimized)
- numpy 1.21.6
- scipy 1.7.3  
- matplotlib 3.5.3
- requests 2.31.0
- urllib3 1.26.20 (downgraded for OpenSSL compatibility)

## Financial Calculations

**Gamma Exposure Formula**: `GEX = Unit Gamma × Open Interest × Contract Size × Spot Price × 0.01`

- **Positive Gamma**: Market makers short gamma (stabilizing)
- **Negative Gamma**: Market makers long gamma (destabilizing)  
- **Gamma Flip Point**: SPX level where market transitions between regimes

The `calcGammaEx()` function implements Black-Scholes gamma calculation with proper handling for calls/puts and zero-time/zero-vol edge cases.

## Chart Output

Charts are saved as high-resolution PNG files (300 DPI) to `gamma_charts/` directory:
- `1_total_gamma_exposure.png`
- `2_open_interest.png` 
- `3_gamma_by_type.png`
- `4_gamma_profile.png`

## Data Processing Pipeline

1. Strike filtering: 80%-120% of current spot price
2. Expiration parsing from option symbol format
3. Call/Put data merging and validation  
4. Black-Scholes gamma calculation per option
5. Aggregation and visualization

The code includes `isThirdFriday()` helper for monthly expiry detection and handles real-time CBOE data parsing.