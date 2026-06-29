import os
import sqlite3
import pandas as pd

DB_PATH = "bluestock_mf.db"
RAW_DIR = "data/raw"
PROCESSED_DIR = "data/processed"
os.makedirs(PROCESSED_DIR, exist_ok=True)

def run_etl():
    conn = sqlite3.connect(DB_PATH)
    print("=== Starting Capstone ETL Pipeline ===")

    df_fund = pd.read_csv(os.path.join(RAW_DIR, "01_fund_master.csv"))
    fund_cols = ['amfi_code', 'fund_house', 'scheme_name', 'category', 'sub_category', 
                 'expense_ratio_pct', 'exit_load_pct', 'min_sip_amount', 'min_lumpsum_amount', 
                 'fund_manager', 'risk_category', 'sebi_category_code']
    df_fund_clean = df_fund[fund_cols]
    df_fund_clean.to_sql("dim_fund", conn, if_exists="append", index=False)
    df_fund_clean.to_csv(os.path.join(PROCESSED_DIR, "01_fund_master_processed.csv"), index=False)
    print(f"Loaded {len(df_fund_clean)} records into dim_fund.")

    df_nav = pd.read_csv(os.path.join(RAW_DIR, "02_nav_history.csv"))
    df_nav_clean = df_nav[['amfi_code', 'date', 'nav']].copy()
    df_nav_clean['date'] = pd.to_datetime(df_nav_clean['date']).dt.strftime('%Y-%m-%d') # Standardize date format
    df_nav_clean.to_sql("fact_nav", conn, if_exists="append", index=False)
    df_nav_clean.to_csv(os.path.join(PROCESSED_DIR, "02_nav_history_processed.csv"), index=False)
    print(f"Loaded {len(df_nav_clean)} records into fact_nav.")

    df_tx = pd.read_csv(os.path.join(RAW_DIR, "08_investor_transactions.csv"))
    if 'transaction_date' in df_tx.columns:
        df_tx['transaction_date'] = pd.to_datetime(df_tx['transaction_date']).dt.strftime('%Y-%m-%d')
    df_tx.to_sql("fact_transactions", conn, if_exists="append", index=False)
    df_tx.to_csv(os.path.join(PROCESSED_DIR, "08_investor_transactions_processed.csv"), index=False)
    print(f"Loaded {len(df_tx)} records into fact_transactions.")

    df_perf = pd.read_csv(os.path.join(RAW_DIR, "07_scheme_performance.csv"))
    perf_cols = ['amfi_code', 'scheme_name', 'return_1yr_pct', 'return_3yr_pct', 'return_5yr_pct', 'expense_ratio_pct', 'risk_grade']
    df_perf_clean = df_perf[perf_cols]
    df_perf_clean.to_sql("fact_performance", conn, if_exists="append", index=False)
    df_perf_clean.to_csv(os.path.join(PROCESSED_DIR, "07_scheme_performance_processed.csv"), index=False)
    print(f"Loaded {len(df_perf_clean)} records into fact_performance.")

    df_aum = pd.read_csv(os.path.join(RAW_DIR, "03_aum_by_fund_house.csv"))
    df_aum.to_sql("fact_aum", conn, if_exists="append", index=False)
    df_aum.to_csv(os.path.join(PROCESSED_DIR, "03_aum_by_fund_house_processed.csv"), index=False)
    print(f"Loaded {len(df_aum)} records into fact_aum.")

    conn.close()
    print("=== ETL Processing Complete & Synced! ===")

if __name__ == "__main__":
    run_etl()