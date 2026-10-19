import time
import csv
from datetime import datetime, timezone
import requests

URL = "https://api.binance.com/api/v3/klines"
SYMBOL = "BTCUSDT"
INTERVAL = "1h"
BATCH_SIZE = 1000
NUM_BATCHES = 18  # ~18 x 1000 hours ~= 2 years
OUT_PATH = "btc_1h.csv"


def fetch_batch(end_time_ms):
    params = {
        "symbol": SYMBOL,
        "interval": INTERVAL,
        "limit": BATCH_SIZE,
        "endTime": end_time_ms,
    }
    response = requests.get(URL, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def fetch_all_candles():
    all_candles = []
    end_time_ms = int(time.time() * 1000)

    for batch_num in range(NUM_BATCHES):
        candles = fetch_batch(end_time_ms)
        if not candles:
            print(f"Batch {batch_num + 1}: no more data available, stopping early.")
            break

        all_candles = candles + all_candles
        end_time_ms = candles[0][0] - 1
        print(f"Batch {batch_num + 1}/{NUM_BATCHES}: got {len(candles)} candles, total so far: {len(all_candles)}")
        time.sleep(0.5)

    return all_candles


def save_csv(candles, path):
    with open(path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "open", "high", "low", "close"])
        for c in candles:
            ts = datetime.fromtimestamp(c[0] / 1000, tz=timezone.utc).isoformat()
            writer.writerow([ts, c[1], c[2], c[3], c[4]])


if __name__ == "__main__":
    candles = fetch_all_candles()
    candles = candles[:-1]
    save_csv(candles, OUT_PATH)
    print(f"Saved {len(candles)} candles to {OUT_PATH}")
    print("First:", candles[0])
    print("Last:", candles[-1])