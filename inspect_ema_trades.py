import sys
sys.path.append("data")
sys.path.append("strategy")
sys.path.append("backtest")
sys.path.append("portfolio")

import pandas as pd
from loader import validate
from ema_cross import add_emas, add_ema_signals
from engine import run_backtest

raw = pd.read_csv("data/btc_1h.csv")
df = validate(raw)
df = add_ema_signals(add_emas(df))

trades, equity_curve = run_backtest(df, fee_rate=0.001, slippage=0.0005)

profits = []
for i in range(0, len(trades) - 1, 2):
    buy = trades[i]
    sell = trades[i + 1]
    if buy["action"] != "BUY" or sell["action"] != "SELL":
        continue
    cost = buy["price"] * buy["shares"]
    proceeds = sell["cash"]
    profit = proceeds - cost
    profits.append(profit)

print(f"Total closed trades: {len(profits)}")
print(f"Total profit: {sum(profits):.2f}")
print(f"Biggest single win:  {max(profits):.2f}")
print(f"Biggest single loss: {min(profits):.2f}")

sorted_profits = sorted(profits, reverse=True)
top_3_sum = sum(sorted_profits[:3])
total = sum(profits)
print(f"Sum of top 3 winning trades: {top_3_sum:.2f}")
if total != 0:
    print(f"That's {top_3_sum / total * 100:.1f}% of total profit")

top_10 = sorted_profits[:10]
print(f"\nTop 10 individual trade profits: {[round(p, 2) for p in top_10]}")