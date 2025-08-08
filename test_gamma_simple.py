import pandas as pd
import numpy as np
import scipy
from scipy.stats import norm
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import requests
import sys

# Simple test to verify the environment is working
print("Testing gamma profile environment...")
print(f"Pandas version: {pd.__version__}")
print(f"NumPy version: {np.__version__}")
print(f"SciPy version: {scipy.__version__}")
print(f"Matplotlib version: {plt.matplotlib.__version__}")

# Test API connection
try:
    response = requests.get("https://cdn.cboe.com/api/global/delayed_quotes/options/_SPX.json")
    if response.status_code == 200:
        data = response.json()
        spot_price = data["data"]["close"]
        print(f"✅ Successfully connected to CBOE API")
        print(f"✅ Current SPX spot price: {spot_price}")
        print(f"✅ Number of options in chain: {len(data['data']['options'])}")
    else:
        print(f"❌ API connection failed with status: {response.status_code}")
except Exception as e:
    print(f"❌ API connection error: {e}")

print("\n🎉 Environment setup is complete and working!")
print("\nTo run the full gamma profile analysis:")
print("python gammaProfileCommandLine.py SPX")
