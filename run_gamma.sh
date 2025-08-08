#!/bin/bash

# Gamma Profile Analysis Runner
# This script activates the virtual environment and runs the gamma profile analysis

echo "🚀 Starting Gamma Profile Analysis..."
echo "📊 Fetching live SPX options data from CBOE..."

# Add uv to PATH and activate virtual environment
export PATH="$HOME/.local/bin:$PATH"
source gamma-env/bin/activate

# Run the gamma profile analysis
python gammaProfileCommandLine.py SPX

echo "✅ Analysis complete! Charts should have displayed on your screen."
