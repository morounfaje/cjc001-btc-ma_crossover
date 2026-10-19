import sys
sys.path.append("data")
sys.path.append("strategy")
sys.path.append("backtest")
sys.path.append("portfolio")
sys.path.append("metrics")

import pandas as pd
from loader import validate
from sma_cross import add_smas, add_signals
from ema_cross import add_emas, add_ema_signals
from engine import run_backtest
from benchmark import run_buy_and_hold
from performance import total_return, max_drawdown, trade_stats


def test_strategy(label, df):
    trades, equity_curve = run_backtest(df, fee_rate=0.001, slippage=0.0005)
    ret = total_return(equity_curve, 10000)
    dd = max_drawdown(equity_curve)
    stats = trade_stats(trades)
    print(f"{label:12s}  return: {ret*100:8.2f}%   drawdown: {dd*100:7.2f}%   "
          f"trades: {stats['trade_count']:5d}   win rate: {stats['win_rate']*100:5.1f}%")


raw = pd.read_csv("data/btc_1h.csv")
df = validate(raw)

sma_df = add_signals(add_smas(df.copy()))
test_strategy("SMA 20/50", sma_df)

ema_df = add_ema_signals(add_emas(df.copy()))
test_strategy("EMA 20/50", ema_df)

benchmark_curve = run_buy_and_hold(df, fee_rate=0.001, slippage=0.0005)
print(f"Buy&Hold      return: {total_return(benchmark_curve, 10000)*100:8.2f}%   "
      f"drawdown: {max_drawdown(benchmark_curve)*100:7.2f}%")