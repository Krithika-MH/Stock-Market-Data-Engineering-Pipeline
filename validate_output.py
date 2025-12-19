
#Validation script to check output correctness

import pandas as pd
import os


def validate_outputs():
    
    expected_tickers = ['AAPL', 'AMD', 'AMZN', 'AVGO', 'CSCO', 
                       'MSFT', 'NFLX', 'PEP', 'TMUS', 'TSLA']
    
    expected_columns = ['date', 'open', 'high', 'low', 'close',
                       'sma_10', 'sma_20', 'ema_10', 'ema_20']

    print("\n" + "="*60)
    print("OUTPUT VALIDATION REPORT")
    print("="*60 + "\n")

    all_valid = True

    for ticker in expected_tickers:
        filename = f'output/result_{ticker}.csv'

        if not os.path.exists(filename):
            print(f"{ticker}: File not found!")
            all_valid = False
            continue

        df = pd.read_csv(filename)

        # Check row count
        row_check = "✓" if len(df) == 24 else "✗"
        print(f"{row_check} {ticker}: {len(df)} rows (expected 24)")

        # Check columns
        missing_cols = set(expected_columns) - set(df.columns)
        if missing_cols:
            print(f"Missing columns: {missing_cols}")
            all_valid = False

        # Check for extra columns not in expected
        extra_cols = set(df.columns) - set(expected_columns)
        if extra_cols:
            print(f"Extra columns found: {extra_cols}")

        # Check for NaN in critical OHLC columns (should NOT have NaN)
        if df[['open', 'high', 'low', 'close']].isnull().any().any():
            print(f"Contains NaN values in OHLC columns")
            all_valid = False

        # Validate OHLC logic
        if not (df['high'] >= df['low']).all():
            print(f" High not always >= Low")
            all_valid = False

        if not ((df['high'] >= df['open']) & (df['high'] >= df['close'])).all():
            print(f" High not always >= Open/Close")
            all_valid = False

        if not ((df['low'] <= df['open']) & (df['low'] <= df['close'])).all():
            print(f" Low not always <= Open/Close")
            all_valid = False

        # Check that SMA_10 and EMA_10 have NaN for first 9 rows
        if df['sma_10'].iloc[:9].notna().any():
            print(f" Warning: SMA_10 has values before month 10")
        
        if df['ema_10'].iloc[:9].notna().any():
            print(f" Warning: EMA_10 has values before month 10")

        # Check that SMA_20 and EMA_20 have NaN for first 19 rows
        if df['sma_20'].iloc[:19].notna().any():
            print(f" Warning: SMA_20 has values before month 20")
        
        if df['ema_20'].iloc[:19].notna().any():
            print(f" Warning: EMA_20 has values before month 20")

        # Verify SMA_10 starts at row 9 (index 9, 10th month)
        if len(df) >= 10 and pd.isna(df['sma_10'].iloc[9]):
            print(f" SMA_10 should have value at month 10 (index 9)")
            all_valid = False

        # Verify SMA_20 starts at row 19 (index 19, 20th month)
        if len(df) >= 20 and pd.isna(df['sma_20'].iloc[19]):
            print(f"  SMA_20 should have value at month 20 (index 19)")
            all_valid = False

    print("\n" + "="*60)
    if all_valid:
        print(" ALL VALIDATIONS PASSED ")
    else:
        print("SOME VALIDATIONS FAILED ")
    print("="*60 + "\n")


if __name__ == "__main__":
    validate_outputs()
