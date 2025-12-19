#FamPay Data Engineering Assessment
# Main script for processing stock data and generating monthly aggregates with technical indicators

import os
import sys
import warnings
from typing import Dict

import pandas as pd

# Suppressing FutureWarnings for cleaner output
warnings.filterwarnings('ignore', category=FutureWarning)


#Load stock data from CSV file
def load_data(file_path: str) -> pd.DataFrame:
    
    try:
        df = pd.read_csv(file_path)
        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values(["ticker", "date"])
        print(
            f" Data loaded successfully: {len(df)} rows, "
            f"{df['ticker'].nunique()} unique tickers"
        )
        
#Returns DataFrame with parsed date column
        return df
    except FileNotFoundError:
        print(f" Error: File '{file_path}' not found!")
        sys.exit(1)
    except Exception as e:
        print(f"  Error loading data: {str(e)}")
        sys.exit(1)

# Resampling daily stock data to monthly frequency with OHLC logic.
def aggregate_to_monthly(df: pd.DataFrame) -> pd.DataFrame:
       
    monthly_data = []

    for ticker in df["ticker"].unique():
        ticker_df = df[df["ticker"] == ticker].copy()
        ticker_df = ticker_df.sort_values("date")
        ticker_df.set_index("date", inplace=True)

        # Monthly OHLC using month-end labels
        monthly = pd.DataFrame(
            {
                "open": ticker_df["open"].resample("ME").first(),   # First day's open
                "high": ticker_df["high"].resample("ME").max(),     # Max high in month
                "low": ticker_df["low"].resample("ME").min(),       # Min low in month
                "close": ticker_df["close"].resample("ME").last(),  # Last day's close
            }
        )

        monthly["ticker"] = ticker
        monthly.reset_index(inplace=True)
        monthly_data.append(monthly)

    result = pd.concat(monthly_data, ignore_index=True)
    print(f"Monthly aggregation complete: {len(result)} rows")

    #Returns DataFrame with monthly aggregated data
    return result

# Calculate Simple Moving Average on a close-price series.
def calculate_sma(close: pd.Series, window: int) -> pd.Series:
    
    # Returns: Series with SMA values (NaN for first window-1 periods)
    
    return close.rolling(window=window, min_periods=window).mean()

# Calculate Exponential Moving Average with SMA seeding.
def calculate_ema_with_sma_seed(close: pd.Series, window: int) -> pd.Series:
    """
    EMA is defined as:
        EMA_t = (Close_t - EMA_{t-1}) * Multiplier + EMA_{t-1}
    where Multiplier = 2 / (window + 1)

    For the first EMA value, the SMA over the first `window` points is used
    as the "previous EMA", exactly as described in the prompt.

    """
    close = close.astype(float).reset_index(drop=True)
    n = len(close)
    ema = pd.Series([float('nan')] * n, dtype=float)

    if n < window:
        # Not enough data to compute first SMA -> all NaN
        return ema

    # Calculate SMA for first window as seed
    sma_seed = close.iloc[:window].mean()
    ema.iloc[window - 1] = sma_seed

    multiplier = 2.0 / (window + 1)

    # Iterate forward and apply recursive EMA formula
    prev_ema = sma_seed
    for i in range(window, n):
        price = close.iloc[i]
        curr_ema = (price - prev_ema) * multiplier + prev_ema
        ema.iloc[i] = curr_ema
        prev_ema = curr_ema

    #  Returns: Series with EMA values; NaN until enough history is available.
    return ema

# Add SMA and EMA indicators to the dataset.
def add_technical_indicators(df: pd.DataFrame) -> pd.DataFrame:
    #Indicators are computed per ticker on monthly closing prices.
    
    result_data = []

    for ticker in df["ticker"].unique():
        ticker_df = df[df["ticker"] == ticker].copy()
        ticker_df = ticker_df.sort_values("date").reset_index(drop=True)

        close = ticker_df["close"]

        # SMA with strict window requirement
        ticker_df["sma_10"] = calculate_sma(close, 10)
        ticker_df["sma_20"] = calculate_sma(close, 20)

        # EMA with SMA-based seeding and strict window requirement
        ticker_df["ema_10"] = calculate_ema_with_sma_seed(close, 10)
        ticker_df["ema_20"] = calculate_ema_with_sma_seed(close, 20)

        result_data.append(ticker_df)

    result = pd.concat(result_data, ignore_index=True)
    print(" Technical indicators calculated: SMA_10, SMA_20, EMA_10, EMA_20")
    # Returns: DataFrame with added technical indicators
    return result

