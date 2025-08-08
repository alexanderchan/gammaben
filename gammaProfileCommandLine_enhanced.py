import pandas as pd
import numpy as np
import scipy
from scipy.stats import norm
import matplotlib.pyplot as plt
from datetime import datetime, timedelta, date
import requests
import sys
import argparse
import os

pd.options.display.float_format = '{:,.4f}'.format

# Black-Scholes European-Options Gamma
def calcGammaEx(S, K, vol, T, r, q, optType, OI):
    if T == 0 or vol == 0:
        return 0

    dp = (np.log(S/K) + (r - q + 0.5*vol**2)*T) / (vol*np.sqrt(T))
    dm = dp - vol*np.sqrt(T)

    if optType == 'call':
        gamma = np.exp(-q*T) * norm.pdf(dp) / (S * vol * np.sqrt(T))
        return OI * 100 * S * S * 0.01 * gamma
    else: # Gamma is same for calls and puts. This is just to cross-check
        gamma = K * np.exp(-r*T) * norm.pdf(dm) / (S * S * vol * np.sqrt(T))
        return OI * 100 * S * S * 0.01 * gamma

def isThirdFriday(d):
    return d.weekday() == 4 and 15 <= d.day <= 21

def save_or_show_chart(save_path=None, chart_name="chart"):
    """Save chart to file or show interactively"""
    if save_path:
        filename = os.path.join(save_path, f"{chart_name}.png")
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"📊 Saved: {filename}")
    else:
        plt.show()

# Parse command line arguments
parser = argparse.ArgumentParser(description='SPX Gamma Profile Analysis')
parser.add_argument('index', help='Index symbol (e.g., SPX)')
parser.add_argument('--save', '-s', action='store_true', help='Save charts to directory instead of displaying')
parser.add_argument('--output-dir', '-o', default='gamma_charts', help='Output directory for saved charts')
args = parser.parse_args()

index = args.index
save_charts = args.save
output_dir = args.output_dir if args.save else None

# Create output directory if saving charts
if save_charts:
    os.makedirs(output_dir, exist_ok=True)
    print(f"📁 Charts will be saved to: {output_dir}/")

# Get options data
print(f"🔄 Fetching {index} options data from CBOE...")
response = requests.get(url="https://cdn.cboe.com/api/global/delayed_quotes/options/_" + index + ".json")
options = response.json()

# Get SPX Spot
spotPrice = options["data"]["close"]
print(f"💰 {index} Spot Price: {spotPrice}")
fromStrike = 0.8 * spotPrice
toStrike = 1.2 * spotPrice

# Get Today's Date
todayDate = date.today()

# Get SPX Options Data
data_df = pd.DataFrame(options["data"]["options"])

data_df['CallPut'] = data_df['option'].str.slice(start=-9,stop=-8)
data_df['ExpirationDate'] = data_df['option'].str.slice(start=-15,stop=-9)
data_df['ExpirationDate'] = pd.to_datetime(data_df['ExpirationDate'], format='%y%m%d')
data_df['Strike'] = data_df['option'].str.slice(start=-8,stop=-3)
data_df['Strike'] = data_df['Strike'].str.lstrip('0')

data_df_calls = data_df.loc[data_df['CallPut'] == "C"]
data_df_puts = data_df.loc[data_df['CallPut'] == "P"]
data_df_calls = data_df_calls.reset_index(drop=True)
data_df_puts = data_df_puts.reset_index(drop=True)

df = data_df_calls[['ExpirationDate','option','last_trade_price','change','bid','ask','volume','iv','delta','gamma','open_interest','Strike']]
df_puts = data_df_puts[['ExpirationDate','option','last_trade_price','change','bid','ask','volume','iv','delta','gamma','open_interest','Strike']]
df_puts.columns = ['put_exp','put_option','put_last_trade_price','put_change','put_bid','put_ask','put_volume','put_iv','put_delta','put_gamma','put_open_interest','put_strike']

df = pd.concat([df, df_puts], axis=1)

df['check'] = np.where((df['ExpirationDate'] == df['put_exp']) & (df['Strike'] == df['put_strike']), 0, 1)

if df['check'].sum() != 0:
    print("PUT CALL MERGE FAILED - OPTIONS ARE MISMATCHED.")
    exit()

df.drop(['put_exp', 'put_strike', 'check'], axis=1, inplace=True)

print(f"📊 Processing {len(df)} option pairs...")

df.columns = ['ExpirationDate','Calls','CallLastSale','CallNet','CallBid','CallAsk','CallVol',
              'CallIV','CallDelta','CallGamma','CallOpenInt','StrikePrice','Puts','PutLastSale',
              'PutNet','PutBid','PutAsk','PutVol','PutIV','PutDelta','PutGamma','PutOpenInt']

