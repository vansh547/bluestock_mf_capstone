import os
import pandas as pd

RAW_DATA_DIR = os.path.join("data", "raw")

csv_files = [
    "01_fund_master.csv",
    "02_nav_history.csv", 
    "03_aum_by_fund_house.csv",
    "04_monthly_sip_inflows.csv",
    "05_category_inflows.csv",
    "06_industry_folio_count.csv",
    "07_scheme_performance.csv",
    "08_investor_transactions.csv",
    "09_portfolio_holdings.csv",
    "10_benchmark_indices.csv"
]

def load_and_profile_datasets():
    print("=== TASK 1: LOADING & PROFILING DATASETS ===")
    datasets = {}
    
    for file in csv_files:
        file_path = os.path.join(RAW_DATA_DIR, file)
        if os.path.exists(file_path):
            print(f"\nProcessing: {file}")
            df = pd.read_csv(file_path)
            datasets[file] = df
            
            print(f"Shape: {df.shape}")
            print("\nData Types:")
            print(df.dtypes.to_dict())  # Shortened printing format
            print(f"Loaded {len(df)} rows successfully.")
            print("-" * 50)
        else:
            print(f"Warning: File not found at {file_path}")
            
    return datasets

def explore_fund_master(datasets):
    print("\n=== TASK 2: EXPLORING FUND MASTER ===")
    fund_master_key = "01_fund_master.csv"
    
    if fund_master_key in datasets:
        df_master = datasets[fund_master_key]
        print("Fund Master Columns:", df_master.columns.tolist())
        
        for col in df_master.columns:
            unique_count = df_master[col].nunique()
            print(f"Unique values in '{col}': {unique_count}")
            if unique_count <= 15:  
                print(df_master[col].dropna().unique())
    else:
        print("Fund master dataset missing.")

def validate_amfi_codes(datasets):
    print("\n=== TASK 3: VALIDATING AMFI CODES & QUALITY SUMMARY ===")
    master_key = "01_fund_master.csv"
    nav_key = "02_nav_history.csv"
    
    if master_key in datasets and nav_key in datasets:
        df_master = datasets[master_key]
        df_nav = datasets[nav_key]
        
        master_code_col = [c for c in df_master.columns if 'code' in c.lower()][0]
        nav_code_col = [c for c in df_nav.columns if 'code' in c.lower()][0]
        
        master_codes = set(df_master[master_code_col].dropna().unique())
        nav_codes = set(df_nav[nav_code_col].dropna().unique())
        
        missing_in_nav = master_codes - nav_codes
        
        print(f"Total Unique Codes in Fund Master: {len(master_codes)}")
        print(f"Total Unique Codes in NAV History: {len(nav_codes)}")
        print(f"Fund Master codes missing from NAV History: {len(missing_in_nav)}")
    else:
        print("Required datasets for validation are missing.")

if __name__ == "__main__":
    loaded_data = load_and_profile_datasets()
    explore_fund_master(loaded_data)
    validate_amfi_codes(loaded_data)
    
    print("\n==========================================")
    print("🏁 FINAL SUMMARY CHECKLIST OF PROCESSED FILES:")
    print("==========================================")
    for i, file in enumerate(csv_files, 1):
        status = "✅ Processed" if file in loaded_data else "❌ Missing"
        print(f"{i}. {file}: {status}")