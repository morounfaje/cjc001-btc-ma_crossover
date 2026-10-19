import csv
from datetime import datetime, timezone
import requests

URL = "https://api.coingecko.com/api/v3/coins/bitcoin/ohlc"
OUT_PATH = "btc.csv"
DAYS = 365


def fetch_candles():
    params = {"vs_currency": "usd", "days": DAYS}
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def save_csv(candles, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "open", "high", "low", "close"])
        for c in candles:
            ts = datetime.fromtimestamp(c[0] / 1000, tz=timezone.utc).isoformat()
            writer.writerow([ts, c[1], c[2], c[3], c[4]])


if __name__ == "__main__":
    candles = fetch_candles()
    save_csv(candles, OUT_PATH)
    print(f"Saved {len(candles)} candles to {OUT_PATH}")
    print("First:", candles[0])
    print("Second:", candles[1])
    print("Last:", candles[-1])