df['ExpirationDate'] = pd.to_datetime(df['ExpirationDate'], format='%a %b %d %Y')
df['ExpirationDate'] = df['ExpirationDate'] + timedelta(hours=16)
df['StrikePrice'] = df['StrikePrice'].astype(float)
df['CallIV'] = df['CallIV'].astype(float)
df['PutIV'] = df['PutIV'].astype(float)
df['CallGamma'] = df['CallGamma'].astype(float)
df['PutGamma'] = df['PutGamma'].astype(float)
df['CallOpenInt'] = df['CallOpenInt'].astype(float)
df['PutOpenInt'] = df['PutOpenInt'].astype(float)

# ---=== CALCULATE SPOT GAMMA ===---
# Gamma Exposure = Unit Gamma * Open Interest * Contract Size * Spot Price
# To further convert into 'per 1% move' quantity, multiply by 1% of spotPrice
df['CallGEX'] = df['CallGamma'] * df['CallOpenInt'] * 100 * spotPrice * spotPrice * 0.01
df['PutGEX'] = df['PutGamma'] * df['PutOpenInt'] * 100 * spotPrice * spotPrice * 0.01 * -1

df['TotalGamma'] = (df.CallGEX + df.PutGEX) / 10**9
dfAgg = df.groupby(['StrikePrice']).sum(numeric_only=True)
strikes = dfAgg.index.values

print("📈 Generating Chart 1: Total Gamma Exposure...")
# Chart 1: Absolute Gamma Exposure
plt.figure(figsize=(12, 8))
plt.grid()
plt.bar(strikes, dfAgg['TotalGamma'].to_numpy(), width=6, linewidth=0.1, edgecolor='k', label="Gamma Exposure")
plt.xlim([fromStrike, toStrike])
chartTitle = "Total Gamma: $" + str("{:.2f}".format(df['TotalGamma'].sum())) + " Bn per 1% " + index + " Move"
plt.title(chartTitle, fontweight="bold", fontsize=20)
plt.xlabel('Strike', fontweight="bold")
plt.ylabel('Spot Gamma Exposure ($ billions/1% move)', fontweight="bold")
plt.axvline(x=spotPrice, color='r', lw=1, label=index + " Spot: " + str("{:,.0f}".format(spotPrice)))
plt.legend()
save_or_show_chart(output_dir, "1_total_gamma_exposure")

print("📈 Generating Chart 2: Open Interest...")
# Chart 2: Open Interest by Calls and Puts
plt.figure(figsize=(12, 8))
plt.grid()
plt.bar(strikes, dfAgg['CallOpenInt'].to_numpy(), width=6, linewidth=0.1, edgecolor='k', label="Call OI")
plt.bar(strikes, -1 * dfAgg['PutOpenInt'].to_numpy(), width=6, linewidth=0.1, edgecolor='k', label="Put OI")
plt.xlim([fromStrike, toStrike])
chartTitle = "Total Open Interest for " + index
plt.title(chartTitle, fontweight="bold", fontsize=20)
plt.xlabel('Strike', fontweight="bold")
plt.ylabel('Open Interest (number of contracts)', fontweight="bold")
plt.axvline(x=spotPrice, color='r', lw=1, label=index + " Spot:" + str("{:,.0f}".format(spotPrice)))
plt.legend()
save_or_show_chart(output_dir, "2_open_interest")

print("📈 Generating Chart 3: Gamma by Call/Put...")
# Chart 3: Absolute Gamma Exposure by Calls and Puts
plt.figure(figsize=(12, 8))
plt.grid()
plt.bar(strikes, dfAgg['CallGEX'].to_numpy() / 10**9, width=6, linewidth=0.1, edgecolor='k', label="Call Gamma")
plt.bar(strikes, dfAgg['PutGEX'].to_numpy() / 10**9, width=6, linewidth=0.1, edgecolor='k', label="Put Gamma")
plt.xlim([fromStrike, toStrike])
chartTitle = "Total Gamma: $" + str("{:.2f}".format(df['TotalGamma'].sum())) + " Bn per 1% " + index + " Move"
plt.title(chartTitle, fontweight="bold", fontsize=20)
plt.xlabel('Strike', fontweight="bold")
plt.ylabel('Spot Gamma Exposure ($ billions/1% move)', fontweight="bold")
plt.axvline(x=spotPrice, color='r', lw=1, label=index + " Spot:" + str("{:,.0f}".format(spotPrice)))
plt.legend()
save_or_show_chart(output_dir, "3_gamma_by_type")

