import pandas as pd
import glob
import os

def clean_and_process_data(input_folder='data', output_file='formatted_sales.csv'):
    # Get all CSV files in the data folder
    files = glob.glob(os.path.join(input_folder, '*.csv'))
    
    all_data = []
    
    for file in files:
        # Read CSV file
        df = pd.read_csv(file)
        
        # Filter for pink morsels only (case insensitive)
        df = df[df['product'].str.lower() == 'pink morsel']
        
        if not df.empty:
            # Clean price: remove $ and convert to float
            df['price'] = df['price'].replace('[\$,]', '', regex=True).astype(float)
            
            # Calculate sales
            df['sales'] = df['price'] * df['quantity']
            
            # Format sales to 2 decimal places
            df['sales'] = df['sales'].round(2)
            
            # Select and rename columns
            df = df[['sales', 'date', 'region']]
            
            all_data.append(df)
    
    if all_data:
        # Combine all DataFrames
        final_df = pd.concat(all_data, ignore_index=True)
        
        # Sort by date
        final_df = final_df.sort_values('date')
        
        # Save to CSV
        final_df.to_csv(output_file, index=False)
        print(f"Successfully processed data. Output saved to {output_file}")
        return final_df
    else:
        print("No pink morsel data found in any files.")
        return None

if __name__ == '__main__':
    clean_and_process_data()