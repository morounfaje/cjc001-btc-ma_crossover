import csv
from datetime import datetime, timezone
import yfinance as yf

SYMBOL = "BTC-USD"
INTERVAL = "1h"
PERIOD = "2y"
OUT_PATH = "btc_1h.csv"


def fetch_candles():
    data = yf.download(SYMBOL, period=PERIOD, interval=INTERVAL)
    return data


def save_csv(df, path):
    df = df.reset_index()
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "open", "high", "low", "close"])
        for _, row in df.iterrows():
            ts = row["Datetime"]
            if ts.tzinfo is None:
                ts = ts.tz_localize(timezone.utc)
            else:
                ts = ts.tz_convert(timezone.utc)
            writer.writerow([ts.isoformat(), row["Open"], row["High"], row["Low"], row["Close"]])


if __name__ == "__main__":
    data = fetch_candles()
    save_csv(data, OUT_PATH)
    print(f"Saved {len(data)} candles to {OUT_PATH}")
    print(data.head())
    print(data.tail())