print("📈 Generating Chart 4: Gamma Profile...")
# ---=== CALCULATE GAMMA PROFILE ===---
levels = np.linspace(fromStrike, toStrike, 30)

# For 0DTE options, I'm setting DTE = 1 day, otherwise they get excluded
df['daysTillExp'] = [1/262 if (np.busday_count(todayDate, x.date())) == 0 \
                           else np.busday_count(todayDate, x.date())/262 for x in df.ExpirationDate]

nextExpiry = df['ExpirationDate'].min()

df['IsThirdFriday'] = [isThirdFriday(x) for x in df.ExpirationDate]
thirdFridays = df.loc[df['IsThirdFriday'] == True]
nextMonthlyExp = thirdFridays['ExpirationDate'].min()

totalGamma = []
totalGammaExNext = []
totalGammaExFri = []

# For each spot level, calc gamma exposure at that point
for level in levels:
    df['callGammaEx'] = df.apply(lambda row : calcGammaEx(level, row['StrikePrice'], row['CallIV'],
                                                          row['daysTillExp'], 0, 0, "call", row['CallOpenInt']), axis = 1)

    df['putGammaEx'] = df.apply(lambda row : calcGammaEx(level, row['StrikePrice'], row['PutIV'],
                                                         row['daysTillExp'], 0, 0, "put", row['PutOpenInt']), axis = 1)

    totalGamma.append(df['callGammaEx'].sum() - df['putGammaEx'].sum())

    exNxt = df.loc[df['ExpirationDate'] != nextExpiry]
    totalGammaExNext.append(exNxt['callGammaEx'].sum() - exNxt['putGammaEx'].sum())

    exFri = df.loc[df['ExpirationDate'] != nextMonthlyExp]
    totalGammaExFri.append(exFri['callGammaEx'].sum() - exFri['putGammaEx'].sum())

totalGamma = np.array(totalGamma) / 10**9
totalGammaExNext = np.array(totalGammaExNext) / 10**9
totalGammaExFri = np.array(totalGammaExFri) / 10**9

# Find Gamma Flip Point
zeroCrossIdx = np.where(np.diff(np.sign(totalGamma)))[0]

negGamma = totalGamma[zeroCrossIdx]
posGamma = totalGamma[zeroCrossIdx+1]
negStrike = levels[zeroCrossIdx]
posStrike = levels[zeroCrossIdx+1]

# Writing and sharing this code is only possible with your support!
# If you find it useful, consider supporting us at perfiliev.com/support :)
zeroGamma = posStrike - ((posStrike - negStrike) * posGamma/(posGamma-negGamma))
zeroGamma = zeroGamma[0]

# Chart 4: Gamma Exposure Profile
plt.figure(figsize=(12, 8))
fig, ax = plt.subplots(figsize=(12, 8))
plt.grid()
plt.plot(levels, totalGamma, label="All Expiries", linewidth=2)
plt.plot(levels, totalGammaExNext, label="Ex-Next Expiry", linewidth=2)
plt.plot(levels, totalGammaExFri, label="Ex-Next Monthly Expiry", linewidth=2)
chartTitle = "Gamma Exposure Profile, " + index + ", " + todayDate.strftime('%d %b %Y')
plt.title(chartTitle, fontweight="bold", fontsize=20)
plt.xlabel('Index Price', fontweight="bold")
plt.ylabel('Gamma Exposure ($ billions/1% move)', fontweight="bold")
plt.axvline(x=spotPrice, color='r', lw=1, label=index + " Spot: " + str("{:,.0f}".format(spotPrice)))
plt.axvline(x=zeroGamma, color='g', lw=1, label="Gamma Flip: " + str("{:,.0f}".format(zeroGamma)))
plt.axhline(y=0, color='grey', lw=1)
plt.xlim([fromStrike, toStrike])
trans = ax.get_xaxis_transform()
plt.fill_between([fromStrike, zeroGamma], min(totalGamma), max(totalGamma), facecolor='red', alpha=0.1, transform=trans)
plt.fill_between([zeroGamma, toStrike], min(totalGamma), max(totalGamma), facecolor='green', alpha=0.1, transform=trans)
plt.legend()
save_or_show_chart(output_dir, "4_gamma_profile")

print(f"\n✅ Analysis Complete!")
print(f"📊 Total Gamma: ${df['TotalGamma'].sum():.2f} Bn per 1% {index} move")
print(f"🎯 Gamma Flip Point: {zeroGamma:.0f}")
if save_charts:
    print(f"💾 All charts saved to: {output_dir}/")
else:
    print("🖼️  Charts displayed in interactive windows")