# Ensuring each ticker has exactly 24 rows by taking the last 24 months and validating data.
def ensure_exactly_24_rows(df: pd.DataFrame) -> pd.DataFrame:
    
    result_data = []

    for ticker in df["ticker"].unique():
        ticker_df = df[df["ticker"] == ticker].copy()
        ticker_df = ticker_df.sort_values("date")

        # Take last 24 rows (most recent 24 months)
        ticker_df = ticker_df.iloc[-24:]

        if len(ticker_df) < 24:
            print(f"⚠ Warning: {ticker} has only {len(ticker_df)} months of data (expected 24)")

        result_data.append(ticker_df)

    result = pd.concat(result_data, ignore_index=True)
    print(" Ensured exactly 24 rows per ticker (last 24 months)")
    return result

# Partition DataFrame by ticker and save each to separate CSV files.
def partition_and_save(df: pd.DataFrame, output_dir: str = "output") -> Dict[str, int]:
    
    os.makedirs(output_dir, exist_ok=True)

    stats: Dict[str, int] = {}

    for ticker in sorted(df["ticker"].unique()):
        ticker_df = df[df["ticker"] == ticker].copy()
        ticker_df = ticker_df.sort_values("date")

        output_columns = [
            "date",
            "open",
            "high",
            "low",
            "close",
            "sma_10",
            "sma_20",
            "ema_10",
            "ema_20",
        ]
        ticker_df = ticker_df[output_columns]

        output_file = os.path.join(output_dir, f"result_{ticker}.csv")
        ticker_df.to_csv(output_file, index=False, float_format="%.6f")

        stats[ticker] = len(ticker_df)
        print(f"  → {ticker}: {len(ticker_df)} rows saved to {output_file}")
    #Returns: Dictionary with ticker: row_count mapping
    return stats

# Validate that output meets requirements.
def validate_output(stats: Dict[str, int], expected_rows: int = 24):
   
    print(f"\n{'=' * 60}")
    print("VALIDATION REPORT")
    print(f"{'=' * 60}")

    all_valid = True
    for ticker, count in stats.items():
        status = "✓" if count == expected_rows else "✗"
        print(f"{status} {ticker}: {count} rows (expected: {expected_rows})")
        if count != expected_rows:
            all_valid = False

    print(f"{'=' * 60}")
    if all_valid:
        print("All files validated successfully!")
    else:
        print(" Warning: Some files do not have exactly 24 rows")
    print(f"{'=' * 60}\n")

# Main execution flow
def main():
    
    print("\n" + "=" * 60)
    print("FamPay Data Engineering Assessment")
    print("Stock Data Monthly Aggregation & Technical Indicators")
    print("=" * 60 + "\n")

    INPUT_FILE = "stock_data.csv"
    OUTPUT_DIR = "output"

    # Step 1: Load data
    print("[1/5] Loading data...")
    df = load_data(INPUT_FILE)

    # Step 2: Aggregate to monthly
    print("\n[2/5] Aggregating to monthly frequency (month-end labels)...")
    monthly_df = aggregate_to_monthly(df)

    # Step 3: Calculate technical indicators
    print("\n[3/5] Calculating technical indicators on monthly closes...")
    final_df = add_technical_indicators(monthly_df)

    # Step 4: Ensure exactly 24 rows per ticker
    print("\n[4/5] Ensuring exactly 24 rows per ticker...")
    final_df = ensure_exactly_24_rows(final_df)

    # Step 5: Partition and save
    print("\n[5/5] Partitioning and saving results...")
    stats = partition_and_save(final_df, OUTPUT_DIR)

    # Validate output
    print("\nValidating output...")
    validate_output(stats)

    print("✓ Process completed successfully!")
    print(f"✓ Output files saved in './{OUTPUT_DIR}/' directory\n")


if __name__ == "__main__":
    main()
