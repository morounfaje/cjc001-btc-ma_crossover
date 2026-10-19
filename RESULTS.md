\# CJC001-BTC — MA Crossover Results



\## Dataset

\- Instrument: Bitcoin (BTC-USD)

\- Timeframe: 1-hour candles

\- Period: \~2 years (Oct 2024 - Oct 2026)

\- Candles: 17,331

\- Source: Yahoo Finance via `yfinance` (`data/download\_yfinance.py`), no account/key required

\- Dataset version (SHA-256 fingerprint): `fef57a93796e67e6`



Note on data sourcing: Binance's public API was blocked at the network

level (confirmed via direct browser test, not a code issue). CoinGecko's

free OHLC endpoint only offers coarse 4-day candles for a 1-year+

request. Yahoo Finance via `yfinance` was the data source that actually

worked at the needed granularity and history length.



\## Strategies tested



SMA 20/50 and EMA 20/50 crossover, long-only, next-bar execution.

`starting\_cash = 10,000`, `fee\_rate = 0.001`, `slippage = 0.0005`.



\## Results



| | SMA 20/50 | EMA 20/50 | Buy \& Hold |

|---|---|---|---|

| Return | -46.65% | -40.15% | +19.95% |

| Max drawdown | -65.64% | -62.28% | -53.98% |

| Trades | 197 | 171 | 1 |

| Win rate | 32.5% | 22.8% | - |



\## Key findings



\*\*1. Both crossover strategies badly underperform buy-and-hold.\*\*

Bitcoin itself rose \~20% over this 2-year window; both SMA and EMA lost

money, by wide margins.



\*\*2. EMA's apparent "edge" over SMA is real strategy behavior, not an

outlier artifact.\*\* EMA had a \*lower\* win rate than SMA (22.8% vs

32.5%) but a \*better\* overall return. Investigating EMA's individual

trades (`inspect\_ema\_trades.py`) showed why: total realized profit was

\-$2,563.18, but the top 3 winning trades alone totaled $4,534.76 -

meaning the other 168 trades lost roughly $7,098 combined. The large

winners were \*softening\* losses, not manufacturing a fake profit. This

is the classic trend-following payoff shape: frequent small losses,

occasional large wins - a genuine, if still unprofitable, pattern.



\*\*3. Trade frequency was sane at hourly bars.\*\* \~170-200 trades over 2

years is a reasonable sample; the underperformance reflects the

strategies' actual signal quality on this asset and period, not a

trade-frequency/cost-compounding artifact.



\## Honest overall conclusion



Neither SMA nor EMA 20/50 crossover beat buy-and-hold on BTC-USD hourly

data over this 2-year window. EMA modestly outperformed SMA, and

investigation shows that difference reflects genuine (if still losing)

trend-following behavior rather than a statistical fluke.



\## Reproducing this result

pip install -r requirements.txt

python data/download\_yfinance.py

python compare\_sma\_ema.py

python inspect\_ema\_trades.py





Re-running `download\_yfinance.py` pulls fresh, current data - results

will differ from the dataset version above, since Bitcoin's market data

is continuously updated. The dataset version hash above identifies

exactly which data produced these specific results.

