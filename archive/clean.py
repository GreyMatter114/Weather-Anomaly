import pandas as pd

def remove_rows_with_empty_values(input_file, output_file, timestamp_column=None):
    # Read the CSV file into a pandas DataFrame
    df = pd.read_csv(input_file)
    
    # Remove rows that contain any NaN (empty) values
    df_cleaned = df
    
    # Convert the timestamp column to the day of the year if it's provided
    if timestamp_column and timestamp_column in df_cleaned.columns:
        # Ensure the timestamp column is in datetime format
        df_cleaned[timestamp_column] = pd.to_datetime(df_cleaned[timestamp_column], errors='coerce')
        
        # If the conversion fails, it replaces the invalid dates with NaT (Not a Time), 
        # so drop rows where the timestamp could not be parsed.
        df_cleaned = df_cleaned.dropna(subset=[timestamp_column])

        # Add a new column for the day of the year
        df_cleaned['Date time'] = df_cleaned[timestamp_column].dt.dayofyear
    
    # Write the cleaned DataFrame to a new CSV file
    df_cleaned.to_csv(output_file, index=False)
    print(f"Rows with empty values have been removed and day of year has been added. The cleaned file is saved as '{output_file}'.")

# Example usage:
input_file = '5yrdata.csv'  # Replace with your input CSV file name
output_file = 'cleaned_output.csv'  # Replace with your desired output file name
timestamp_column = 'Date time'  # Replace with the name of the timestamp column, if applicable

remove_rows_with_empty_values(input_file, output_file, timestamp_column)
