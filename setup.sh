#!/bin/bash

echo "================================================================================"
echo "🔧 SETUP GUIDE - Inventory Optimization with Machine Learning"
echo "================================================================================"
echo ""

# Check if running on macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "📱 Detected: macOS"
    echo ""
    
    # Check for Xcode Command Line Tools
    if xcode-select -p &> /dev/null; then
        echo "✅ Xcode Command Line Tools: Installed"
    else
        echo "❌ Xcode Command Line Tools: NOT installed"
        echo ""
        echo "🔨 REQUIRED STEP 1: Install Xcode Command Line Tools"
        echo "   Run this command in terminal:"
        echo "   $ xcode-select --install"
        echo ""
        echo "   Then click 'Install' in the popup dialog."
        echo "   This will take a few minutes..."
        echo ""
        read -p "Press Enter after installing Xcode Command Line Tools..."
    fi
fi

echo ""
echo "================================================================================"
echo "📦 STEP 2: Installing Python Dependencies"
echo "================================================================================"
echo ""

# Check Python
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✅ Python found: $PYTHON_VERSION"
else
    echo "❌ Python 3 not found. Please install Python 3.8+"
    exit 1
fi

echo ""
echo "Installing base dependencies..."
pip3 install pandas numpy matplotlib seaborn scipy plotly --quiet --upgrade

echo ""
echo "Installing ML libraries (this may take a few minutes)..."
pip3 install scikit-learn statsmodels xgboost --quiet --upgrade

echo ""
echo "Installing Prophet (optional, may take longer)..."
pip3 install prophet --quiet --upgrade 2>&1 | grep -v "Warning" || echo "⚠️  Prophet installation failed (optional)"

echo ""
echo "================================================================================"
echo "✅ INSTALLATION COMPLETE!"
echo "================================================================================"
echo ""

# Run test
echo "🧪 Running system test..."
echo ""

cd "$(dirname "$0")"
python3 test_simple.py

if [ $? -eq 0 ]; then
    echo ""
    echo "================================================================================"
    echo "🎉 SUCCESS! Your system is ready to use!"
    echo "================================================================================"
    echo ""
    echo "🚀 Quick Start Commands:"
    echo ""
    echo "   1. Run main system:"
    echo "      $ python3 main.py"
    echo ""
    echo "   2. Compare ML algorithms:"
    echo "      $ python3 demo_ml.py"
    echo ""
    echo "   3. Test specific algorithm:"
    echo "      $ python3 demo_ml.py xgboost"
    echo ""
    echo "   4. Run examples:"
    echo "      $ python3 examples.py"
    echo ""
    echo "📖 Documentation:"
    echo "   - README.md - Project overview"
    echo "   - ML_GUIDE.md - ML algorithms guide"
    echo ""
else
    echo ""
    echo "⚠️  Some tests failed. Please check the error messages above."
fi
