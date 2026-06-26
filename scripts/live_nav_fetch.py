import os
import requests
import pandas as pd

RAW_DATA_DIR = "data\\raw"

target_schemes = {
    "125497": "HDFC_Top_100_Direct",
    "119551": "SBI_Bluechip",
    "120503": "ICICI_Bluechip",
    "118632": "Nippon_Large_Cap",
    "119092": "Axis_Bluechip",
    "120841": "Kotak_Bluechip"
}

def fetch_and_save_nav(scheme_code, scheme_name):
    url = f"https://api.mfapi.in/mf/{scheme_code}"
    print(f"Fetching data for {scheme_name} (Code: {scheme_code})...")
    
    try:
        response = requests.get(url, timeout=15)
        if response.status_code == 200:
            data = response.json()
            
            nav_list = data.get("data", [])
            meta = data.get("meta", {})
            
            if nav_list:
                df = pd.DataFrame(nav_list)

                df["scheme_code"] = meta.get("scheme_code", scheme_code)
                df["scheme_name"] = meta.get("scheme_name", scheme_name)
                

                df = df[["scheme_code", "scheme_name", "date", "nav"]]

                output_file = os.path.join(RAW_DATA_DIR, f"live_nav_{scheme_code}.csv")
                df.to_csv(output_file, index=False)
                print(f"Successfully saved {len(df)} rows to {output_file}")
            else:
                print(f"No NAV records returned for {scheme_code}.")
        else:
            print(f"Failed to fetch data. HTTP Status Code: {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred while calling the API: {e}")

if __name__ == "__main__":
    print("=== LIVE NAV FETCH ACTIVATED ===")
    for code, name in target_schemes.items():
        fetch_and_save_nav(code, name)