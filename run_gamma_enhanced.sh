#!/bin/bash

# Enhanced Gamma Profile Analysis Runner
# This script provides options for displaying charts interactively or saving to files

echo "🚀 Enhanced Gamma Profile Analysis"
echo "📊 Fetching live SPX options data from CBOE..."

# Add uv to PATH and activate virtual environment
export PATH="$HOME/.local/bin:$PATH"
source gamma-env/bin/activate

echo ""
echo "Choose an option:"
echo "1) Display charts interactively (default)"
echo "2) Save charts to files"
echo ""
read -p "Enter choice (1 or 2): " choice

case $choice in
    2)
        echo "💾 Saving charts to gamma_charts/ directory..."
        python gammaProfileCommandLine_enhanced.py SPX --save
        echo ""
        echo "📁 Charts saved! You can view them with:"
        echo "   open gamma_charts/"
        echo "   or individually:"
        echo "   open gamma_charts/1_total_gamma_exposure.png"
        echo "   open gamma_charts/2_open_interest.png"
        echo "   open gamma_charts/3_gamma_by_type.png"
        echo "   open gamma_charts/4_gamma_profile.png"
        ;;
    *)
        echo "🖼️  Displaying charts interactively..."
        python gammaProfileCommandLine_enhanced.py SPX
        echo ""
        echo "ℹ️  Chart Navigation Tips:"
        echo "   • Use toolbar buttons to zoom, pan, and navigate"
        echo "   • Click and drag to zoom into specific areas"
        echo "   • Right-click for context menu options"
        echo "   • Press 'r' to reset zoom"
        echo "   • Close each chart window to proceed to the next"
        ;;
esac

echo ""
echo "✅ Analysis complete!"
