import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import os

# Task 1: Read all CSV files from data folder
def read_all_csvs():
    data_folder = Path('./data')
    all_data = []
    
    for csv_file in data_folder.glob('*.csv'):
        try:
            df = pd.read_csv(csv_file)
            df['building'] = csv_file.stem  # Use filename as building name
            all_data.append(df)
            print(f"Loaded: {csv_file.name}")
        except:
            print(f"Skipped bad file: {csv_file.name}")
    
    if all_data:
        return pd.concat(all_data, ignore_index=True)
    return pd.DataFrame()

# Task 2: Calculate summaries
def get_summaries(df):
    # Daily totals
    df['date'] = pd.to_datetime(df['timestamp']).dt.date
    daily = df.groupby(['date', 'building'])['kwh'].sum().reset_index()
    
    # Building summary
    summary = df.groupby('building')['kwh'].agg(['mean', 'sum', 'max']).round(2)
    
    return daily, summary

# Task 3: Simple classes
class Building:
    def __init__(self, name):
        self.name = name
        self.total_kwh = 0
    
    def add_kwh(self, kwh):
        self.total_kwh += kwh

# Task 4: Make charts
def make_charts(df_daily, summary):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
    
    # Daily trend
    for building in df_daily['building'].unique():
        building_data = df_daily[df_daily['building'] == building]
        ax1.plot(building_data['date'], building_data['kwh'], label=building)
    ax1.set_title('Daily Usage')
    ax1.legend()
    
    # Building comparison
    summary['sum'].plot(kind='bar', ax=ax2)
    ax2.set_title('Total by Building')
    
    plt.savefig('dashboard.png')
    plt.close()
    print("Saved: dashboard.png")

# Task 5: Save files
def save_results(df, summary):
    Path('./output').mkdir(exist_ok=True)
    
    # Save cleaned data
    df.to_csv('output/cleaned_data.csv', index=False)
    
    # Save summary
    summary.to_csv('output/summary.csv')
    
    # Print report
    total = df['kwh'].sum()
    top_building = summary['sum'].idxmax()
    print(f"\n=== SUMMARY ===")
    print(f"Total kWh: {total:,.0f}")
    print(f"Top building: {top_building}")
    print("Files saved in output/")

# MAIN CODE
df = read_all_csvs()
if not df.empty:
    daily, summary = get_summaries(df)
    make_charts(daily, summary)
    save_results(df, summary)
    print("DONE!")
else:
    print("No data files found in ./data/")
